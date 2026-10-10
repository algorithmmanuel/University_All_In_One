# EduCyber Nigeria — PostgreSQL with Docker Desktop (Windows)

## 1. Configure a local database password

From the repository root in PowerShell:

```powershell
Copy-Item .env.example .env
notepad .env
```

Replace the placeholder POSTGRES_PASSWORD with a strong, random local password. Do not commit .env. Avoid characters needing URL encoding for this first local setup (use a long alphanumeric password).

## 2. Start PostgreSQL

Ensure Docker Desktop is running:

```powershell
docker compose up -d postgres
docker compose ps
```

The database is reachable **only from the local machine** on port **5433**. The Docker volume persists data across restarts.

## 3. Install backend dependencies

In a second PowerShell terminal:

```powershell
cd api
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Set DATABASE_URL for the **current terminal** using the password you chose (replace YOUR_PASSWORD):

```powershell
$env:DATABASE_URL = "postgresql+psycopg://educyber:YOUR_PASSWORD@localhost:5433/educyber"
```

## 4. Apply migrations, then start FastAPI

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Check:
- http://localhost:8000/health/db → `{"database":"connected"}`
- http://localhost:8000/api/v1/academies → 3 academies
- http://localhost:8000/api/v1/courses → empty list until published courses are created
- http://localhost:3000 → API connected (with Next.js running)

## Notes

- Run Alembic migrations before starting the updated API.
- The API requires DATABASE_URL and will fail clearly if it is missing.
- This initial database schema is **not** a complete account system. Learner identifiers in the progress table are placeholders until authenticated users and ownership controls are implemented. No public progress-writing endpoints are provided.
- Do not use real student information during development.
- The default `/health` endpoint does not verify database connectivity; use `/health/db`.
- Avoid `docker compose down -v` unless you intentionally want to delete the database volume.
