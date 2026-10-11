from fastapi import Depends, FastAPI
from game_catalog import game_catalog
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Academy, Course
from auth_routes import router as auth_router
from learning_routes import router as learning_router
from quiz_routes import router as quiz_router
from mission_routes import router as mission_router
from pathway_routes import router as pathway_router
from mission_manifest_routes import router as mission_manifest_router

app = FastAPI(title="EduCyber Nigeria API", version="0.6.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Authorization", "Content-Type"])
app.include_router(auth_router)
app.include_router(learning_router)
app.include_router(quiz_router)
app.include_router(mission_router)
app.include_router(pathway_router)
app.include_router(mission_manifest_router)

def get_db():
    with SessionLocal() as session:
        yield session

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/db")
def database_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "connected"}

@app.get("/api/v1/academies")
def list_academies(db: Session = Depends(get_db)):
    rows = db.scalars(select(Academy).order_by(Academy.id)).all()
    return {"academies": [{"id": row.id, "name": row.name, "status": row.status} for row in rows]}

@app.get("/api/v1/courses")
def list_courses(academy_id: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Course).where(Course.status == "published")
    if academy_id:
        stmt = stmt.where(Course.academy_id == academy_id)
    rows = db.scalars(stmt.order_by(Course.id)).all()
    return {"courses": [{"id": row.id, "academy_id": row.academy_id, "title": row.title, "description": row.description} for row in rows]}

@app.get('/api/v1/games')
def list_games():
    return game_catalog()
