"""Public, versioned game discovery catalogue.

Catalog entries marked planned are not playable. Never imply a game is playable
until a validated mission exists for the same pathway.
"""
from mission_data import MISSIONS
from pathway_catalog import PATHWAYS

# Existing playable games retain their IDs and mission mappings.
PLAYABLE = (
    ("scholarship-detective", "secondary", "Scholarship Detective", "Email investigation", ("phishing-investigation",)),
    ("password-fortress", "secondary", "Password Fortress", "Account defense", ("password-fortress",)),
    ("privacy-patrol", "secondary", "Privacy Patrol", "Personal data safety", ("privacy-patrol",)),
    ("scam-spotter", "secondary", "Scam Spotter", "Online fraud awareness", ("scam-spotter",)),
    ("safe-social", "secondary", "Safe Social", "Social media safety", ("safe-social",)),
    ("device-defender", "secondary", "Device Defender", "Device security", ("device-defender",)),
    ("wifi-wise", "secondary", "Wi-Fi Wise", "Safe connectivity", ("wifi-wise",)),
    ("digital-footprints", "secondary", "Digital Footprints", "Digital citizenship", ("digital-footprints",)),
    ("mfa-guardian", "secondary", "MFA Guardian", "Authentication", ("mfa-guardian",)),
    ("backup-buddy", "secondary", "Backup Buddy", "Data resilience", ("backup-buddy",)),
    ("midnight-alerts", "university", "Midnight Login Alerts", "SOC triage", ("soc-alert-triage",)),
    ("operation-firewall", "university", "Operation Firewall", "3D SOC investigation", ("operation-firewall",)),
    ("branch-resilience", "professional", "Branch Resilience", "Incident command", ("incident-response",)),
)

# Roadmap entries are explicitly unavailable until independently tested missions ship.
PLANNED = {
    "university": (
        ("network-watch", "Network Watch", "Network monitoring"),
        ("web-defense", "Web Defense", "Web application security"),
        ("cloud-perimeter", "Cloud Perimeter", "Cloud configuration"),
        ("forensics-desk", "Forensics Desk", "Digital forensics"),
        ("malware-clues", "Malware Clues", "Malware analysis"),
        ("identity-lab", "Identity Lab", "Identity security"),
        ("secure-code-review", "Secure Code Review", "Secure development"),
        ("threat-hunter", "Threat Hunter", "Threat detection"),
    ),
    "professional": (
        ("risk-command", "Risk Command", "Risk governance"),
        ("zero-trust-briefing", "Zero Trust Briefing", "Architecture assurance"),
        ("cloud-incident", "Cloud Incident", "Cloud incident response"),
        ("supply-chain-watch", "Supply Chain Watch", "Third-party security"),
        ("ransomware-recovery", "Ransomware Recovery", "Business continuity"),
        ("identity-crisis", "Identity Crisis", "Privileged access"),
        ("boardroom-breach", "Boardroom Breach", "Executive crisis decisions"),
        ("ai-governance", "AI Governance", "AI risk management"),
        ("audit-trail", "Audit Trail", "Control assurance"),
    ),
}


def game_catalog():
    games = []
    pathway_ids = {path.id for path in PATHWAYS}
    for game_id, pathway, title, mechanic, mission_ids in PLAYABLE:
        if pathway not in pathway_ids or not mission_ids or not all(m in MISSIONS for m in mission_ids):
            raise ValueError("Invalid playable game mapping")
        games.append({
            "id": game_id, "pathway": pathway, "title": title,
            "mechanic": mechanic, "mission_ids": list(mission_ids),
            "difficulty": MISSIONS[mission_ids[0]]["difficulty"],
            "summary": MISSIONS[mission_ids[0]]["summary"],
            "mission_count": len(mission_ids), "status": "playable",
        })
    for pathway, entries in PLANNED.items():
        if pathway not in pathway_ids:
            raise ValueError("Unknown pathway in planned games")
        for game_id, title, mechanic in entries:
            games.append({
                "id": game_id, "pathway": pathway, "title": title,
                "mechanic": mechanic, "mission_ids": [],
                "difficulty": "Coming soon",
                "summary": f"A future defensive cybersecurity simulation covering {mechanic.lower()}.",
                "mission_count": 0, "status": "planned",
            })
    ids = [game["id"] for game in games]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate game ID")
    for pathway in pathway_ids:
        if sum(game["pathway"] == pathway for game in games) != 10:
            raise ValueError("Each pathway must contain exactly ten catalogue entries")
    return {"version": 3, "pathways": [p.id for p in PATHWAYS], "games": games}
