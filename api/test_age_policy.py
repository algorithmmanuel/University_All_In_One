"""Safeguarding age boundaries and strict teacher registration."""
from datetime import date
import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from age_policy import age_band, age_on, registration_policy
from auth_routes import RegisterRequest


@pytest.mark.parametrize(("dob", "today", "expected"), [
    (date(2013, 10, 11), date(2026, 10, 11), "minor"),
    (date(2013, 10, 12), date(2026, 10, 11), "under_13"),
    (date(2008, 10, 11), date(2026, 10, 11), "adult"),
    (date(2008, 10, 12), date(2026, 10, 11), "minor"),
    (date(2000, 2, 29), date(2026, 2, 28), "adult"),
])
def test_age_boundaries(dob, today, expected):
    assert age_band(dob, today) == expected


def test_invalid_dates_rejected():
    for dob in (date(2027, 1, 1), date(1800, 1, 1)):
        with pytest.raises(HTTPException) as err:
            age_on(dob, date(2026, 10, 11))
        assert err.value.status_code == 422


def test_registration_policy():
    today = date(2026, 10, 11)
    with pytest.raises(HTTPException) as err:
        registration_policy(date(2015, 1, 1), "student", today)
    assert err.value.status_code == 403
    assert registration_policy(date(2010, 1, 1), "student", today) == ("minor", False)
    with pytest.raises(HTTPException):
        registration_policy(date(2010, 1, 1), "teacher", today)
    assert registration_policy(date(1990, 1, 1), "student", today) == ("adult", True)
    assert registration_policy(date(1990, 1, 1), "teacher", today) == ("adult", False)


def test_registration_requires_dob_and_forbids_extra_fields():
    base = {"full_name": "Test Learner", "email": "learner@example.invalid",
            "password": "a-long-test-password"}
    with pytest.raises(ValidationError):
        RegisterRequest(**base)
    with pytest.raises(ValidationError):
        RegisterRequest(**base, date_of_birth="2000-01-01", guardian_consent_verified=True)
    assert RegisterRequest(**base, date_of_birth="2000-01-01").date_of_birth == date(2000, 1, 1)
