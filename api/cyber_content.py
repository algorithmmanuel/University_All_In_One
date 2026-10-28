"""Original English cybersecurity learning/practice release, static and versioned.

Sources are references, not scraped text. Keep this revision available for saved
practice snapshots and study completion. No provider calls or model-generated runtime text.
"""
from pathlib import Path
REVISION = 'cyber-lab-v1'
SOURCES = {
    'nist': {'title': 'NIST Cybersecurity Framework', 'url': 'https://www.nist.gov/cyberframework', 'reviewed': '2026-10-28'},
    'owasp': {'title': 'OWASP Top 10', 'url': 'https://owasp.org/projects/top-ten', 'reviewed': '2026-10-28'},
    'mitre': {'title': 'MITRE ATT&CK', 'url': 'https://attack.mitre.org/', 'reviewed': '2026-10-28'},
}
# Each topic teaches the complete assessed concept set through its worked cases below.
TOPICS = {
 'fundamentals': ('Security goals and risk', 'nist', 'A service can be online while leaking data or accepting incorrect transactions. Separate confidentiality, integrity and availability when describing impact. Identify critical services and dependencies before prioritising controls. A threat can exploit a vulnerability; risk depends on context and potential consequences. Layered controls reduce different paths, and accountable owners must decide how to handle remaining risk.'),
 'phishing': ('Phishing and trusted verification', 'mitre', 'An urgent message can imitate a colleague or authority. Display names, good grammar and an encrypted connection do not establish the legitimacy of a request. Verify unexpected instructions through an independently known channel. Treat passwords, recovery codes and one-time codes as secrets. If exposed, report promptly and use official account controls. Handle suspicious files through approved processes, not by opening them on a work device.'),
 'identity': ('Identity and effective access', 'nist', 'Authentication establishes an identity; authorisation determines what that identity may do. MFA uses different categories of proof. Deny unexpected approvals and review activity. Unique passwords limit reuse risk. Least privilege, individual accounts and timely access changes help maintain accountable access as duties change. A changed password may leave sessions active; review supported revocation controls. Protect recovery routes alongside everyday sign-in.'),
 'network': ('Networks and containment tradeoffs', 'mitre', 'Sketch the systems and links needed for a business service. Narrow rules and segmentation reduce unnecessary communication and some spread paths. Isolation removes connectivity but also interrupts service and does not clean a device. Traffic timing, private addresses and familiar network names are clues rather than complete trust verdicts. Correlate source, destination, process and expected activity; authorise changes and plan rollback.'),
 'endpoint': ('Endpoint exposure and patching', 'mitre', 'Patching addresses known weaknesses in supported software. Plan changes for compatibility and availability; patching is not the same as removing existing compromise. Endpoint alerts, signature status and dashboard health provide bounded evidence. Validate behaviour, persistence and entry conditions. Limit unnecessary administrator access and remove unsupported software safely. Treat lost devices and unknown removable devices through approved response procedures.'),
 'application': ('Application controls and safe requests', 'owasp', 'Keep query structure separate from user values with parameterized queries. Validate input and object-level authority on the server even when browser controls exist. Render untrusted text safely for its context. Limit request sizes and keep secrets out of code and error messages. A blocked request proves only what happened on the observed path. Retried state-changing requests need stable command identities and server validation to prevent duplicate effects.'),
 'cloud': ('Cloud exposure and shared responsibility', 'nist', 'Cloud security responsibilities depend on the service model. Review effective identity and resource permissions, including inheritance, against intended access. Public access can expose encrypted-at-rest objects if the service returns decrypted contents. Scope credentials and remove unused access after dependency checks. Rotate exposed keys and investigate their usage. Preserve logs when repairing policies; new-region activity needs contextual validation rather than an automatic verdict.'),
 'response': ('Evidence-led incident response', 'mitre', 'Triage using plausible impact and evidence rather than alert labels alone. Correlate independent sign-in, endpoint and network records. Preserve originals and document clock offsets and transformations; correlation is not automatic causation. Containment limits exposure while investigation and eradication continue. Agree escalation roles, document decisions, distinguish facts from hypotheses, validate restored services and give after-action improvements owners and follow-up.'),
 'recovery': ('Backup assurance and recovery', 'nist', 'A backup job or replica is not proof of usable service recovery. Test restoration, application dependencies and access. RPO describes the targeted data-loss window; RTO describes targeted restoration time. Protect recovery copies and keys against common production failures and credential compromise. Checksums compare bytes but do not establish full recoverability. Resolve relevant entry conditions and validate restoration before reconnecting systems.'),
 'governance': ('Governance and control assurance', 'nist', 'A policy, tool count or closed ticket is not evidence that controls operated effectively. Test design and operation for the relevant scope and time. Assign risk owners, require scoped supplier evidence and govern exceptions with limits and review dates. Separate sensitive approvals from implementation where feasible. Minimise retained data, communicate confirmed impact and uncertainty, and verify that remediation changes the condition it was intended to fix.'),
}
MODULES = [
 {'id': 'protect', 'title': 'Protect the branch', 'topics': ['fundamentals', 'phishing', 'identity', 'endpoint'],
  'example': 'A caller asks a teller to approve an unexpected MFA prompt. Deny and report it, then review sessions through official controls. Installing MFA improves one entry path; it does not prove an already compromised workstation is clean.',
  'game': 'Use Strengthen sign-in before the stolen-password event; patch exposed assets and investigate existing activity separately.'},
 {'id': 'defend', 'title': 'Defend connected services', 'topics': ['network', 'application', 'cloud'],
  'example': 'An application alert appears while transaction service is healthy. Preserve the request and outcome records. Restrict only justified communication after checking dependencies; blocking everything may create an avoidable branch outage.',
  'game': 'Investigate and monitor assets. Segment the database path and compare the availability cost of isolating individual assets.'},
 {'id': 'recover', 'title': 'Respond, recover and assure', 'topics': ['response', 'recovery', 'governance'],
  'example': 'A backup dashboard is green but no restore has been attempted. A logical restore is useful evidence, yet full service recovery also needs working access, application dependencies, validated data and resolved entry conditions.',
  'game': 'Verify the recovery copy, isolate an affected asset, restore it, validate its condition and reconnect deliberately. Review the event timeline afterwards.'},
]


def load_bank():
    bank = []; topic = None
    for line in Path(__file__).with_name('content').joinpath('cyber_practice_v1.txt').read_text(encoding='utf-8').splitlines():
        if not line: continue
        if line.startswith('['): topic = line[1:-1]; continue
        prompt, correct, wrong1, wrong2, explanation = line.split('|')
        index = sum(q['topic'] == topic for q in bank) + 1
        position = (index - 1) % 3
        options = [wrong1, wrong2]; options.insert(position, correct)
        bank.append({'id': f'{topic}-{index:02}', 'revision': REVISION, 'topic': topic,
            'objective': topic + '-apply', 'difficulty': 'foundational' if index <= 4 else 'applied',
            'module': next(m['id'] for m in MODULES if topic in m['topics']),
            'prompt': prompt, 'options': options, 'answer': position,
            'explanation': explanation, 'source': SOURCES[TOPICS[topic][1]]})
    return bank

BANK = load_bank()


def lessons():
    return [{**module, 'revision': REVISION, 'sections': [{
        'id': topic, 'title': TOPICS[topic][0], 'objective': 'Apply ' + TOPICS[topic][0].lower() + ' to an evidence-based decision.',
        'body': TOPICS[topic][2], 'source': SOURCES[TOPICS[topic][1]],
        'worked_cases': [{'situation': q['prompt'], 'reasoning': q['explanation']} for q in BANK if q['topic'] == topic]
    } for topic in module['topics']]} for module in MODULES]
