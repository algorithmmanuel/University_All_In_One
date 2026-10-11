"""Private beta invites and learner-owned feedback. Never expose invite codes in logs."""
from datetime import datetime, timezone
from hashlib import sha256
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from auth import current_user
from db_dependencies import get_db
from models import BetaFeedback, User

router = APIRouter(prefix="/api/v1/beta", tags=["private-beta"])

class FeedbackInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    category: str = Field(pattern="^(bug|usability|content|suggestion|other)$")
    rating: int | None = Field(default=None, ge=1, le=5)
    message: str = Field(min_length=10, max_length=2000)
    page: str = Field(default="", max_length=160)


@router.post("/feedback", status_code=201)
def submit_feedback(body: FeedbackInput, user: User = Depends(current_user),
                    db: Session = Depends(get_db)):
    if user.role != "student":
        raise HTTPException(status_code=403, detail="Learner account required")
    if user.age_band != "adult":
        raise HTTPException(status_code=403, detail="Adult beta accounts only")
    feedback = BetaFeedback(user_id=user.id, category=body.category, rating=body.rating,
                            message=body.message.strip(), page=body.page.strip())
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return {"id": feedback.id, "message": "Feedback received. Thank you."}


@router.get("/feedback/mine")
def my_feedback(user: User = Depends(current_user), db: Session = Depends(get_db)):
    records = db.scalars(select(BetaFeedback).where(BetaFeedback.user_id == user.id)
                         .order_by(BetaFeedback.id.desc()).limit(30)).all()
    return {"feedback": [{"id": item.id, "category": item.category, "rating": item.rating,
                           "message": item.message, "page": item.page,
                           "created_at": item.created_at.isoformat()} for item in records]}
