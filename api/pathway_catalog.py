"""Versioned, cybersecurity-only pathway metadata. No database migration required."""
from typing import Literal
from pydantic import BaseModel, ConfigDict

Audience = Literal["secondary", "university", "professional"]

class Pathway(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: Audience
    title: str
    description: str
    learning_objectives: tuple[str, ...]
    sample_missions: tuple[str, ...]

PATHWAYS: tuple[Pathway, ...] = (
    Pathway(id="secondary", title="Cyber Explorers",
            description="Age-appropriate digital safety and defensive cybersecurity.",
            learning_objectives=("Recognize phishing", "Protect accounts", "Respect online privacy"),
            sample_missions=("phishing-investigation",)),
    Pathway(id="university", title="Cyber Academy",
            description="Applied foundations in networks, secure coding and incident investigation.",
            learning_objectives=("Analyze security alerts", "Correlate evidence", "Practice secure development"),
            sample_missions=("soc-alert-triage",)),
    Pathway(id="professional", title="Cyber Command",
            description="Cyber defense, incident command, governance and resilience simulations.",
            learning_objectives=("Prioritize incidents", "Coordinate containment", "Plan recovery"),
            sample_missions=("incident-response",)),
)

def pathway_catalog() -> dict:
    return {"version": 1, "domain": "cybersecurity", "pathways": [
        pathway.model_dump(mode="json") for pathway in PATHWAYS
    ]}
