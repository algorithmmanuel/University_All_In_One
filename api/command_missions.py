"""Nine fictional professional-level defensive decision simulations."""
from mission_data import step

COMMAND_MISSIONS = {
    "risk-command": {
        "title": "Risk Command", "track": "Risk governance",
        "difficulty": "Advanced", "summary": "Prioritize and treat technology risks at a fictional financial institution.",
        "steps": [
            step("Risk register", "An internet-facing service lacks a supported operating system.",
                 ["Critical service processes payments","Vendor support ended last quarter","Compensating controls are undocumented"], "What should the risk owner do?", [
                     ("Accept the risk without recording it", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Assess likelihood and impact, assign ownership and propose treatment", 10, "Correct. This decision preserves accountability, evidence and proportionality."),
                     ("Hide the unsupported asset", 0, "Reassess the control objective, evidence and accountable decision-maker.")
                 ]),
            step("Treatment plan", "The proposed remediation requires a six-week maintenance window.",
                 ["Exposure remains during the window","Temporary segmentation is feasible","Business owner can approve downtime"], "Which approach is defensible?", [
                     ("Approve time-bound compensating controls and a funded remediation plan", 10, "Correct. This decision preserves accountability, evidence and proportionality."),
                     ("Delay without controls", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Transfer accountability to the auditor", 0, "Reassess the control objective, evidence and accountable decision-maker.")
                 ]),
            step("Residual risk", "The remediation is complete but one exception remains.",
                 ["Patch evidence reviewed","Exception expires in 30 days","Risk committee requires residual-risk approval"], "How should the decision close?", [
                     ("Mark all risks eliminated", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Delete the exception record", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Document residual risk, accountable acceptance and expiry monitoring", 10, "Correct. This decision preserves accountability, evidence and proportionality.")
                 ]),
        ],
        "finding_key": [1,0,2],
    },
    "zero-trust-briefing": {
        "title": "Zero Trust Briefing", "track": "Architecture assurance",
        "difficulty": "Advanced", "summary": "Review identity, device and workload trust boundaries.",
        "steps": [
            step("Access design", "A privileged admin can access production from any unmanaged laptop.",
                 ["Privileged account exists","Device compliance not enforced","Conditional access available"], "What should the architect recommend?", [
                     ("Require strong authentication and compliant device posture", 10, "Correct. This decision preserves accountability, evidence and proportionality."),
                     ("Rely on office network location alone", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Share administrator passwords", 0, "Reassess the control objective, evidence and accountable decision-maker.")
                 ]),
            step("Service identity", "A workload uses a long-lived shared service secret.",
                 ["Secret is shared between services","No rotation record","Managed workload identity supported"], "What is the strongest design improvement?", [
                     ("Copy the secret to more systems", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Use scoped workload identities and rotate remaining secrets", 10, "Correct. This decision preserves accountability, evidence and proportionality."),
                     ("Disable service logs", 0, "Reassess the control objective, evidence and accountable decision-maker.")
                 ]),
            step("Policy validation", "A pilot policy blocks unmanaged devices but affects one approved emergency workflow.",
                 ["Pilot denies unmanaged devices","Emergency workflow needs documented exception","Audit events are available"], "What is a sound rollout decision?", [
                     ("Disable every policy", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Allow all devices permanently", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Create tightly controlled emergency access, test and monitor", 10, "Correct. This decision preserves accountability, evidence and proportionality.")
                 ]),
        ],
        "finding_key": [1,2,1],
    },
    "cloud-incident": {
        "title": "Cloud Incident", "track": "Cloud incident response",
        "difficulty": "Advanced", "summary": "Coordinate a fictional cloud credential compromise.",
        "steps": [
            step("Detection", "Cloud logs show API calls from an unfamiliar region using a service credential.",
                 ["Credential normally runs in one region","New API calls modify access rules","Cloud audit logs retained"], "What should incident command do first?", [
                     ("Validate activity and invoke approved credential containment", 10, "Correct. This decision preserves accountability, evidence and proportionality."),
                     ("Delete all cloud accounts", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Ignore until monthly review", 0, "Reassess the control objective, evidence and accountable decision-maker.")
                 ]),
            step("Containment", "The affected credential has permission to modify multiple storage resources.",
                 ["Credential scope is broad","Rotation can interrupt production","Temporary role restriction is available"], "Which containment balances risk and continuity?", [
                     ("Publish the secret to developers", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Restrict and rotate credentials under a coordinated response", 10, "Correct. This decision preserves accountability, evidence and proportionality."),
                     ("Stop collecting audit logs", 0, "Reassess the control objective, evidence and accountable decision-maker.")
                 ]),
            step("Recovery", "Credentials are rotated and the affected resources are identified.",
                 ["Access changes reviewed","Known-good infrastructure templates exist","Monitoring rules need updating"], "What should recovery include?", [
                     ("Restore unreviewed permissions", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Close without an incident report", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Reconcile configuration, validate access and improve detections", 10, "Correct. This decision preserves accountability, evidence and proportionality.")
                 ]),
        ],
        "finding_key": [1,0,2],
    },
    "supply-chain-watch": {
        "title": "Supply Chain Watch", "track": "Third-party security",
        "difficulty": "Advanced", "summary": "Assess a software supplier with privileged integration access.",
        "steps": [
            step("Vendor alert", "A vendor reports suspicious activity in its build environment.",
                 ["Vendor provides signed notification","Supplier deploys production updates","Software bill of materials exists"], "What should the customer organization do?", [
                     ("Assess exposure, freeze unverified releases and request evidence", 10, "Correct. This decision preserves accountability, evidence and proportionality."),
                     ("Ignore because the incident is external", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Disable all vendor oversight", 0, "Reassess the control objective, evidence and accountable decision-maker.")
                 ]),
            step("Artifact review", "A new supplier package has an unexpected digest.",
                 ["Expected digest differs","Signature validation is inconclusive","Previous approved package is available"], "Which action is appropriate?", [
                     ("Install to see whether it works", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Quarantine the package and verify provenance with the supplier", 10, "Correct. This decision preserves accountability, evidence and proportionality."),
                     ("Turn off signature checks", 0, "Reassess the control objective, evidence and accountable decision-maker.")
                 ]),
            step("Contract assurance", "The supplier has contained the issue and offers a corrective action plan.",
                 ["Root cause report received","Remediation milestones documented","Access privileges remain excessive"], "How should assurance conclude?", [
                     ("Accept verbal assurances only", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Remove supplier monitoring", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Track corrective actions and reduce unnecessary integration privileges", 10, "Correct. This decision preserves accountability, evidence and proportionality.")
                 ]),
        ],
        "finding_key": [1,0,2],
    },
    "ransomware-recovery": {
        "title": "Ransomware Recovery", "track": "Business continuity",
        "difficulty": "Advanced", "summary": "Lead a fictional bank's ransomware recovery and communications.",
        "steps": [
            step("Initial response", "Multiple branch endpoints display ransom notes while core banking remains online.",
                 ["Branch devices affected","Core banking status currently healthy","Network segmentation controls exist"], "What is the first command decision?", [
                     ("Activate incident response, isolate affected segments and preserve evidence", 10, "Correct. This decision preserves accountability, evidence and proportionality."),
                     ("Pay immediately without assessment", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Reimage every server", 0, "Reassess the control objective, evidence and accountable decision-maker.")
                 ]),
            step("Recovery prioritization", "Backups are available but restoration capacity is limited.",
                 ["Critical service RTO is four hours","Backup integrity test passed","Dependency map identifies authentication service"], "How should recovery be sequenced?", [
                     ("Restore random systems first", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Use BIA priorities and service dependencies to schedule restoration", 10, "Correct. This decision preserves accountability, evidence and proportionality."),
                     ("Ignore recovery objectives", 0, "Reassess the control objective, evidence and accountable decision-maker.")
                 ]),
            step("Executive update", "Some branches have resumed operations while investigation continues.",
                 ["Recovery validation documented","Residual exposure remains","Customers require accurate service updates"], "What should leadership communicate?", [
                     ("Declare the entire incident closed", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Publish unverified attribution", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Report confirmed impacts, recovery progress and remaining risks", 10, "Correct. This decision preserves accountability, evidence and proportionality.")
                 ]),
        ],
        "finding_key": [1,2,0],
    },
    "identity-crisis": {
        "title": "Identity Crisis", "track": "Privileged access",
        "difficulty": "Advanced", "summary": "Respond to suspected abuse of an enterprise administrator account.",
        "steps": [
            step("Privileged anomaly", "An administrator account makes unusual directory policy changes overnight.",
                 ["Change ticket absent","New privileged role assignment","Admin is currently unreachable"], "What should the responder do?", [
                     ("Validate events and initiate approved privileged-account containment", 10, "Correct. This decision preserves accountability, evidence and proportionality."),
                     ("Erase sign-in history", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Assume the activity is authorized", 0, "Reassess the control objective, evidence and accountable decision-maker.")
                 ]),
            step("Session control", "Investigation confirms an unauthorized privileged session.",
                 ["Active sessions detected","Break-glass account is separate","Session revocation supported"], "What is the safest containment?", [
                     ("Wait until the next audit", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Revoke unauthorized sessions, rotate credentials and preserve evidence", 10, "Correct. This decision preserves accountability, evidence and proportionality."),
                     ("Share break-glass credentials widely", 0, "Reassess the control objective, evidence and accountable decision-maker.")
                 ]),
            step("Control improvement", "The attacker used a legacy authentication exception.",
                 ["Legacy exception lacked expiry","Privileged MFA enforcement available","Review owner assigned"], "What prevents recurrence?", [
                     ("Allow permanent bypasses", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Disable audit logs", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Remove unnecessary exceptions and monitor privileged access", 10, "Correct. This decision preserves accountability, evidence and proportionality.")
                 ]),
        ],
        "finding_key": [1,0,1],
    },
    "boardroom-breach": {
        "title": "Boardroom Breach", "track": "Executive crisis decisions",
        "difficulty": "Advanced", "summary": "Present cyber incident decisions to a fictional board.",
        "steps": [
            step("First briefing", "A material service outage is suspected to involve a cyberattack.",
                 ["Impact assessment incomplete","Incident commander activated","Regulatory notification timelines may apply"], "What should the board request?", [
                     ("A verified situation report, ownership and time-bound next update", 10, "Correct. This decision preserves accountability, evidence and proportionality."),
                     ("An unsupported public attribution", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("A promise of zero financial impact", 0, "Reassess the control objective, evidence and accountable decision-maker.")
                 ]),
            step("Strategic trade-off", "Operations proposes reopening a service before containment is verified.",
                 ["Service is revenue critical","Security validation is incomplete","Temporary alternatives exist"], "What is the responsible decision?", [
                     ("Reopen immediately without review", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Use risk-based recovery gates and documented executive approval", 10, "Correct. This decision preserves accountability, evidence and proportionality."),
                     ("Hide the decision from stakeholders", 0, "Reassess the control objective, evidence and accountable decision-maker.")
                 ]),
            step("Disclosure governance", "The investigation confirms a reportable customer data incident.",
                 ["Legal notification assessment complete","Affected population estimated","Communications plan reviewed"], "What should the board oversee?", [
                     ("Delay all communications indefinitely", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Publish raw customer records", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Ensure timely accurate disclosures and remediation oversight", 10, "Correct. This decision preserves accountability, evidence and proportionality.")
                 ]),
        ],
        "finding_key": [0,1,2],
    },
    "ai-governance": {
        "title": "AI Governance", "track": "AI risk management",
        "difficulty": "Advanced", "summary": "Govern a fictional AI credit-assessment pilot.",
        "steps": [
            step("Model inventory", "A business unit deploys an AI scoring model without registering it.",
                 ["Model influences lending decisions","Training-data lineage incomplete","Model owner not assigned"], "What is the first governance action?", [
                     ("Register the use case, assign accountability and assess risk before scaling", 10, "Correct. This decision preserves accountability, evidence and proportionality."),
                     ("Expand immediately to all customers", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Remove audit records", 0, "Reassess the control objective, evidence and accountable decision-maker.")
                 ]),
            step("Bias assessment", "Validation shows different error rates across customer groups.",
                 ["Performance gap is measurable","Evaluation sample sizes differ","Human review exists"], "What should the AI risk team do?", [
                     ("Suppress subgroup metrics", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Investigate representativeness, fairness and impact with documented controls", 10, "Correct. This decision preserves accountability, evidence and proportionality."),
                     ("Assume overall accuracy is sufficient", 0, "Reassess the control objective, evidence and accountable decision-maker.")
                 ]),
            step("Monitoring", "The approved model's predictions drift after a market change.",
                 ["Input distributions shifted","Complaint rate increased","Rollback plan exists"], "What is an appropriate response?", [
                     ("Ignore until the annual review", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Remove human oversight", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Trigger drift review, protective thresholds and retraining approval", 10, "Correct. This decision preserves accountability, evidence and proportionality.")
                 ]),
        ],
        "finding_key": [1,0,1],
    },
    "audit-trail": {
        "title": "Audit Trail", "track": "Control assurance",
        "difficulty": "Advanced", "summary": "Plan and conclude a technology control audit using evidence.",
        "steps": [
            step("Audit planning", "An IT team reports that every critical change was approved.",
                 ["Change population contains 240 records","Approval evidence is incomplete","Risk-based sampling is available"], "What should the auditor do?", [
                     ("Define scope, obtain the full population and select evidence-based samples", 10, "Correct. This decision preserves accountability, evidence and proportionality."),
                     ("Accept the verbal statement", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Write the conclusion before testing", 0, "Reassess the control objective, evidence and accountable decision-maker.")
                 ]),
            step("Control testing", "A sampled production change has no independent approval.",
                 ["Deployment timestamp recorded","Approver field blank","Emergency change policy exists"], "How should the exception be evaluated?", [
                     ("Delete the sample", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Corroborate records, evaluate policy criteria and assess impact", 10, "Correct. This decision preserves accountability, evidence and proportionality."),
                     ("Assume fraud without further evidence", 0, "Reassess the control objective, evidence and accountable decision-maker.")
                 ]),
            step("Reporting", "Management provides a remediation plan for repeated change-control exceptions.",
                 ["Root cause identified","Owner and due date assigned","Retesting evidence not yet available"], "What is the correct audit conclusion?", [
                     ("Close immediately on promise alone", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Remove the finding", 0, "Reassess the control objective, evidence and accountable decision-maker."),
                     ("Report the validated gap and track remediation to verified closure", 10, "Correct. This decision preserves accountability, evidence and proportionality.")
                 ]),
        ],
        "finding_key": [1,0,2],
    },
}
