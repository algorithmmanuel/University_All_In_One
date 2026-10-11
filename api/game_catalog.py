"""Public game grouping. Each pathway supports multiple independent games."""
from mission_data import MISSIONS
from pathway_catalog import PATHWAYS

GAME_DEFINITIONS = (
    ("scholarship-detective", "secondary", "Scholarship Detective", "Email investigation", ("phishing-investigation",)),
    ("password-fortress", "secondary", "Password Fortress", "Account defense", ("password-fortress",)),
    ("midnight-alerts", "university", "Midnight Login Alerts", "SOC triage", ("soc-alert-triage",)),
    ("operation-firewall", "university", "Operation Firewall", "3D SOC investigation", ("operation-firewall",)),
    ("branch-resilience", "professional", "Branch Resilience", "Incident command", ("incident-response",)),
)

def game_catalog():
    games = []
    for game_id, pathway, title, mechanic, mission_ids in GAME_DEFINITIONS:
        if not all(m in MISSIONS for m in mission_ids):
            raise ValueError("Unknown mission in game catalog")
        games.append({
            "id": game_id, "pathway": pathway, "title": title,
            "mechanic": mechanic, "mission_ids": list(mission_ids),
            "difficulty": MISSIONS[mission_ids[0]]["difficulty"],
            "summary": MISSIONS[mission_ids[0]]["summary"],
            "mission_count": len(mission_ids),
        })
    return {"version": 1, "pathways": [p.id for p in PATHWAYS], "games": games}
