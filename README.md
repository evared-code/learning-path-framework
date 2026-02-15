# Q-Learning Framework for Cybersecurity Competency Development

A dual-mode personalized learning path recommendation system using Q-Learning algorithm with heuristic and LLM-enhanced Q-value estimation.

## 📋 Overview

This framework generates personalized cybersecurity training paths by analyzing current and target competency levels across 12 SDLC phases. It supports two Q-function modes:

- **Heuristic Mode**: Fast mathematical formula-based Q-value calculation
- **LLM-Enhanced Mode**: AI-powered Q-value estimation using Z.AI GLM models

## 🎯 Features

- **Dual Q-Function Modes**: Choose between fast heuristic or AI-powered estimation
- **12 SDLC Phases**: Requirements, Design, Development, Testing, Deployment, Maintenance, Process Planning, Team Coordination, Defect Management, Metrics, Configuration, Documentation
- **10 Cybersecurity Courses**: Curated from Coursera, Pluralsight, Udemy, SANS, and more
- **Competency Gap Analysis**: Automatic calculation and visualization
- **PDF Export**: Generate professional learning path reports
- **Z.AI Integration**: Support for 7 GLM models including free-tier options
- **Zero Cost Deployment**: Uses free tiers of Render and GitHub Pages

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Frontend  │ ──────> │    Backend   │ ──────> │   Z.AI API  │
│ (HTML/JS)   │         │  (FastAPI)   │         │ (Optional)  │
└─────────────┘         └──────────────┘         └─────────────┘
     │                         │
     │                         │
     v                         v
GitHub Pages              Render.com
```

## 🚀 Quick Start

### Prerequisites

- GitHub account
- Render account (free tier)
- Z.AI API key (optional, for LLM mode)

### Deployment

**1. Clone this repository**

```bash
git clone https://github.com/YOUR-USERNAME/learning-path-framework.git
cd learning-path-framework
```

**2. Deploy Backend to Render**

- Go to [render.com](https://render.com)
- Create new Web Service
- Connect this repository
- Configure:
  - **Root Directory**: `backend/`
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
  - **Instance Type**: Free

**3. Deploy Frontend to GitHub Pages**

- Go to repository Settings → Pages
- Source: Deploy from branch `main` / `root`
- Update `backendUrl` in `frontend/index.html` (line 368) with your Render URL

**4. Access your application**

```
https://YOUR-USERNAME.github.io/learning-path-framework/frontend/
```

For detailed deployment instructions, see [DEPLOYMENT_GUIDE_COMPLETE.md](DEPLOYMENT_GUIDE_COMPLETE.md)

## 📊 Usage

### 1. Select Q-Function Mode

Choose between **Heuristic** (no API key needed) or **LLM-Enhanced** (requires Z.AI API key).

### 2. Configure API Key (LLM Mode Only)

- Obtain API key from [z.ai/model-api](https://z.ai/model-api)
- Enter and validate your key
- Select GLM model (GLM-5 recommended)

### 3. Upload CSV Data

Your CSV file must contain 28 columns:

**Basic Information (4 columns):**
- `ParticipantID`, `Name`, `CurrentRole`, `TargetRole`

**Competency Levels (24 columns - 12 phases × 2):**
- `Req_Current`, `Req_Target`
- `Design_Current`, `Design_Target`
- `Dev_Current`, `Dev_Target`
- `Test_Current`, `Test_Target`
- `Deploy_Current`, `Deploy_Target`
- `Maint_Current`, `Maint_Target`
- `PSP_Current`, `PSP_Target`
- `TSP_Current`, `TSP_Target`
- `Defect_Current`, `Defect_Target`
- `Metric_Current`, `Metric_Target`
- `Config_Current`, `Config_Target`
- `Doc_Current`, `Doc_Target`

**Competency Scale**: 0 = None, 1 = Beginner, 2 = Intermediate, 3 = Advanced

[Download Sample CSV Template](https://github.com/YOUR-USERNAME/learning-path-framework/blob/main/sample_data.csv)

### 4. Generate Learning Path

- Select participant from table
- Click "Run Q-Learning Algorithm"
- View results and export to PDF

## 🔧 Technology Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: SQLite
- **AI Integration**: Z.AI GLM models (OpenAI-compatible API)
- **Deployment**: Render.com

### Frontend
- **Technologies**: HTML5, CSS3, Vanilla JavaScript
- **PDF Generation**: jsPDF + jsPDF-AutoTable
- **Deployment**: GitHub Pages

## 📁 Project Structure

```
learning-path-framework/
├── backend/
│   ├── app.py                 # FastAPI application
│   └── requirements.txt       # Python dependencies
├── frontend/
│   └── index.html            # Web interface
├── DEPLOYMENT_GUIDE_COMPLETE.md
├── sample_data.csv
└── README.md
```

## 🧮 Q-Learning Algorithm

### Heuristic Q-Function

```
Q(s, a) = 0.6 × Δ_gap + 0.3 × r_rel + 0.1 × r_diff
```

Where:
- `Δ_gap`: Gap reduction potential
- `r_rel`: Relevance to current needs
- `r_diff`: Difficulty appropriateness

### LLM-Enhanced Q-Function

Uses Z.AI GLM models to evaluate course value based on:
- Current competency levels
- Target competencies
- Course characteristics (difficulty, topics, impact)
- Contextual reasoning

## 🎓 Supported Z.AI Models

| Model | Description | Cost |
|-------|-------------|------|
| GLM-5 | Latest flagship | Paid |
| GLM-4.7 | High performance | Paid |
| GLM-4.5 | Balanced | Paid |
| GLM-4.5 Flash | Fast | **Free** |
| GLM-4.5 Air | Lightweight | **Free** |
| GLM-4.6V | Vision | Paid |
| GLM-4 | Stable | Paid |

## 📚 Course Catalog

The framework includes 10 curated cybersecurity courses:

1. **Secure Coding Fundamentals** (Coursera) - Beginner
2. **Threat Modeling for Developers** (Pluralsight) - Intermediate
3. **Security Testing & SAST/DAST** (Udemy) - Beginner
4. **Container & Cloud Security** (Linux Foundation) - Intermediate
5. **API Security Best Practices** (Pluralsight) - Intermediate
6. **DevSecOps & Security in Agile** (Scrum Alliance) - Beginner
7. **Advanced Web Application Security** (SANS) - Intermediate
8. **Vulnerability Management** (Cybrary) - Beginner
9. **Secure Architecture Design** (Coursera) - Advanced
10. **Security Metrics & Risk Management** (ISACA) - Intermediate

## 🔌 API Documentation

Once deployed, access interactive API documentation at:

```
https://your-backend.onrender.com/docs
```

### Key Endpoints

- `GET /health` - Health check and available models
- `POST /validate_key` - Validate Z.AI API key
- `POST /generate_path` - Generate learning path
- `GET /courses` - List all courses
- `GET /history` - View generation history

## 💰 Cost Breakdown

| Component | Service | Cost |
|-----------|---------|------|
| Backend | Render Free Tier | $0/month |
| Frontend | GitHub Pages | $0/month |
| Database | SQLite (file-based) | $0/month |
| LLM API (optional) | Z.AI Subscription | Variable* |

*LLM mode is optional. Heuristic mode is completely free.

Free-tier GLM models (4.5-flash, 4.5-air) are available for zero-cost LLM usage.

## 🧪 Testing

### Backend Health Check

```bash
curl https://your-backend.onrender.com/health
```

### Generate Path (Heuristic Mode)

```bash
curl -X POST https://your-backend.onrender.com/generate_path \
  -H "Content-Type: application/json" \
  -d '{
    "current": [1,1,1,1,0,0,0,1,1,0,1,1],
    "target": [2,2,2,2,2,2,2,2,2,2,2,2],
    "mode": "heuristic"
  }'
```

### Generate Path (LLM Mode)

```bash
curl -X POST https://your-backend.onrender.com/generate_path \
  -H "Content-Type: application/json" \
  -d '{
    "current": [1,1,1,1,0,0,0,1,1,0,1,1],
    "target": [2,2,2,2,2,2,2,2,2,2,2,2],
    "mode": "llm",
    "model_name": "glm-5",
    "zai_api_key": "YOUR_API_KEY"
  }'
```

## 🐛 Troubleshooting

### Backend Issues

**Problem**: Backend not responding  
**Solution**: 
- Check Render deployment status
- Verify logs in Render dashboard
- Confirm build succeeded

**Problem**: API key validation fails  
**Solution**:
- Verify API key is correct
- Check Z.AI subscription is active
- Try generating new API key

### Frontend Issues

**Problem**: Frontend shows old version  
**Solution**:
- Hard refresh (Ctrl+Shift+R)
- Clear browser cache
- Wait 2-3 minutes for GitHub Pages to update

**Problem**: CSV upload fails  
**Solution**:
- Verify all 28 columns are present
- Check column names match exactly
- Ensure competency values are 0-3
- Download and compare with sample template

## 📖 Documentation

- **[Complete Deployment Guide](DEPLOYMENT_GUIDE_COMPLETE.md)** - Step-by-step deployment instructions
- **[API Reference](https://your-backend.onrender.com/docs)** - Interactive API documentation
- **[Sample CSV Template](sample_data.csv)** - Example competency data

## 🤝 Contributing

This is an academic research project. For questions or collaboration inquiries, please open an issue.

## 📄 License

This project is developed for academic research purposes.

## 📧 Contact

For academic collaboration or questions:
- Open an issue in this repository
- Email: [your-email@university.edu]

## 🎓 Academic Citation

If you use this framework in your research, please cite:

```bibtex
@article{yourname2024qlearning,
  title={Q-Learning Framework for Personalized Cybersecurity Competency Development},
  author={Your Name},
  journal={Conference/Journal Name},
  year={2024}
}
```

## 🙏 Acknowledgments

- Z.AI for GLM model access
- Render for free backend hosting
- GitHub for free frontend hosting
- All cybersecurity training platform providers

## 📊 Project Statistics

![GitHub stars](https://img.shields.io/github/stars/YOUR-USERNAME/learning-path-framework)
![GitHub forks](https://img.shields.io/github/forks/YOUR-USERNAME/learning-path-framework)
![GitHub issues](https://img.shields.io/github/issues/YOUR-USERNAME/learning-path-framework)
![GitHub license](https://img.shields.io/github/license/YOUR-USERNAME/learning-path-framework)

---

**Developed for academic research in cybersecurity education and competency development.**

**Live Demo**: [https://your-username.github.io/learning-path-framework/frontend/](https://your-username.github.io/learning-path-framework/frontend/)

**API**: [https://your-backend.onrender.com](https://your-backend.onrender.com)
