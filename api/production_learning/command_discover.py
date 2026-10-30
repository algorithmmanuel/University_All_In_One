"""Original Cyber Command stage-one reading course. Publication is gated."""
COURSE = {
  "key": "command-discover-v1",
  "title": "Cyber Risk, Business Value & Decision-Making",
  "academy_id": "cyber",
  "pathway": "professional",
  "stage": "discover",
  "description": "Cyber Command, stage 1: eight substantial lessons on business impact, service dependencies, governance, controls, assurance and risk decisions.",
  "revision": "v1",
  "lessons": [
    {
      "position": 1,
      "title": "Cyber risk is a business decision",
      "content": "Learning focus\nCyber risk is the possibility that technology-related uncertainty prevents an organisation from meeting its objectives. Start with the essential service, affected stakeholders, business consequence and time horizon, not with a list of security tools. Confidentiality, integrity and availability represent different failure consequences; the most serious one depends on the business situation. A delayed payment, a changed ledger entry and a stolen customer record are not interchangeable outcomes. Risk statements should identify a credible event, cause and consequence.\n\nWorked example: A small lender depends on same-day repayment posting. A threat scenario involving corrupted transaction records could damage confidence and require lengthy reconciliation even when the application stays online.\n\nPractise and reflect: Write a risk statement naming an asset, event, vulnerability, business consequence and owner. Explain why a generic statement such as 'cyberattacks may occur' is hard to manage."
    },
    {
      "position": 2,
      "title": "Map critical services and dependencies",
      "content": "Learning focus\nAn organisation's critical services depend on people, providers, facilities, networks, identity systems, data, processes and recovery arrangements. A service diagram should show what customers receive and which systems make delivery possible. Dependencies outside the technology team matter as much as internal servers; a payment partner or electricity provider can affect outcomes without belonging to your organisation. Prioritisation improves when teams distinguish critical dependencies from convenient ones and verify assumptions with service owners.\n\nWorked example: A bank's online transaction channel appears to depend mainly on its mobile application. An exercise uncovers a shared identity provider and third-party switching service that are both essential to completing payments.\n\nPractise and reflect: For a fictional financial institution, trace an end-to-end customer transaction and identify three single points of failure and a way to validate each dependency."
    },
    {
      "position": 3,
      "title": "Decision rights and accountability",
      "content": "Learning focus\nPolicies, committees and security roles help only when decisions have named owners and workable authority. The board sets appetite and oversight expectations; executives fund and direct action; control owners operate safeguards; independent assurance evaluates evidence. A cybersecurity team can recommend urgent containment but may need business agreement when that action will interrupt critical services. Escalation rules should define when delay is unacceptable, what facts are needed and who accepts residual risk. Accountability should survive organisational changes.\n\nWorked example: During an incident, operations wants a database service online while security recommends isolation. A predefined escalation path helps leaders compare fraud risk, service impact and reversible alternatives instead of debating authority during the crisis.\n\nPractise and reflect: Draft a simple decision-rights matrix for a suspected payment compromise. Distinguish the person who recommends, approves, executes and independently reviews each action."
    },
    {
      "position": 4,
      "title": "Select controls for a stated objective",
      "content": "Learning focus\nControls are methods of changing risk, not achievements merely because they appear in an inventory. Preventive controls lower the likelihood of some events; detective controls make emerging harm visible; responsive and recovery controls reduce consequences. Design the control around a measurable objective, with a clear owner, reliable evidence and frequency. Two tools that fail in the same way are less resilient than independent safeguards. Control effectiveness must consider bypasses, maintenance and response readiness, not procurement status.\n\nWorked example: A firm reports that backups run nightly. Auditors ask whether restoration of the actual critical service has been tested, including identities, dependencies and transaction reconciliation. The backup schedule alone cannot answer the recovery question.\n\nPractise and reflect: Take a risk scenario and propose one preventive, one detective and one recovery control. Define a test that could show each control does not work as intended."
    },
    {
      "position": 5,
      "title": "Understand likelihood, impact and uncertainty",
      "content": "Learning focus\nRisk estimates are models of uncertain conditions, not precise predictions. Use transparent assumptions about affected assets, exposure, threat capability and plausible outcomes. Financial figures can help compare business alternatives but should not hide material customer, safety or legal consequences. Evidence may support a range rather than a single point estimate. Keep the confidence level visible and revisit estimates when architecture, incidents or supplier conditions change. Distinguish an organisation's risk appetite from an operational threshold that triggers escalation.\n\nWorked example: A cloud migration may reduce data-centre outage exposure while introducing concentration in a provider region. Leadership evaluates a range of possible service interruptions and recovery options instead of declaring cloud either safe or unsafe.\n\nPractise and reflect: Write two plausible impact scenarios with assumptions and uncertainties. Identify what additional evidence could materially change the priority."
    },
    {
      "position": 6,
      "title": "Translate incidents into executive choices",
      "content": "Learning focus\nAn executive incident brief should separate confirmed facts, working hypotheses, business impact, immediate decisions and next reporting time. Technical detail matters when it changes a decision; otherwise translate it into a service or customer consequence. Avoid premature certainty about attribution or the amount of data exposed. State whether actions are reversible, which services will be interrupted and what evidence will confirm recovery. A consistent briefing cadence prevents an information vacuum without encouraging invented updates.\n\nWorked example: The SOC detects unusual database access, but no verified exfiltration evidence is available. Leaders receive a short account of confirmed access indicators, containment alternatives and investigation gaps rather than an unqualified declaration of a data breach.\n\nPractise and reflect: Prepare a six-sentence update for executives: confirmed event, confidence, affected service, decision needed, risk of action and next evidence milestone."
    },
    {
      "position": 7,
      "title": "Assurance and the limits of green dashboards",
      "content": "Learning focus\nA green status indicator may mean a control was installed, an issue was closed or an assessment passed; none alone proves resilience under pressure. Assurance tests whether defined objectives are achieved under realistic conditions and whether evidence is complete enough to support conclusions. Mature reporting distinguishes design effectiveness from operating effectiveness, trends from snapshots and unresolved dependencies from assigned actions. Independent review should challenge management assumptions while preserving clear ownership for remediation.\n\nWorked example: A dashboard shows all disaster-recovery tasks completed. A reviewer discovers that application restoration was never tested after a network topology change. The meaningful follow-up is a service-level exercise and evidence of recovered operations, not merely a revised slide.\n\nPractise and reflect: Design three board-level indicators: a leading control measure, an outcome measure and a test-backed resilience measure. Explain how each could be gamed."
    },
    {
      "position": 8,
      "title": "Choose and communicate a defensible risk response",
      "content": "Learning focus\nRisk treatment choices include reducing exposure, changing a process, transferring some financial consequences, deliberately accepting residual risk or ending an activity. Each requires a documented reason, accountable approval and a means to revisit the choice. Treatment planning should consider practical sequencing and dependencies; a perfect long-term architecture cannot excuse unmanaged short-term exposure. Connect the plan to budget, milestones, operational checks and evidence. A good decision record explains why an alternative was not chosen.\n\nWorked example: After an external provider weakness is found, management weighs immediate isolation, compensating monitoring and a contract remediation timetable. The final record names the temporary controls, expiry date, escalation trigger and executive risk owner.\n\nPractise and reflect: Write a one-page risk decision explaining context, options, preferred action, owner, residual exposure and evidence for closure.\n\nFurther reading — editorial reference candidates (verify links before publication):\nNIST Cybersecurity Framework: https://www.nist.gov/cyberframework\nNIST Risk Management Framework: https://csrc.nist.gov/projects/risk-management\nCISA Cybersecurity Performance Goals: https://www.cisa.gov/cross-sector-cybersecurity-performance-goals"
    }
  ]
}
