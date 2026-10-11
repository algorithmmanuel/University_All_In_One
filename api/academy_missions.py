"""Eight fictional university-level defensive investigations. No live targets."""
from mission_data import step

ACADEMY_MISSIONS = {
    "network-watch": {
        "title": "Network Watch", "track": "Network monitoring",
        "difficulty": "Intermediate", "summary": "Investigate anomalous traffic in a fictional campus network.",
        "steps": [
            step("Traffic baseline", "The campus firewall shows a sudden spike in outbound traffic from a lab computer.",
                 ["Normal outbound volume is 2 GB per hour","Current outbound volume is 24 GB per hour","A routine printer job completed"], "What should the analyst do first?", [
                     ("Disable the entire campus network", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Compare flows, destinations and the asset baseline", 10, "Correct. This action is proportionate, evidence-based and defensive."),
                     ("Delete the traffic records", 0, "Reconsider the evidence, scope and authorized defensive response.")
                 ]),
            step("Flow correlation", "NetFlow shows repeated connections to an unapproved external endpoint.",
                 ["Destination 203.0.113.45 is not on the approved list","The lab computer is managed","Connections recur every 30 seconds"], "What should be checked next?", [
                     ("Correlate endpoint activity and DNS with the flows", 10, "Correct. This action is proportionate, evidence-based and defensive."),
                     ("Assume the endpoint is safe", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Block all internet access indefinitely", 0, "Reconsider the evidence, scope and authorized defensive response.")
                 ]),
            step("Containment proposal", "Endpoint telemetry confirms an unauthorized process initiated the connections.",
                 ["Unauthorized process confirmed","Scope limited to one workstation so far","Evidence snapshots are available"], "What is the proportionate response?", [
                     ("Ignore because only one asset is affected", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Erase the logs immediately", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Isolate the affected host under the response plan and preserve evidence", 10, "Correct. This action is proportionate, evidence-based and defensive.")
                 ]),
        ],
        "finding_key": [1,2,0],
    },
    "web-defense": {
        "title": "Web Defense", "track": "Web application security",
        "difficulty": "Intermediate", "summary": "Assess suspicious web requests and recommend defensive fixes.",
        "steps": [
            step("Web gateway", "A simulated web app logs repeated requests containing unexpected SQL operators.",
                 ["Requests target a search parameter","WAF reports injection-like patterns","Normal search traffic continues"], "What is the best first response?", [
                     ("Review request logs and validate the application input handling", 10, "Correct. This action is proportionate, evidence-based and defensive."),
                     ("Publish the suspicious payloads to users", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Disable all logging", 0, "Reconsider the evidence, scope and authorized defensive response.")
                 ]),
            step("Code review", "The application builds a database query by concatenating untrusted input.",
                 ["Query uses string concatenation","Parameter binding is available","Application has a test environment"], "Which remediation is strongest?", [
                     ("Hide the search field", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Use parameterized queries and add regression tests", 10, "Correct. This action is proportionate, evidence-based and defensive."),
                     ("Rely only on a client-side warning", 0, "Reconsider the evidence, scope and authorized defensive response.")
                 ]),
            step("Verification", "The team deployed a fix to staging.",
                 ["Parameterized query confirmed","Security tests pass in staging","Production change approval is pending"], "What should happen before production release?", [
                     ("Bypass change control", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Declare all web risk eliminated", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Review test evidence, approve deployment and monitor", 10, "Correct. This action is proportionate, evidence-based and defensive.")
                 ]),
        ],
        "finding_key": [1,0,1],
    },
    "cloud-perimeter": {
        "title": "Cloud Perimeter", "track": "Cloud configuration",
        "difficulty": "Intermediate", "summary": "Review a fictional cloud storage exposure and its control failures.",
        "steps": [
            step("Cloud inventory", "A storage bucket containing student records appears publicly readable.",
                 ["Public access flag enabled","Dataset contains personal information","Bucket owner is identified"], "What is the priority?", [
                     ("Restrict public access through approved response and preserve access logs", 10, "Correct. This action is proportionate, evidence-based and defensive."),
                     ("Copy the records to another public bucket", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Wait for an external complaint", 0, "Reconsider the evidence, scope and authorized defensive response.")
                 ]),
            step("Policy inspector", "A policy grants wildcard read access to anonymous principals.",
                 ["Principal is wildcard","Read action applies broadly","Least privilege is required"], "What should the cloud team change?", [
                     ("Disable all monitoring", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Remove public grants and scope access to approved identities", 10, "Correct. This action is proportionate, evidence-based and defensive."),
                     ("Make the bucket publicly writable", 0, "Reconsider the evidence, scope and authorized defensive response.")
                 ]),
            step("Assurance", "The bucket is private again and access logs are retained.",
                 ["Exposure window identified","Access logs retained","Data access impact not yet established"], "How should the incident close?", [
                     ("Assume no data was accessed", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Delete audit trails", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Assess exposure impact, notify responsible teams and test preventive controls", 10, "Correct. This action is proportionate, evidence-based and defensive.")
                 ]),
        ],
        "finding_key": [1,0,2],
    },
    "forensics-desk": {
        "title": "Forensics Desk", "track": "Digital forensics",
        "difficulty": "Intermediate", "summary": "Preserve evidence and reconstruct a simulated workstation incident.",
        "steps": [
            step("Acquisition", "A workstation is suspected of unauthorized access.",
                 ["Device is powered on","Volatile evidence may be lost","Forensic process requires authorization"], "What should the investigator do?", [
                     ("Document the state and follow an approved acquisition procedure", 10, "Correct. This action is proportionate, evidence-based and defensive."),
                     ("Explore personal files without approval", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Reinstall the operating system immediately", 0, "Reconsider the evidence, scope and authorized defensive response.")
                 ]),
            step("Evidence handling", "Two analysts need to transfer a forensic image.",
                 ["Image hash is recorded","Chain-of-custody log exists","Original device is secured"], "How should integrity be protected?", [
                     ("Edit the original image", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Verify hashes and record each transfer", 10, "Correct. This action is proportionate, evidence-based and defensive."),
                     ("Share the image over an untracked channel", 0, "Reconsider the evidence, scope and authorized defensive response.")
                 ]),
            step("Timeline reconstruction", "Logs show suspicious access before the reported incident.",
                 ["System event at 10:04","Authentication event at 10:02","Clock offset documented"], "What is the sound conclusion?", [
                     ("Assume all timestamps are exact", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Delete conflicting records", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Normalize timestamps and correlate independent evidence", 10, "Correct. This action is proportionate, evidence-based and defensive.")
                 ]),
        ],
        "finding_key": [1,0,2],
    },
    "malware-clues": {
        "title": "Malware Clues", "track": "Malware analysis",
        "difficulty": "Intermediate", "summary": "Triage fictional malware indicators without executing unknown files.",
        "steps": [
            step("File intake", "A suspicious executable is received for authorized analysis.",
                 ["File source is untrusted","SHA-256 hash can be calculated","Isolated analysis environment exists"], "What is the safest first action?", [
                     ("Hash and quarantine the sample under lab procedures", 10, "Correct. This action is proportionate, evidence-based and defensive."),
                     ("Run it on a production workstation", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Email the sample to classmates", 0, "Reconsider the evidence, scope and authorized defensive response.")
                 ]),
            step("Static clues", "Static analysis finds an unusual persistence reference.",
                 ["Startup registry reference","Executable is unsigned","Known-good software inventory exists"], "What should the analyst do?", [
                     ("Assume all unsigned files are malicious", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Correlate the indicators with trusted telemetry", 10, "Correct. This action is proportionate, evidence-based and defensive."),
                     ("Disable endpoint monitoring", 0, "Reconsider the evidence, scope and authorized defensive response.")
                 ]),
            step("Detection update", "The response team confirms malicious behavior in an isolated lab.",
                 ["Observed behavior documented","Indicators validated","Detection rule can be tested"], "What is the next defensive step?", [
                     ("Publish the executable for unrestricted use", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Erase analysis notes", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Test and deploy detection updates under change control", 10, "Correct. This action is proportionate, evidence-based and defensive.")
                 ]),
        ],
        "finding_key": [0,0,1],
    },
    "identity-lab": {
        "title": "Identity Lab", "track": "Identity security",
        "difficulty": "Intermediate", "summary": "Investigate excessive privileges and suspicious authentication.",
        "steps": [
            step("Access review", "A former contractor retains an active privileged role.",
                 ["Contract ended last month","Privileged role remains assigned","Access review is overdue"], "What should happen?", [
                     ("Revoke unnecessary access through the approved process and investigate usage", 10, "Correct. This action is proportionate, evidence-based and defensive."),
                     ("Leave the role active indefinitely", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Share the credentials with the team", 0, "Reconsider the evidence, scope and authorized defensive response.")
                 ]),
            step("Conditional access", "A privileged login bypasses an expected MFA requirement.",
                 ["Policy exclusion matches the account","Sign-in is from an unfamiliar device","Access policy change was not approved"], "What should be reviewed?", [
                     ("Disable sign-in auditing", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Investigate the exclusion and enforce approved MFA policy", 10, "Correct. This action is proportionate, evidence-based and defensive."),
                     ("Approve every pending login", 0, "Reconsider the evidence, scope and authorized defensive response.")
                 ]),
            step("Governance", "The role has been removed and the policy corrected.",
                 ["Role owner identified","Access review frequency documented","Exception approvals require tracking"], "What prevents recurrence?", [
                     ("Rely on informal verbal approvals", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Remove periodic reviews", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Automate joiner-mover-leaver reviews and monitor exceptions", 10, "Correct. This action is proportionate, evidence-based and defensive.")
                 ]),
        ],
        "finding_key": [1,0,1],
    },
    "secure-code-review": {
        "title": "Secure Code Review", "track": "Secure development",
        "difficulty": "Intermediate", "summary": "Review a fictional CI pipeline for security and release integrity.",
        "steps": [
            step("Repository review", "A developer accidentally committed an API credential to source control.",
                 ["Credential visible in commit history","Secret scanning raised an alert","Credential may remain valid"], "What is the best response?", [
                     ("Revoke and rotate the credential, investigate exposure and remove it safely", 10, "Correct. This action is proportionate, evidence-based and defensive."),
                     ("Hide the alert", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Only delete the latest line of code", 0, "Reconsider the evidence, scope and authorized defensive response.")
                 ]),
            step("Pipeline gate", "A CI workflow allows security scanner failures to be ignored.",
                 ["Scanner configured to continue on error","Release pipeline still succeeds","Blocking gate is required by policy"], "What is the best control improvement?", [
                     ("Disable all scans", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Enforce policy-based blocking and handle exceptions through approval", 10, "Correct. This action is proportionate, evidence-based and defensive."),
                     ("Trust successful builds as proof of security", 0, "Reconsider the evidence, scope and authorized defensive response.")
                 ]),
            step("Artifact integrity", "The release uses a mutable image tag after verification.",
                 ["Validated digest is available","Deployment references latest tag","Image signing is configured"], "How can release integrity improve?", [
                     ("Remove signatures", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Disable artifact retention", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Deploy the validated immutable digest and verify attestations", 10, "Correct. This action is proportionate, evidence-based and defensive.")
                 ]),
        ],
        "finding_key": [0,0,1],
    },
    "threat-hunter": {
        "title": "Threat Hunter", "track": "Threat detection",
        "difficulty": "Intermediate", "summary": "Build and validate a defensive hunt hypothesis using simulated telemetry.",
        "steps": [
            step("Hypothesis", "Multiple endpoints show periodic DNS requests to a new domain.",
                 ["DNS queries repeat every minute","Domain was registered recently","Traffic spans three managed endpoints"], "What should the hunter do?", [
                     ("Form a testable hypothesis and correlate DNS with endpoint events", 10, "Correct. This action is proportionate, evidence-based and defensive."),
                     ("Declare a breach immediately", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Delete all DNS logs", 0, "Reconsider the evidence, scope and authorized defensive response.")
                 ]),
            step("Hunt pivot", "Process telemetry links the requests to an unfamiliar scheduled task.",
                 ["Task created shortly before first DNS query","Task runs under a service account","Endpoint inventory has no matching software"], "What is the next step?", [
                     ("Ignore the task because it is scheduled", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Validate task provenance and inspect related host activity", 10, "Correct. This action is proportionate, evidence-based and defensive."),
                     ("Run the unknown task on a live server", 0, "Reconsider the evidence, scope and authorized defensive response.")
                 ]),
            step("Hunt outcome", "The task is confirmed unauthorized and the affected hosts are identified.",
                 ["Three hosts affected","Evidence preserved","Containment owners assigned"], "What should the team do?", [
                     ("Stop hunting without documenting", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Disable telemetry", 0, "Reconsider the evidence, scope and authorized defensive response."),
                     ("Escalate, contain under the response plan and convert findings into detections", 10, "Correct. This action is proportionate, evidence-based and defensive.")
                 ]),
        ],
        "finding_key": [0,0,0],
    },
}
