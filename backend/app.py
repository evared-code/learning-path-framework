"""
Production FastAPI Backend with Z.AI Integration
Uses OpenAI-compatible API with GLM models
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import numpy as np
import sqlite3
from openai import OpenAI

app = FastAPI(
    title="Q-Learning Framework - Z.AI Integration",
    description="Use Z.AI GLM models with your API key",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_PATH = "learning_paths.db"

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS learning_paths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            participant_id TEXT,
            participant_name TEXT,
            mode TEXT,
            model_name TEXT,
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

# Z.AI Available Models
ZAI_MODELS = {
    "glm-5": "GLM-5 (Latest Flagship - Recommended)",
    "glm-4.7": "GLM-4.7 (High Performance)",
    "glm-4.5": "GLM-4.5 (Balanced)",
    "glm-4.5-flash": "GLM-4.5 Flash (Fast & Free)",
    "glm-4.5-air": "GLM-4.5 Air (Lightweight & Free)",
    "glm-4.6v": "GLM-4.6V (Vision)",
    "glm-4": "GLM-4 (Stable)"
}

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

# Pydantic Models
class GeneratePathRequest(BaseModel):
    current: List[float] = Field(..., min_items=12, max_items=12)
    target: List[float] = Field(..., min_items=12, max_items=12)
    mode: Literal["heuristic", "llm"] = "heuristic"
    model_name: Optional[str] = "glm-5"
    zai_api_key: Optional[str] = None
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
    model_name: Optional[str] = None
    path: List[str]
    courses: List[CourseResponse]
    initial_gap: float
    final_gap: float
    gap_reduction: float
    iterations: int
    final_state: List[float]

class HealthResponse(BaseModel):
    status: str
    available_models: dict
    version: str

class ValidateKeyRequest(BaseModel):
    zai_api_key: str

# Q-value functions
def heuristic_q_value(course: dict, current: np.ndarray, target: np.ndarray) -> float:
    """Heuristic Q-value calculation"""
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

async def zai_q_value(course: dict, current: np.ndarray, target: np.ndarray, 
                      model: str, api_key: str) -> float:
    """Query Z.AI GLM model using OpenAI-compatible API"""
    
    gap = target - current
    
    prompt = f"""Rate this cybersecurity course (0-10) for this learner:

Current competencies (0-3 scale): {current.tolist()}
Target competencies: {target.tolist()}
Current gaps: {gap.tolist()}

SDLC Phases: {', '.join(PHASE_NAMES)}

Course Details:
- Name: {course['name']}
- Difficulty: {course['difficulty']}/3 (1=Beginner, 2=Intermediate, 3=Advanced)
- Competency Impact: {course['competency_impact']}
- Topics Covered: {', '.join(course['topics'])}

Evaluate: How valuable is this course for THIS learner RIGHT NOW?
Consider: gap reduction potential, relevance to current needs, difficulty appropriateness.

Respond with ONLY a single number from 0 to 10."""

    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.z.ai/api/paas/v4/"
        )
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert in cybersecurity training and competency development."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=50
        )
        
        text = response.choices[0].message.content.strip()
        
        # Extract number
        import re
        numbers = re.findall(r'\d+\.?\d*', text)
        if numbers:
            q_value = float(numbers[0]) / 3.0  # Normalize to 0-3 scale
            return max(0, min(q_value, 3))
        else:
            return 1.5
            
    except Exception as e:
        print(f"Z.AI API error: {e}")
        return heuristic_q_value(course, current, target)

# API Endpoints
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Q-Learning Framework with Z.AI Integration",
        "version": "1.0.0",
        "description": "Use your own Z.AI API key to access GLM models",
        "docs": "/docs",
        "get_api_key": "https://z.ai/model-api"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health():
    return HealthResponse(
        status="healthy",
        available_models=ZAI_MODELS,
        version="1.0.0"
    )

@app.post("/validate_key", tags=["API Key"])
async def validate_key(request: ValidateKeyRequest):
    """Validate Z.AI API key"""
    try:
        client = OpenAI(
            api_key=request.zai_api_key,
            base_url="https://api.z.ai/api/paas/v4/"
        )
        
        response = client.chat.completions.create(
            model="glm-4.5-flash",  # Use free model for validation
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        if response.choices:
            return {"valid": True, "message": "API key is valid"}
        else:
            return {"valid": False, "message": "Invalid response from API"}
            
    except Exception as e:
        return {"valid": False, "message": str(e)}

@app.get("/models", tags=["Models"])
async def list_models():
    """List all available Z.AI models"""
    return {
        "models": ZAI_MODELS,
        "count": len(ZAI_MODELS),
        "description": "Z.AI GLM model family"
    }

@app.post("/generate_path", response_model=PathResponse, tags=["Learning Path"])
async def generate_path(request: GeneratePathRequest):
    """Generate personalized learning path"""
    try:
        current = np.array(request.current, dtype=float)
        target = np.array(request.target, dtype=float)
        mode = request.mode
        model_name = request.model_name or "glm-5"
        
        # Validate API key for LLM mode
        if mode == "llm":
            if not request.zai_api_key:
                raise HTTPException(
                    status_code=400,
                    detail="Z.AI API key required for LLM mode. Get yours at https://z.ai/model-api"
                )
        
        # Q-Learning algorithm
        path = []
        state = current.copy()
        available = COURSE_CATALOG.copy()
        epsilon = 0.5
        max_iter = 10
        
        for iteration in range(max_iter):
            gap = np.linalg.norm(target - state)
            if gap < epsilon or not available:
                break
            
            # Calculate Q-values
            q_values = []
            for course in available:
                if mode == "llm":
                    q = await zai_q_value(course, state, target, model_name, request.zai_api_key)
                else:
                    q = heuristic_q_value(course, state, target)
                q_values.append({'course': course, 'q_value': q})
            
            # Greedy selection
            q_values.sort(key=lambda x: x['q_value'], reverse=True)
            best = q_values[0]
            
            path.append({
                'course_id': best['course']['id'],
                'q_value': best['q_value']
            })
            
            # Update state
            state = np.minimum(state + np.array(best['course']['competency_impact']), 3.0)
            available = [c for c in available if c['id'] != best['course']['id']]
        
        # Calculate metrics
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
        if request.participant_id:
            try:
                conn = sqlite3.connect(DATABASE_PATH)
                c = conn.cursor()
                c.execute('''
                    INSERT INTO learning_paths 
                    (participant_id, participant_name, mode, model_name, 
                     initial_gap, final_gap, gap_reduction, path)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    request.participant_id,
                    request.participant_name or "Unknown",
                    mode,
                    model_name if mode == "llm" else None,
                    round(initial_gap, 2),
                    round(final_gap, 2),
                    round(gap_reduction, 1),
                    ','.join([c.id for c in courses])
                ))
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"DB error: {e}")
        
        return PathResponse(
            success=True,
            mode=mode,
            model_name=model_name if mode == "llm" else None,
            path=[c.id for c in courses],
            courses=courses,
            initial_gap=round(initial_gap, 2),
            final_gap=round(final_gap, 2),
            gap_reduction=round(gap_reduction, 1),
            iterations=len(path),
            final_state=state.tolist()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/courses", tags=["Courses"])
async def list_courses():
    return {"courses": COURSE_CATALOG, "count": len(COURSE_CATALOG)}

@app.get("/phases", tags=["SDLC"])
async def list_phases():
    return {"phases": PHASE_NAMES, "count": len(PHASE_NAMES)}

@app.get("/history", tags=["Analytics"])
async def get_history(limit: int = 10):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('''
            SELECT participant_id, participant_name, mode, model_name,
                   initial_gap, final_gap, gap_reduction, path, created_at
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
                "model_name": row[3],
                "initial_gap": row[4],
                "final_gap": row[5],
                "gap_reduction": row[6],
                "path": row[7].split(','),
                "created_at": row[8]
            })
        
        return {"history": history, "count": len(history)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
