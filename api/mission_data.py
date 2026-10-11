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

# Operation Firewall: synthetic bank SOC incident; no live systems or offensive actions.
MISSIONS["operation-firewall"] = {
    "title": "Operation Firewall",
    "track": "SOC investigation",
    "difficulty": "Intermediate",
    "summary": "Investigate a fictional bank identity alert, contain risk and document recovery.",
    "steps": [
        step("SOC command room",
             "At 02:14, a fictional bank monitoring console flags repeated failed logins followed by a successful privileged sign-in.",
             ["42 failed sign-ins in six minutes", "Successful privileged login at 02:14", "Routine nightly backup completed"],
             "What is the best first action?", [
                 ("Correlate sign-in events and verify with the account owner", 10, "Correct. Establish whether the sign-in is authorized while preserving evidence."),
                 ("Delete the alert as a false positive", 0, "The event has not yet been validated."),
                 ("Shut down every bank service", 0, "Unproven broad disruption is disproportionate.")]),
        step("Evidence terminal",
             "The sign-in used an unfamiliar device and accessed a privileged configuration screen.",
             ["Device is absent from approved inventory", "Office printer is online", "Privileged configuration was accessed"],
             "What should the analyst recommend?", [
                 ("Ignore the session because MFA was enabled", 0, "MFA alone does not establish the session is legitimate."),
                 ("Escalate and contain the suspect session under the response plan", 10, "Correct. Apply approved, proportionate containment."),
                 ("Disable audit logging", 0, "Security evidence must be retained.")]),
        step("Incident command desk",
             "The response team has revoked the suspect session and found no confirmed data extraction.",
             ["Session revocation confirmed", "Unverified rumor on social media", "No confirmed data exfiltration in available logs"],
             "What closes this stage responsibly?", [
                 ("Declare zero impact without further review", 0, "Absence of evidence is not proof of no impact."),
                 ("Publish unverified incident details", 0, "Communications must follow approved incident procedures."),
                 ("Document findings, monitor for recurrence and review affected controls", 10, "Correct. Complete evidence-based follow-up.")])
    ]
}

MISSIONS["password-fortress"] = {
    "title": "Password Fortress",
    "track": "Account safety",
    "difficulty": "Beginner",
    "summary": "Protect a fictional student account with unique passwords and safer sign-in choices.",
    "steps": [
        step("Password workshop",
             "You are creating a password for a new school account.",
             ["Password reuse increases risk", "Long unique passphrases are easier to remember", "Password managers can help"],
             "Which choice is safest?", [
                 ("Use a long unique passphrase", 10, "Correct. A unique passphrase is a strong choice."),
                 ("Reuse a password from another account", 0, "Password reuse increases risk."),
                 ("Use your birthday", 0, "Personal details are often predictable.")]),
        step("Second lock",
             "Your school offers additional sign-in protection.",
             ["Passwords are one authentication factor", "An authenticator provides another factor", "Unexpected approval prompts need caution"],
             "What should you do?", [
                 ("Approve every sign-in prompt", 0, "Only approve sign-ins you initiated."),
                 ("Enable MFA and reject unexpected prompts", 10, "Correct. MFA adds protection."),
                 ("Share verification codes", 0, "Keep verification codes private.")]),
        step("Account recovery",
             "An unfamiliar session appears in your school account.",
             ["Official account settings show active sessions", "Unknown sessions can be revoked", "Recovery settings should be reviewed"],
             "What is the safest response?", [
                 ("Ignore the session", 0, "Investigate unfamiliar sessions."),
                 ("Share your password with classmates", 0, "Never share credentials."),
                 ("Visit the official service and secure the account", 10, "Correct. Review sessions and account security.")])
    ]
}

# Imported after step and the legacy mission registry are defined.
from explorer_missions import EXPLORER_MISSIONS
MISSIONS.update(EXPLORER_MISSIONS)
