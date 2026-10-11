"""Private beta validation and feedback privacy contract."""
from datetime import date
from pydantic import ValidationError
import pytest
from auth_routes import RegisterRequest
from beta_routes import FeedbackInput


def test_beta_invite_is_optional_outside_beta_mode():
    req = RegisterRequest(full_name="Adult Tester", email="adult@example.com",
                          password="test-password-long", date_of_birth=date(1990, 1, 1),
                          beta_invite="some-private-beta-code")
    assert req.beta_invite == "some-private-beta-code"


@pytest.mark.parametrize("category", ["bug", "usability", "content", "suggestion", "other"])
def test_feedback_categories(category):
    assert FeedbackInput(category=category, rating=5, message="Useful feedback message").category == category


@pytest.mark.parametrize("invalid", [
    {"category": "spam", "rating": 5, "message": "Useful feedback message"},
    {"category": "bug", "rating": 6, "message": "Useful feedback message"},
    {"category": "bug", "rating": 0, "message": "Useful feedback message"},
    {"category": "bug", "rating": 3, "message": "short"},
    {"category": "bug", "rating": 3, "message": "x" * 2001},
    {"category": "bug", "rating": 3, "message": "Useful feedback message", "user_id": 1},
])
def test_feedback_rejects_invalid_or_privilege_fields(invalid):
    with pytest.raises(ValidationError):
        FeedbackInput(**invalid)
