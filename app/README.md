# MR Route Optimization

## Local setup

### Backend (PowerShell)

```powershell
cd app/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --port 8000
```

Set `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, and a development `JWT_SECRET` in `.env` before using database-backed endpoints.

### Frontend

```powershell
cd app/frontend
npm install
Copy-Item .env.example .env.local
npm run dev
```

Set `VITE_GOOGLE_MAPS_API_KEY` to a browser-restricted key for map rendering. The frontend uses `http://localhost:8000/api` by default.

## Database setup

Run these files in Supabase SQL Editor, in order:

1. `backend/scripts/schema.sql`
2. `backend/scripts/migration_v2.sql`
3. `backend/scripts/migration_v3.sql`
4. `python -m scripts.seed_data` from `app/backend`

The seed script uses synthetic Pune-area data and is safe to rerun for visit assignments.

## Verification

```powershell
cd app/backend
python -m unittest discover -s tests -v

cd ../frontend
npm run build
```

## Production checklist

- Set `ENVIRONMENT=production`.
- Set a strong, unique `JWT_SECRET`.
- Use the Supabase service key only on the backend.
- Set explicit production `CORS_ORIGINS`.
- Configure `VITE_GOOGLE_MAPS_API_KEY` with HTTP referrer restrictions.
- Run `/api/health` for liveness and `/api/ready` for database readiness.
- Do not use real patient data in the university demo dataset.
