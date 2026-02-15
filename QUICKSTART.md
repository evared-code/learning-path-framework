# ⚡ QUICKSTART GUIDE

Get up and running in **5 minutes**!

---

## 🚀 Option 1: Docker (Fastest)

### Prerequisites
- Docker installed
- Docker Compose installed

### Steps

```bash
# 1. Navigate to folder
cd FINAL-DEPLOYMENT/

# 2. Start everything
docker-compose up -d

# 3. Wait 10 seconds for services to start
sleep 10

# 4. Test
./test.sh

# 5. Open browser
open http://localhost:8000/docs
```

**Done! ✅**

- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

## ☁️ Option 2: Cloud Deploy (Easiest)

### Backend → Render

1. Go to [render.com](https://render.com)
2. New → Web Service
3. Connect GitHub (upload files first)
4. Settings:
   - Root: `backend/`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - Free tier
5. Deploy!

Get URL: `https://your-app.onrender.com`

### Frontend → GitHub Pages

1. Create repo: `learning-path-framework`
2. Upload `frontend/index.html`
3. Update backend URL in HTML (line 236)
4. Settings → Pages → Enable
5. Access: `https://USERNAME.github.io/learning-path-framework/`

**Done! ✅**

---

## 💻 Option 3: Local (No Docker)

### Backend

```bash
cd backend/

# Install
pip install -r requirements.txt

# Run
uvicorn app:app --reload
```

### Frontend

```bash
cd frontend/

# Serve
python -m http.server 3000
```

**Access:**
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

**Done! ✅**

---

## 🧪 Testing

### Test Backend

```bash
# Health check
curl http://localhost:8000/health

# API Docs
open http://localhost:8000/docs
```

### Test Frontend

1. Open frontend URL
2. Set backend URL: `http://localhost:8000`
3. Click "Test Connection"
4. Upload `sample_data.csv`
5. Select participant
6. Generate path
7. Export PDF

---

## 🎯 Make Commands (Docker only)

```bash
make up       # Start services
make down     # Stop services
make logs     # View logs
make test     # Run tests
make db       # Open database
make backup   # Backup database
make clean    # Remove everything
```

---

## ❓ Troubleshooting

### Port 8000 already in use
```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"
```

### Backend not reachable
```bash
# Check status
docker-compose ps

# View logs
docker-compose logs backend

# Restart
docker-compose restart backend
```

### LLM mode not working
```bash
# Add API key to .env
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# Restart
docker-compose restart backend
```

---

## 📝 Next Steps

1. ✅ Get it running (choose option above)
2. ✅ Test with `sample_data.csv`
3. ✅ Try both modes (Heuristic + LLM)
4. ✅ Export PDF
5. ✅ Deploy to production (Render + GitHub Pages)
6. ✅ Update URLs in research paper
7. ✅ Submit! 🎉

---

## 🔗 Important URLs

**Local:**
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost or http://localhost:3000

**Production:**
- Backend: https://your-app.onrender.com
- Docs: https://your-app.onrender.com/docs
- Frontend: https://USERNAME.github.io/learning-path-framework/

---

**Need help?** Check `README.md` for complete documentation!
