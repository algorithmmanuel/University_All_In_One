"""Self-contained fictional training scenarios."""
def step(scene, story, evidence, question, options):
    return {"scene": scene, "story": story, "evidence": evidence,
            "question": question, "options": [
                {"text": label, "points": points, "feedback": feedback}
                for label, points, feedback in options]}

MISSIONS = {
    "phishing-investigation": {
        "title": "The Scholarship Email", "track": "Phishing investigation",
        "difficulty": "Beginner", "summary": "Investigate a suspicious scholarship notification.",
        "steps": [
            step("Inbox", "An unexpected scholarship email demands immediate verification.",
                 ["Unknown sender", "Urgent deadline", "Unfamiliar verification website"],
                 "What should you do first?", [
                    ("Verify through the school's official website", 10, "Correct. Verify independently."),
                    ("Follow the email link", 0, "Unverified links can be unsafe."),
                    ("Forward the link to friends", 0, "Avoid spreading suspicious links.")]),
            step("Evidence review", "The message asks for a portal password on an unfamiliar website.",
                 ["Password requested", "Unrelated website"],
                 "What is the strongest warning sign?", [
                    ("The email has a greeting", 0, "Greetings are not reliable evidence."),
                    ("An unrelated site requests a password", 10, "Correct. This is a major warning sign."),
                    ("The message is short", 0, "Length alone does not establish risk.")]),
            step("Response", "A classmate reports entering a password on the suspicious site.",
                 ["Potentially exposed account"], "What should they do?", [
                    ("Wait until next week", 0, "Prompt action is important."),
                    ("Contact the sender", 0, "The sender may not be trustworthy."),
                    ("Use the real portal to reset credentials, enable MFA and report", 10,
                     "Correct. Secure the account and report the incident.")])
        ]},
    "soc-alert-triage": {
        "title": "Midnight Login Alerts", "track": "SOC analyst",
        "difficulty": "Beginner", "summary": "Review a fictional privileged account alert.",
        "steps": [
            step("Alert queue", "Many unsuccessful sign-ins are followed by one successful privileged login.",
                 ["37 failed attempts", "One successful login"], "What is the right priority?", [
                    ("Dismiss the alert", 0, "The pattern warrants investigation."),
                    ("Investigate promptly", 10, "Correct. Validate the suspicious sign-in."),
                    ("Remove the audit records", 0, "Preserve security evidence.")]),
            step("Correlation", "The login came from an unfamiliar device.",
                 ["Unknown device", "Unexpected location"], "What should be checked?", [
                    ("Sign-in logs, device details and later activity", 10, "Correct. Correlate evidence."),
                    ("Only the user's job title", 0, "Job title cannot validate the event."),
                    ("Nothing further", 0, "The event remains unexplained.")]),
            step("Escalation", "Unusual administrative activity is confirmed.",
                 ["Suspicious privileged activity"], "What is the next step?", [
                    ("Ignore the finding", 0, "This may increase impact."),
                    ("Disable monitoring", 0, "Monitoring should remain available."),
                    ("Follow incident procedures and preserve evidence", 10, "Correct. Coordinate containment.")])
        ]},
    "incident-response": {
        "title": "Ransomware at the Branch", "track": "Incident response",
        "difficulty": "Beginner", "summary": "Manage a fictional branch disruption.",
        "steps": [
            step("Initial report", "A branch workstation displays a ransom demand.",
                 ["Files inaccessible", "Ransom message"], "What should happen first?", [
                    ("Isolate the affected workstation under the response plan", 10, "Correct. Limit potential spread."),
                    ("Continue using the workstation", 0, "This may worsen the incident."),
                    ("Ignore the report", 0, "Prompt response matters.")]),
            step("Scope", "Additional devices show unusual file changes.",
                 ["Possible spread", "Backups need protection"], "What is the priority?", [
                    ("Erase all records", 0, "Preserve evidence."),
                    ("Assess affected assets and safeguard backups", 10, "Correct. Protect recovery options."),
                    ("Ignore the backups", 0, "Recovery readiness is essential.")]),
            step("Recovery", "The incident is contained and a clean backup is validated.",
                 ["Containment verified", "Backup checked"], "What should the team do?", [
                    ("Reconnect everything without checks", 0, "Reinfection remains a concern."),
                    ("Skip communication", 0, "Keep stakeholders informed."),
                    ("Restore under the approved plan and monitor", 10, "Correct. Validate and monitor recovery.")])
        ]}
}
