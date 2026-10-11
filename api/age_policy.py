"""Age-aware registration policy. DOB is self-declared, not verified identity."""
from datetime import date
from fastapi import HTTPException


def age_on(dob: date, today: date | None = None) -> int:
    today = today or date.today()
    if dob > today:
        raise HTTPException(status_code=422, detail="Date of birth cannot be in the future")
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if age > 120:
        raise HTTPException(status_code=422, detail="Enter a valid date of birth")
    return age


def age_band(dob: date, today: date | None = None) -> str:
    age = age_on(dob, today)
    if age < 13:
        return "under_13"
    if age < 18:
        return "minor"
    return "adult"


def registration_policy(dob: date, role: str, today: date | None = None) -> tuple[str, bool]:
    band = age_band(dob, today)
    if band == "under_13":
        # No child account or personal data stored until a real guardian flow exists.
        raise HTTPException(status_code=403, detail="Registration for children under 13 is not available yet")
    if role == "teacher" and band != "adult":
        raise HTTPException(status_code=403, detail="Teacher accounts require age 18 or older")
    # Minor accounts remain inactive pending a verified guardian/consent workflow.
    return band, band == "adult" and role == "student"
