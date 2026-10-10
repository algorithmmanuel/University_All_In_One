from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="EduCyber Nigeria API", version="0.1.0")
# Keep this restricted to the local web app during development.
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=False, allow_methods=["GET"], allow_headers=["*"])

ACADEMIES = [
    {"id": "secondary", "name": "Secondary School", "status": "preview"},
    {"id": "university", "name": "University", "status": "preview"},
    {"id": "cyber", "name": "Cybersecurity Academy", "status": "preview"},
]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/academies")
def list_academies():
    return {"academies": ACADEMIES}
