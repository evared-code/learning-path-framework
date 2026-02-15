"""
Production FastAPI Backend
- Dual Q-function modes (Heuristic + LLM)
- SQLite database for path storage
- Complete API with documentation
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import numpy as np
import os
import sqlite3
from datetime import datetime
from anthropic import Anthropic

# Initialize FastAPI
app = FastAPI(
    title="Q-Learning Framework API",
    description="Personalized cybersecurity learning path generation with dual-mode Q-function",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Anthropic client
anthropic_client = None
if os.environ.get("ANTHROPIC_API_KEY"):
    anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Database setup
DATABASE_PATH = os.environ.get("DATABASE_PATH", "learning_paths.db")

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS learning_paths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            participant_id TEXT,
            participant_name TEXT,
            mode TEXT,
            initial_gap REAL,
            final_gap REAL,
            gap_reduction REAL,
            path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Course catalog
COURSE_CATALOG = [
    {'id':'C01','name':'Secure Coding Fundamentals','platform':'Coursera',
     'competency_impact':[0.5,0.3,1.0,0.5,0.2,0.3,0.2,0.2,0.3,0.2,0.3,0.2],
     'topics':['OWASP A03','OWASP A01','Input Validation'],'difficulty':1},
    {'id':'C02','name':'Threat Modeling for Developers','platform':'Pluralsight',
     'competency_impact':[0.8,1.0,0.3,0.3,0.2,0.2,0.3,0.3,0.2,0.3,0.2,0.3],
     'topics':['STRIDE','Attack Trees','Security Architecture'],'difficulty':2},
    {'id':'C03','name':'Security Testing & SAST/DAST','platform':'Udemy',
     'competency_impact':[0.3,0.3,0.5,1.0,0.3,0.3,0.2,0.2,0.5,0.3,0.2,0.3],
     'topics':['DAST','SAST','OWASP Testing'],'difficulty':1},
    {'id':'C04','name':'Container & Cloud Security','platform':'Linux Foundation',
     'competency_impact':[0.2,0.5,0.3,0.3,1.0,0.5,0.2,0.2,0.2,0.2,0.8,0.3],
     'topics':['Docker Security','OWASP A05','Cloud Security'],'difficulty':2},
    {'id':'C05','name':'API Security Best Practices','platform':'Pluralsight',
     'competency_impact':[0.5,0.8,1.0,0.5,0.3,0.3,0.2,0.2,0.3,0.2,0.3,0.3],
     'topics':['OWASP A01','OWASP A07','OAuth 2.0'],'difficulty':2},
    {'id':'C06','name':'DevSecOps & Security in Agile','platform':'Scrum Alliance',
     'competency_impact':[0.5,0.3,0.3,0.5,0.3,0.3,1.0,0.8,0.5,0.5,0.3,0.5],
     'topics':['Secure SDLC','DevSecOps','CI/CD Security'],'difficulty':1},
    {'id':'C07','name':'Advanced Web Application Security','platform':'SANS',
     'competency_impact':[0.3,0.5,1.0,0.8,0.3,0.3,0.2,0.2,0.3,0.3,0.2,0.3],
     'topics':['OWASP A01','OWASP A02','XSS','CSRF'],'difficulty':2},
    {'id':'C08','name':'Vulnerability Management','platform':'Cybrary',
     'competency_impact':[0.3,0.2,0.3,0.5,0.3,1.0,0.3,0.3,1.0,0.5,0.3,0.5],
     'topics':['CVE','Patch Management','Incident Response'],'difficulty':1},
    {'id':'C09','name':'Secure Architecture Design','platform':'Coursera',
     'competency_impact':[0.8,1.0,0.5,0.3,0.5,0.3,0.3,0.3,0.2,0.3,0.3,0.5],
     'topics':['Security Architecture','Zero Trust'],'difficulty':3},
    {'id':'C10','name':'Security Metrics & Risk Management','platform':'ISACA',
     'competency_impact':[0.5,0.3,0.2,0.3,0.2,0.3,0.5,0.5,0.3,1.0,0.3,0.8],
     'topics':['Security Metrics','Risk Assessment','Compliance'],'difficulty':2}
]

PHASE_NAMES = [
    'Requirements', 'Design', 'Development', 'Testing', 
    'Deployment', 'Maintenance', 'Process Planning', 'Team Coordination',
    'Defect Management', 'Estimation & Metrics', 'Config Management', 'Documentation'
]

# Pydantic models
class GeneratePathRequest(BaseModel):
    current: List[float] = Field(..., min_items=12, max_items=12)
    target: List[float] = Field(..., min_items=12, max_items=12)
    mode: Literal["heuristic", "llm"] = "heuristic"
    participant_id: Optional[str] = None
    participant_name: Optional[str] = None

class CourseResponse(BaseModel):
    id: str
    name: str
    platform: str
    topics: List[str]
    difficulty: int
    q_value: Optional[float] = None

class PathResponse(BaseModel):
    success: bool
    mode: str
    path: List[str]
    courses: List[CourseResponse]
    initial_gap: float
    final_gap: float
    gap_reduction: float
    iterations: int
    final_state: List[float]
    saved_to_db: bool = False

class HealthResponse(BaseModel):
    status: str
    llm_available: bool
    version: str
    database_connected: bool

# Q-value functions
def heuristic_q_value(course: dict, current: np.ndarray, target: np.ndarray) -> float:
    """Heuristic Q-value: Q(s,a) = 0.6·Δ_gap + 0.3·r_rel + 0.1·r_diff"""
    impact = np.array(course['competency_impact'])
    gap = target - current
    gap_norm = np.linalg.norm(gap)
    
    if gap_norm < 0.01:
        return 0.0
    
    potential = np.minimum(current + impact, 3.0)
    new_gap_norm = np.linalg.norm(target - potential)
    gap_reduction = gap_norm - new_gap_norm
    
    relevance = np.dot(impact, gap) / gap_norm
    avg_current = np.mean(current)
    difficulty_match = 1.0 - abs(course['difficulty'] - avg_current) / 3.0
    
    return 0.6 * gap_reduction + 0.3 * relevance + 0.1 * difficulty_match

async def llm_q_value(course: dict, current: np.ndarray, target: np.ndarray) -> float:
    """LLM-based Q-value estimation using Claude API"""
    if not anthropic_client:
        raise HTTPException(status_code=400, detail="LLM mode requires ANTHROPIC_API_KEY")
    
    gap = target - current
    prompt = f"""Expert cybersecurity training evaluation.

Current competency: {current.tolist()}
Target competency: {target.tolist()}
Gap: {gap.tolist()}

Phases: {', '.join(PHASE_NAMES)}

Course: {course['name']}
Platform: {course['platform']}
Difficulty: {course['difficulty']} (1=Beginner, 2=Intermediate, 3=Advanced)
Impact: {course['competency_impact']}
Topics: {', '.join(course['topics'])}

Rate this course's value (0-10) for this learner RIGHT NOW.
Consider: gap reduction, relevance, difficulty match, topic importance.

Number only:"""

    try:
        message = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=50,
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}]
        )
        q_value = float(message.content[0].text.strip()) / 3.0
        return q_value
    except Exception as e:
        print(f"LLM error: {e}, falling back to heuristic")
        return heuristic_q_value(course, current, target)

# API Endpoints
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Q-Learning Framework API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "generate_path": "/generate_path",
            "courses": "/courses",
            "phases": "/phases"
        }
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.close()
        db_connected = True
    except:
        db_connected = False
    
    return HealthResponse(
        status="healthy",
        llm_available=anthropic_client is not None,
        version="1.0.0",
        database_connected=db_connected
    )

@app.post("/generate_path", response_model=PathResponse, tags=["Learning Path"])
async def generate_path(request: GeneratePathRequest):
    """Generate personalized learning path with Q-Learning"""
    try:
        current = np.array(request.current, dtype=float)
        target = np.array(request.target, dtype=float)
        mode = request.mode
        
        if mode == "llm" and not anthropic_client:
            raise HTTPException(status_code=400, detail="LLM mode requires API key")
        
        q_function = llm_q_value if mode == "llm" else heuristic_q_value
        
        # Q-Learning algorithm
        path = []
        state = current.copy()
        available = COURSE_CATALOG.copy()
        epsilon = 0.5
        max_iter = 10
        
        for _ in range(max_iter):
            gap = np.linalg.norm(target - state)
            if gap < epsilon or not available:
                break
            
            q_values = []
            for course in available:
                q = await q_function(course, state, target) if mode == "llm" else q_function(course, state, target)
                q_values.append({'course': course, 'q_value': q})
            
            q_values.sort(key=lambda x: x['q_value'], reverse=True)
            best = q_values[0]
            
            path.append({'course_id': best['course']['id'], 'q_value': best['q_value']})
            state = np.minimum(state + np.array(best['course']['competency_impact']), 3.0)
            available = [c for c in available if c['id'] != best['course']['id']]
        
        # Metrics
        initial_gap = float(np.linalg.norm(target - current))
        final_gap = float(np.linalg.norm(target - state))
        gap_reduction = ((initial_gap - final_gap) / initial_gap * 100) if initial_gap > 0 else 100
        
        # Build response
        courses = []
        for item in path:
            course = next(c for c in COURSE_CATALOG if c['id'] == item['course_id'])
            courses.append(CourseResponse(
                id=course['id'],
                name=course['name'],
                platform=course['platform'],
                topics=course['topics'],
                difficulty=course['difficulty'],
                q_value=item['q_value']
            ))
        
        # Save to database
        saved = False
        if request.participant_id:
            try:
                conn = sqlite3.connect(DATABASE_PATH)
                c = conn.cursor()
                c.execute('''
                    INSERT INTO learning_paths 
                    (participant_id, participant_name, mode, initial_gap, final_gap, gap_reduction, path)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    request.participant_id,
                    request.participant_name or "Unknown",
                    mode,
                    round(initial_gap, 2),
                    round(final_gap, 2),
                    round(gap_reduction, 1),
                    ','.join([c.id for c in courses])
                ))
                conn.commit()
                conn.close()
                saved = True
            except Exception as e:
                print(f"DB save error: {e}")
        
        return PathResponse(
            success=True,
            mode=mode,
            path=[c.id for c in courses],
            courses=courses,
            initial_gap=round(initial_gap, 2),
            final_gap=round(final_gap, 2),
            gap_reduction=round(gap_reduction, 1),
            iterations=len(path),
            final_state=state.tolist(),
            saved_to_db=saved
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/courses", tags=["Courses"])
async def list_courses():
    """List all available courses"""
    return {"courses": COURSE_CATALOG, "count": len(COURSE_CATALOG)}

@app.get("/phases", tags=["SDLC"])
async def list_phases():
    """List all SDLC phases"""
    return {"phases": PHASE_NAMES, "count": len(PHASE_NAMES)}

@app.get("/history", tags=["Analytics"])
async def get_history(limit: int = 10):
    """Get recent learning path history"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('''
            SELECT participant_id, participant_name, mode, initial_gap, final_gap, 
                   gap_reduction, path, created_at
            FROM learning_paths
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        rows = c.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                "participant_id": row[0],
                "participant_name": row[1],
                "mode": row[2],
                "initial_gap": row[3],
                "final_gap": row[4],
                "gap_reduction": row[5],
                "path": row[6].split(','),
                "created_at": row[7]
            })
        
        return {"history": history, "count": len(history)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
