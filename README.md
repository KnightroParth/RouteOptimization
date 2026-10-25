# MR Route Optimization

**AI-Based Medical Representative Visit Prioritization & Route Optimization System**

An intelligent platform that uses **Random Forest ML** for doctor visit priority scoring and **Google OR-Tools VRPTW** for optimal route planning — built for pharmaceutical field operations.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + Vite)                   │
│  HashRouter SPA · Recharts · Leaflet · Lucide Icons         │
│  Deployed on Vercel                                         │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST API (axios)
┌──────────────────────▼──────────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  JWT Auth · 10 Route Modules · Pydantic Validation          │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │ ML Priority      │  │ VRPTW Route     │                   │
│  │ Engine (sklearn)  │  │ Optimizer       │                   │
│  │ RandomForest     │  │ (OR-Tools)      │                   │
│  └─────────────────┘  └─────────────────┘                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Supabase (PostgreSQL)                           │
│  users · doctors · visits · routes · route_stops             │
│  medical_representatives · priority_predictions              │
└─────────────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 19, Vite, Recharts, Leaflet, Lucide React |
| **Backend** | Python 3.12, FastAPI, Uvicorn |
| **ML** | scikit-learn (RandomForestClassifier), joblib, pandas |
| **Optimization** | Google OR-Tools (VRPTW solver) |
| **Database** | Supabase (PostgreSQL) |
| **Auth** | JWT (python-jose + bcrypt) |
| **Maps** | OpenRouteService (distance matrix), Google Maps |
| **Notifications** | WhatsApp Business API (sandbox) |

## Features

- **ML-Powered Priority Scoring** — Random Forest classifier trained on 6 features (visit recency, prescription volume, engagement, follow-up urgency, visit frequency, specialty alignment)
- **VRPTW Route Optimization** — OR-Tools vehicle routing with time windows, service durations, and capacity constraints
- **Role-Based Dashboards** — Separate MR and Manager views with real-time KPIs
- **Analytics Dashboard** — Priority distribution, visit trends, specialty coverage, territory performance
- **Staff Management** — Full CRUD for team members (Manager only)
- **WhatsApp Notifications** — Template-based visit reminders via sandbox API
- **Interactive Route Maps** — Leaflet-based visualization with stop sequencing

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Supabase project (with tables created via migration SQL)

### Backend Setup

```bash
cd app/backend

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Supabase credentials, JWT secret, etc.

# Train ML model (first time only)
python -m scripts.generate_training_data
python -m scripts.train_model

# Start development server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd app/frontend

# Install dependencies
npm install

# Start development server
npm run dev
# Opens at http://localhost:5173
```

### Environment Variables

Create a `.env` file in `app/backend/` with:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
JWT_SECRET=your-secure-random-secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=480
CORS_ORIGINS=http://localhost:5173
ORS_API_KEY=your-openrouteservice-key
```

## ML Pipeline

### Training

```bash
cd app/backend

# 1. Generate synthetic training data (3,000 records)
python -m scripts.generate_training_data

# 2. Train Random Forest model
python -m scripts.train_model
```

### Model Performance (Synthetic Data)

| Metric | Value |
|--------|-------|
| 5-Fold CV Accuracy | 73.25% ± 1.23% |
| Test Accuracy | 72.83% |
| Weighted Precision | 72.94% |
| Weighted Recall | 72.83% |
| Weighted F1 | 72.55% |

### Feature Importances

| Feature | Importance |
|---------|-----------|
| Days Since Last Visit | 40.1% |
| Prescription Volume | 18.5% |
| Engagement Score | 14.6% |
| Follow-Up Required | 11.3% |
| Visit Frequency | 8.9% |
| Specialty Alignment | 6.6% |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | User login (returns JWT) |
| POST | `/api/auth/register` | User registration |
| GET | `/api/doctors` | List all doctors |
| POST | `/api/doctors` | Create doctor |
| GET | `/api/visits` | List visits (filtered by MR) |
| POST | `/api/visits` | Create visit |
| POST | `/api/routes/generate` | Generate optimized route |
| GET | `/api/dashboard/mr` | MR dashboard stats |
| GET | `/api/dashboard/manager` | Manager dashboard stats |
| GET | `/api/ml/feature-importance` | ML model weights & metrics |
| POST | `/api/ml/run-batch` | Run batch inference |
| GET | `/api/analytics/overview` | Analytics charts data |
| GET | `/api/staff` | List staff (Manager only) |
| GET | `/api/health` | Health check |
| GET | `/api/ready` | Readiness check (DB connectivity) |

## Testing

```bash
cd app/backend

# Run all 32 backend tests
python -m unittest discover -s tests -v
```

## Project Structure

```
app/
├── backend/
│   ├── app/
│   │   ├── auth/          # JWT handler & dependencies
│   │   ├── ml/            # Trained model (.pkl) & metrics
│   │   ├── models/        # Pydantic schemas
│   │   ├── routes/        # 10 API route modules
│   │   ├── services/      # Priority engine, optimizer, distance
│   │   └── main.py        # FastAPI app + CORS + router registration
│   ├── scripts/           # Training data gen, model training, seeds
│   └── tests/             # 32 unit & contract tests
├── frontend/
│   ├── src/
│   │   ├── components/    # Sidebar, RouteMap, MobileNav
│   │   ├── context/       # AuthContext
│   │   ├── pages/         # 10 page components
│   │   ├── services/      # API client (axios)
│   │   └── App.jsx        # Router + lazy-loaded routes
│   └── vite.config.js
└── README.md
```

## License

This project is developed as an academic research project for AI-based pharmaceutical field operations optimization.
