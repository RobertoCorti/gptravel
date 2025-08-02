# 🚀 GPTravel Setup Guide - Full Stack AI Travel Planner

## 📋 Prerequisites

- **Python 3.9+** (but not 3.9.7)
- **Node.js 18+** and npm
- **Poetry** for Python dependency management
- **OpenAI API Key** for AI travel planning

## 🔧 Installation Steps

### 1. Clone and Setup Python Backend

```bash
# Install Poetry if you don't have it
curl -sSL https://install.python-poetry.org | python3 -

# Install all Python dependencies (including FastAPI)
poetry install

# Install spaCy model (required for NLP)
poetry run python -m spacy download en_core_web_md
```

### 2. Setup Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
```

### 3. Start the Application

#### Option A: Quick Start (Recommended)

```bash
# Terminal 1: Start Python Backend
python start_backend.py

# Terminal 2: Start Frontend (in frontend/ directory)
cd frontend
npm run dev
```

#### Option B: Manual Start

```bash
# Terminal 1: Python Backend
poetry run uvicorn backend_api:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Frontend (in frontend/ directory)
cd frontend
npm run dev
```

### 4. Access Your Application

- **Frontend**: http://localhost:3001 (or 3000)
- **Backend API**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs (Interactive Swagger UI)

## 🧪 Testing the Complete System

1. **Check Backend Status**: Look for green "AI Backend Online" indicator
2. **Fill the Travel Form**:
   - **OpenAI Key**: Your real `sk-...` API key
   - **Departure**: `New York, NY`
   - **Destination**: `Tokyo, Japan`
   - **Dates**: Any future date range
   - **Travel Reason**: Choose any option
3. **Submit**: Watch real AI generate your personalized travel plan! ✨

## 🏗️ Project Architecture

```
GPTravel/
├── backend_api.py              # FastAPI server (NEW)
├── start_backend.py            # Backend start script (NEW)
├── pyproject.toml              # Poetry dependencies (UPDATED)
├── src/gptravel/               # Your existing Python logic
│   ├── core/                   # Travel planning engine
│   ├── prototype/              # Streamlit app (legacy)
│   └── main.py
├── frontend/                   # Next.js frontend (NEW)
│   ├── src/
│   │   ├── app/                # Next.js App Router
│   │   ├── components/         # React components
│   │   ├── lib/               # Utilities and API client
│   │   └── types/             # TypeScript types
│   ├── package.json
│   └── tailwind.config.js
└── tests/                      # Your existing tests
```

## 🔍 Available Features

### 🤖 AI-Powered Planning
- **Real GPT-4 Integration**: Personalized travel itineraries
- **Smart Prompting**: Context-aware travel suggestions
- **Multiple Travel Styles**: Business, Romantic, Solo, Friends, Family

### 🎨 Modern UI/UX
- **Beautiful Interface**: Modern React components
- **Responsive Design**: Works on all devices
- **Real-time Status**: Backend health monitoring
- **Smart Error Handling**: Graceful fallbacks

### ⚡ Performance & Reliability
- **Fast APIs**: Efficient FastAPI backend
- **Token Optimization**: Distance-based OpenAI usage
- **Fallback System**: Works even if backend is offline
- **Type Safety**: Full TypeScript coverage

## 🛠️ Development Commands

### Python Backend
```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest

# Code formatting
poetry run black .
poetry run isort .

# Start development server
python start_backend.py
```

### Frontend
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run linting
npm run lint
```

## 🔧 Configuration

### Environment Variables

Create `.env` in project root:
```bash
OPENAI_API_KEY=your_key_here  # Optional: for backend testing
```

Create `frontend/.env.local`:
```bash
NEXT_PUBLIC_PYTHON_API_URL=http://127.0.0.1:8000
```

## 📚 API Documentation

Your FastAPI backend provides interactive documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

Available endpoints:
- `POST /api/travel` - Generate travel plan
- `POST /api/validate-location` - Validate locations
- `GET /health` - Health check

## 🔄 Migration from Streamlit

Your original Streamlit app is still available:
```bash
# Run legacy Streamlit app
poetry run streamlit run Home.py
```

But the new Next.js frontend offers:
- ✅ Better performance and UX
- ✅ Modern responsive design
- ✅ API-first architecture
- ✅ Production-ready deployment options

## 🚀 Deployment (Future)

### Frontend (Vercel)
```bash
cd frontend
npm run build
# Deploy to Vercel
```

### Backend (Railway/Heroku)
```bash
# Your FastAPI backend is ready for cloud deployment
# Just update CORS settings for production domain
```

## 🆘 Troubleshooting

### Common Issues

**Poetry not found**:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**FastAPI dependencies missing**:
```bash
poetry install
```

**Frontend won't start**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Backend connection failed**:
- Ensure Python backend is running on port 8000
- Check the green/yellow status indicator in the frontend

## 🎓 What You've Built

Congratulations! You've created a **production-ready, full-stack AI application** featuring:

- **Modern Frontend**: React + Next.js + TypeScript + Tailwind CSS
- **Python Backend**: FastAPI + Your existing travel planning logic
- **AI Integration**: Real OpenAI GPT-4 for personalized travel plans
- **Professional Architecture**: Separation of concerns, error handling, health monitoring

This is portfolio-worthy work that demonstrates full-stack development skills! 🏆 
