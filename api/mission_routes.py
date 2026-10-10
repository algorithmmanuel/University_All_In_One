"""Server-authoritative simulated missions with persistent user-specific runs."""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from auth import current_user
from database import SessionLocal
from mission_data import MISSIONS
from models import MissionRun, User

router = APIRouter(prefix="/api/v1/missions", tags=["missions"])

def get_db():
    with SessionLocal() as db:
        yield db

def require_student(user: User):
    if user.role != "student":
        raise HTTPException(status_code=403, detail="Student account required")

def get_run(db: Session, user: User, run_id: int) -> MissionRun:
    run = db.get(MissionRun, run_id)
    if run is None or run.user_id != user.id:
        raise HTTPException(status_code=404, detail="Mission run not found")
    return run

def public_step(step: dict) -> dict:
    return {k: step[k] for k in ("scene", "story", "evidence", "question")} | {
        "options": [o["text"] for o in step["options"]]}

def state(run: MissionRun):
    mission = MISSIONS[run.mission_id]
    complete = run.completed_at is not None
    return {"run_id": run.id, "mission_id": run.mission_id, "title": mission["title"],
            "step_index": run.step_index, "step_count": len(mission["steps"]),
            "score": run.score, "max_score": 15 * len(mission["steps"]),
            "completed": complete,
            "step": None if complete else public_step(mission["steps"][run.step_index]),
            "last_feedback": run.choices[-1]["feedback"] if run.choices else None}

@router.get("")
def catalog(user: User = Depends(current_user), db: Session = Depends(get_db)):
    require_student(user)
    runs = db.scalars(select(MissionRun).where(MissionRun.user_id == user.id)
                      .order_by(MissionRun.id.desc())).all()
    latest = {}
    for run in runs:
        if run.mission_id not in latest:
            latest[run.mission_id] = {"run_id": run.id, "score": run.score,
                "completed": run.completed_at is not None, "step_index": run.step_index}
    return {"missions": [
        {"id": key, "title": m["title"], "track": m["track"],
         "difficulty": m["difficulty"], "summary": m["summary"],
         "step_count": len(m["steps"]), "latest_run": latest.get(key)}
        for key,m in MISSIONS.items()]}

@router.post("/{mission_id}/start", status_code=201)
def start(mission_id: str, user: User = Depends(current_user), db: Session = Depends(get_db)):
    require_student(user)
    if mission_id not in MISSIONS:
        raise HTTPException(status_code=404, detail="Mission not found")
    run = MissionRun(user_id=user.id, mission_id=mission_id, step_index=0, score=0, choices=[])
    db.add(run)
    db.commit()
    db.refresh(run)
    return state(run)

@router.get("/runs/{run_id}")
def resume(run_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    require_student(user)
    return state(get_run(db, user, run_id))

class Decision(BaseModel):
    option_index: int
    expected_step: int
    finding_index: int | None = None

@router.post("/runs/{run_id}/decide")
def decide(run_id: int, body: Decision, user: User = Depends(current_user), db: Session = Depends(get_db)):
    require_student(user)
    run = get_run(db, user, run_id)
    steps = MISSIONS[run.mission_id]["steps"]
    if run.completed_at is not None:
        raise HTTPException(status_code=409, detail="Mission already completed")
    if body.expected_step != run.step_index:
        raise HTTPException(status_code=409, detail="Mission has advanced; refresh your progress")
    step = steps[run.step_index]
    if body.option_index < 0 or body.option_index >= len(step["options"]):
        raise HTTPException(status_code=422, detail="Invalid decision")
    if body.finding_index is not None and not 0 <= body.finding_index < len(step["evidence"]):
        raise HTTPException(status_code=422, detail="Invalid finding")
    # Finding score is calculated from a server-owned answer key, never from browser points.
    finding_key = {
        "phishing-investigation": [2, 1, 0],
        "soc-alert-triage": [1, 0, 0],
        "incident-response": [0, 0, 1],
    }
    correct_finding = finding_key[run.mission_id][run.step_index]
    investigation_points = 5 if body.finding_index == correct_finding else 0
    selected = step["options"][body.option_index]
    run.choices = [*run.choices, {"step": run.step_index, "option_index": body.option_index,
                                  "points": selected["points"] + investigation_points,
                                  "finding_index": body.finding_index,
                                  "investigation_points": investigation_points,
                                  "feedback": selected["feedback"] + (
                                      " Investigation finding: +5 points." if investigation_points else
                                      " Investigation finding: +0 points.")}]
    run.score += selected["points"] + investigation_points
    run.step_index += 1
    if run.step_index == len(steps):
        run.completed_at = datetime.now(timezone.utc)
    db.commit()
    return state(run)

@router.get("/history")
def history(user: User = Depends(current_user), db: Session = Depends(get_db)):
    require_student(user)
    runs = db.scalars(select(MissionRun).where(MissionRun.user_id == user.id)
                      .order_by(MissionRun.id.desc()).limit(50)).all()
    return {"runs": [{"id": r.id, "title": MISSIONS[r.mission_id]["title"],
                      "score": r.score, "max_score": len(MISSIONS[r.mission_id]["steps"]) * 15,
                      "completed": r.completed_at is not None,
                      "created_at": r.created_at.isoformat()} for r in runs if r.mission_id in MISSIONS]}
