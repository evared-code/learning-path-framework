# 🚀 COMPLETE DEPLOYMENT GUIDE
## Q-Learning Framework for Cybersecurity Learning Paths

---

## 📦 Package Contents

```
FINAL-DEPLOYMENT/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── Dockerfile          # Docker configuration
│   └── requirements.txt    # Python dependencies
├── frontend/
│   └── index.html          # Web interface
├── docs/
│   └── [documentation]
├── docker-compose.yml      # Complete stack orchestration
├── .env.example           # Environment variables template
├── sample_data.csv        # Test data (11 participants)
└── README.md              # This file
```

---

## 🎯 Deployment Options

Choose ONE of these deployment methods:

### **Option 1: Docker (Recommended for Production)** ⭐
- Complete stack in containers
- Easy to deploy anywhere
- Includes database
- Production-ready

### **Option 2: Cloud Deploy (Easiest)**
- Backend: Render/Railway (free tier)
- Frontend: GitHub Pages (free)
- No Docker needed
- Good for demo/research

### **Option 3: Local Development**
- Test on your machine
- For development only
- Quick setup

---

# OPTION 1: DOCKER DEPLOYMENT

## Prerequisites

- Docker installed
- Docker Compose installed
- (Optional) Anthropic API key for LLM mode

---

## Step 1: Prepare Environment

```bash
# Clone/download this package
cd FINAL-DEPLOYMENT/

# Copy environment template
cp .env.example .env

# Edit .env and add your API key (optional)
nano .env

# Add this line (if you want LLM mode):
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
```

---

## Step 2: Build and Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

**Services will start:**
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:80 (if using nginx)

---

## Step 3: Test the System

### A. Test Health Endpoint

```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "llm_available": true,
  "version": "1.0.0",
  "database_connected": true
}
```

### B. Test Heuristic Mode

```bash
curl -X POST http://localhost:8000/generate_path \
  -H "Content-Type: application/json" \
  -d '{
    "current": [1,1,1,1,0,0,0,1,1,0,1,1],
    "target": [2,2,2,2,2,2,2,2,2,2,2,2],
    "mode": "heuristic",
    "participant_id": "TEST001",
    "participant_name": "Test User"
  }'
```

### C. Open Interactive Docs

```bash
open http://localhost:8000/docs
```

Try all endpoints directly in Swagger UI!

---

## Step 4: Access Frontend

### Option A: Use Local Nginx (included in docker-compose)

```
http://localhost
```

### Option B: Deploy to GitHub Pages

```bash
cd frontend/

# Update backend URL in index.html (line ~236)
# Change to your production backend URL

# Deploy
git init
git add index.html
git commit -m "Deploy frontend"
git remote add origin https://github.com/USERNAME/learning-path.git
git push -u origin main

# Enable GitHub Pages in repo settings
```

---

## Step 5: Production Deployment

### Deploy to Cloud with Docker

**Railway:**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
railway up
```

**Render:**
- Connect GitHub repo
- Select "Docker" deployment
- Set environment variables
- Deploy!

---

# OPTION 2: CLOUD DEPLOYMENT (NO DOCKER)

## Step 1: Deploy Backend to Render

1. **Go to** [render.com](https://render.com)

2. **New → Web Service**

3. **Connect your GitHub repository**

4. **Configure:**
   ```
   Name: learning-path-backend
   Region: Singapore / Oregon
   Branch: main
   Root Directory: backend/
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT
   Instance Type: Free
   ```

5. **Environment Variables:**
   ```
   ANTHROPIC_API_KEY = sk-ant-... (optional)
   ```

6. **Create Web Service**

7. **Get URL:** `https://learning-path-backend.onrender.com`

---

## Step 2: Deploy Frontend to GitHub Pages

1. **Create repository:** `learning-path-framework`

2. **Upload `frontend/index.html`**

3. **Update backend URL** in index.html:
   ```javascript
   let backendUrl = 'https://learning-path-backend.onrender.com';
   ```

4. **Enable GitHub Pages:**
   - Settings → Pages
   - Source: main / root
   - Save

5. **Access:** `https://USERNAME.github.io/learning-path-framework/`

---

# OPTION 3: LOCAL DEVELOPMENT

## Step 1: Backend

```bash
cd backend/

# Install dependencies
pip install -r requirements.txt

# Set API key (optional)
export ANTHROPIC_API_KEY="sk-ant-..."

# Run server
uvicorn app:app --reload --port 8000
```

**Access:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

## Step 2: Frontend

```bash
cd frontend/

# Serve with Python
python -m http.server 3000
```

**Access:** http://localhost:3000

**Update backend URL** in browser config section to: `http://localhost:8000`

---

# 🧪 TESTING

## 1. Backend API Tests

```bash
# Health check
curl http://localhost:8000/health

# List courses
curl http://localhost:8000/courses

# List phases
curl http://localhost:8000/phases

# Generate path (heuristic)
curl -X POST http://localhost:8000/generate_path \
  -H "Content-Type: application/json" \
  -d @test_request.json

# View history
curl http://localhost:8000/history?limit=5
```

## 2. Frontend Tests

1. Open frontend URL
2. Test backend connection
3. Upload `sample_data.csv`
4. Select participant
5. Try heuristic mode
6. (If API key set) Try LLM mode
7. Export PDF

---

# 📊 DATABASE

## SQLite Database Location

**Docker:** `/app/data/learning_paths.db` (mounted to `./data/`)

**Local:** `learning_paths.db` (in backend directory)

## View Database

```bash
# Docker
docker exec -it learning-path-backend sqlite3 /app/data/learning_paths.db

# Local
cd backend/
sqlite3 learning_paths.db

# Query
sqlite> SELECT * FROM learning_paths;
sqlite> .exit
```

---

# 🔧 DOCKER COMMANDS

## Basic Operations

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart service
docker-compose restart backend

# View logs
docker-compose logs -f backend

# Rebuild after code changes
docker-compose up --build -d

# Remove everything (including volumes)
docker-compose down -v
```

## Advanced

```bash
# Execute commands in container
docker exec -it learning-path-backend bash

# View database
docker exec -it learning-path-backend sqlite3 /app/data/learning_paths.db

# Check resource usage
docker stats learning-path-backend

# Export database
docker cp learning-path-backend:/app/data/learning_paths.db ./backup.db
```

---

# 🌐 PRODUCTION CHECKLIST

## Before Going Live

- [ ] Set `ANTHROPIC_API_KEY` environment variable
- [ ] Update CORS origins in `app.py` (line 28)
- [ ] Change frontend backend URL to production URL
- [ ] Test both heuristic and LLM modes
- [ ] Verify database persistence
- [ ] Test PDF export
- [ ] Set up SSL/HTTPS
- [ ] Configure domain (optional)
- [ ] Set up monitoring (optional)
- [ ] Enable backups for database

## Security

- [ ] Never commit `.env` with real API keys
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS in production
- [ ] Restrict CORS to your domain
- [ ] Add rate limiting (optional)
- [ ] Set up API key rotation (optional)

---

# 📈 MONITORING

## Health Checks

```bash
# Manual
curl http://localhost:8000/health

# Automated (add to cron)
*/5 * * * * curl -f http://your-backend/health || alert
```

## Docker Health

```bash
docker ps  # Check HEALTH status column
```

## Logs

```bash
# Real-time
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Specific service
docker-compose logs backend
```

---

# 🐛 TROUBLESHOOTING

## Backend Issues

**"LLM mode not available"**
```bash
# Check environment variable
docker exec learning-path-backend env | grep ANTHROPIC

# Set it
docker-compose down
# Edit .env
docker-compose up -d
```

**"Database locked"**
```bash
# Restart backend
docker-compose restart backend
```

**Port already in use**
```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Changed from 8000:8000
```

## Frontend Issues

**"Backend not reachable"**
- Check backend URL in config
- Verify CORS settings
- Check backend is running: `docker-compose ps`

**CSV upload fails**
- Verify file has 28 columns
- Check no missing values
- Ensure values are 0-3

## Docker Issues

**Build fails**
```bash
# Clean build
docker-compose down
docker system prune -a
docker-compose up --build
```

**Container exits immediately**
```bash
# Check logs
docker-compose logs backend

# Check for syntax errors
docker-compose config
```

---

# 📊 API ENDPOINTS

## Complete API Reference

### GET /
Root endpoint with API info

### GET /health
Health check + system status

### POST /generate_path
Generate learning path
- **Input:** current, target, mode, participant_id, participant_name
- **Output:** path, courses, metrics, saved_to_db

### GET /courses
List all available courses

### GET /phases
List all SDLC phases

### GET /history?limit=10
Get recent generated paths

### GET /docs
Interactive Swagger UI

### GET /redoc
ReDoc documentation

---

# 💰 COST ANALYSIS

## Free Tier Options

| Component | Platform | Cost | Limitations |
|-----------|----------|------|-------------|
| Backend | Render | $0 | Sleeps after 15min |
| Backend | Railway | $5 credit/mo | ~550 hours |
| Frontend | GitHub Pages | $0 | 100GB bandwidth |
| Database | SQLite | $0 | File-based |
| LLM API | Anthropic | Pay-per-use | ~$0.015/path |

## Estimated Monthly Costs

**Hobby Use (100 paths/month):**
- Hosting: $0 (free tiers)
- LLM API: $1.50
- **Total: $1.50/month**

**Production (1000 paths/month):**
- Hosting: $7 (Render paid tier)
- LLM API: $15
- **Total: $22/month**

---

# 📝 FOR RESEARCH PAPER

## URLs to Include

**API Documentation:**
```
https://your-backend.onrender.com/docs
```

**Live Demo:**
```
https://username.github.io/learning-path-framework/
```

**Repository:**
```
https://github.com/username/learning-path-framework
```

## Implementation Section

```latex
\subsection{Deployment Architecture}

The framework is deployed as a containerized FastAPI backend 
with a static frontend. The backend exposes RESTful endpoints 
for dual-mode Q-learning (heuristic and LLM-enhanced). Results 
are persisted in SQLite database for analytics. The system is 
deployed using Docker containers for reproducibility and 
scalability.

Interactive API documentation is available at /docs endpoint, 
enabling validation and testing by reviewers.
```

---

# ✅ QUICK START SUMMARY

## Fastest Path to Deployment

```bash
# 1. Download package
cd FINAL-DEPLOYMENT/

# 2. Start with Docker
docker-compose up -d

# 3. Test
curl http://localhost:8000/health

# 4. Access
open http://localhost:8000/docs

# 5. Deploy frontend
cd frontend/
# Upload to GitHub Pages

# Done! ✅
```

---

# 📞 SUPPORT

## Logs Location

- Docker: `docker-compose logs`
- Local: Terminal output

## Common URLs

- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Frontend: `http://localhost` or GitHub Pages URL
- Database: `./data/learning_paths.db`

---

**🎉 Ready to Deploy!**

Choose your deployment option and follow the steps above.
