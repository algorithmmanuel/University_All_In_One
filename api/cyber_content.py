"""Original English cybersecurity learning/practice release, static and versioned.

Sources are references, not scraped text. Keep this revision available for saved
practice snapshots and study completion. No provider calls or model-generated runtime text.
"""
from pathlib import Path
from cyber_curriculum_v3 import supplements, app_source
LEGACY_REVISION = 'cyber-lab-v1'
BUILD_B_REVISION = 'cyber-lab-v2'
REVISION = 'cyber-lab-v3'
SOURCES = {
    'nist': {'title': 'NIST Cybersecurity Framework', 'url': 'https://www.nist.gov/cyberframework', 'reviewed': '2026-10-28'},
    'owasp': {'title': 'OWASP Top 10', 'url': 'https://owasp.org/projects/top-ten', 'reviewed': '2026-10-28'},
    'mitre': {'title': 'MITRE ATT&CK', 'url': 'https://attack.mitre.org/', 'reviewed': '2026-10-28'},
}
# Public reference sections for the new edition; original question sources remain frozen.
READINGS = {
 'phishing': ('MITRE ATT&CK: Phishing (T1566)', 'https://attack.mitre.org/techniques/T1566/'),
 'identity': ('OWASP Authentication Cheat Sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html'),
 'network': ('MITRE ATT&CK: Network Segmentation (M1030)', 'https://attack.mitre.org/mitigations/M1030/'),
 'endpoint': ('MITRE ATT&CK: Update Software (M1051)', 'https://attack.mitre.org/mitigations/M1051/'),
 'application': ('OWASP Authorization Cheat Sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html'),
 'cloud': ('NIST SP 800-144: public-cloud security and privacy considerations (2011)', 'https://csrc.nist.gov/pubs/sp/800/144/final'),
 'response': ('NIST SP 800-61 Rev. 3: Incident Response (2025)', 'https://csrc.nist.gov/pubs/sp/800/61/r3/final'),
 'recovery': ('NIST SP 800-34 Rev. 1: Contingency Planning (2010)', 'https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final'),
}
EXTENSIONS = {
 'fundamentals': 'Consider two redundant branch servers that share one identity provider. The server count suggests resilience, but a failed shared dependency can still stop both. Map the service path, set measurable targets and test the whole dependency chain. State the assumptions and scope of each conclusion. A laboratory test and a production control test support different claims.',
 'phishing': 'A real colleague account can be compromised and an expected invoice can carry substituted payment details. Verify consequential changes through established independent channels even when the business context looks plausible. Encourage prompt reporting without blame. Receipt, opening an attachment, submitting credentials and session exposure are different events; response should follow evidence of what actually happened.',
 'identity': 'In Supplier Access Crisis, staff MFA does not revoke the supplier service credential. Inventory non-human identities and their owners, scopes and expiry conditions. Removing one role may leave group-based access or delegated application permissions. Rotation must invalidate the obsolete credential, and disabling an account may require separate verification of sessions. Review effective access rather than one reassuring control label.',
 'network': 'Compare the intended network diagram with actual permitted paths. One restrictive rule can be bypassed by another route. Isolating the identity service can interrupt other applications, so containment needs a dependency-aware decision and rollback plan. DNSSEC addresses origin authentication and integrity of signed DNS data; it does not encrypt all application traffic or establish that a business request is legitimate.',
 'endpoint': 'Patching a compromised device closes a modeled weakness without proving a trusted operating state. Preserve relevant records, assess persistence and exposed credentials, then validate recovery. A signed binary, known hash or healthy dashboard is one evidence input with limits. Requested remote wipe, requested agent installation and confirmed execution/effectiveness are separate states.',
 'application': 'A game retry after a lost response must reuse its original command identity. A conflicting reuse is rejected, while an identical retry cannot spend credits twice. Transactions and version checks protect concurrent state changes. Keep practice question/options snapshots fixed so later authoring cannot change what an earlier learner is graded against. Enforce ownership on every object request and avoid secrets in logs.',
 'cloud': 'Review effective cloud access across identity, resource and inherited policies. Production and backup permissions controlled by the same powerful identity can create a shared recovery failure path. A provider health report does not validate customer configuration. The linked 2011 NIST publication supplies general outsourcing/security considerations, not current provider-specific setup instructions; validate actual service controls against current official documentation.',
 'response': 'Supplier credential revocation closes future entry but does not remove compromise already present. Coordinate containment, evidence collection and restoration under an incident decision authority. Keep confirmed facts separate from hypotheses and record what was known when each decision was made. Verify that requested actions executed and achieved their intended effects. A final report may truthfully retain unresolved questions.',
 'recovery': 'Recovery Under Pressure begins with encrypted services: disconnection alone cannot restore availability. Contain affected assets, verify a recovery source, restore isolated systems, validate and reconnect deliberately. Include identities, keys, application dependencies, people and runbooks in recovery tests. Report component and service-level results separately. The linked NIST planning guide is an older reference for concepts, not a claim of compliance or a vendor runbook.',
 'governance': 'A closed remediation ticket, training completion or policy document does not establish the corresponding outcome. Match evidence to scope, time and objective. Record sample limitations, supplier report scope, exception expiry and cross-team responsibilities. AI or multiplayer expansion should follow demonstrated value, dependable operation and relevant data/safety/cost evaluation rather than a feature-count target.',
}


def further_reading(topic):
    title, url = READINGS.get(topic, (SOURCES['nist']['title'], SOURCES['nist']['url']))
    return {'title': title, 'url': url, 'reviewed': '2026-10-28'}

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


def _difficulty(index, revision):
    """Keep old labels fixed; v3 adds 16/4/5 items to each 4/16/5 topic pool."""
    if revision == REVISION:
        if index <= 41: return 'foundational'
        return 'applied' if index <= 45 else 'challenging'
    if index <= 4: return 'foundational'
    return 'challenging' if index >= 21 else 'applied'


def _source(topic, index, revision):
    """Source metadata is part of a question edition, not the current module edition."""
    if revision == REVISION:
        if topic == 'application': return app_source(index)
        return {**further_reading(topic), 'reviewed': '2026-10-29'}
    if revision == BUILD_B_REVISION: return further_reading(topic)
    return SOURCES[TOPICS[topic][1]]


def _load_file(filename, revision, offset=0):
    bank = []
    counts = {}
    topic = None
    path = Path(__file__).with_name('content').joinpath(filename)
    for line_number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not line: continue
        if line.startswith('['):
            topic = line[1:-1]
            if topic not in TOPICS: raise ValueError(f'{filename}:{line_number}: unknown topic')
            continue
        fields = line.split('|')
        if topic is None or len(fields) != 5 or not all(field.strip() for field in fields):
            raise ValueError(f'{filename}:{line_number}: invalid question record')
        prompt, correct, wrong1, wrong2, explanation = fields
        if len({correct, wrong1, wrong2}) != 3:
            raise ValueError(f'{filename}:{line_number}: repeated option')
        counts[topic] = counts.get(topic, 0) + 1
        index = counts[topic] + offset
        position = (index - 1) % 3
        options = [wrong1, wrong2]
        options.insert(position, correct)
        objective = f'{topic}-decision-{index:02}' if revision == REVISION else topic + '-apply'
        bank.append({'id': f'{topic}-{index:02}', 'revision': revision, 'topic': topic,
            'objective': objective, 'difficulty': _difficulty(index, revision),
            'module': next(m['id'] for m in MODULES if topic in m['topics']),
            'prompt': prompt, 'options': options, 'answer': position,
            'explanation': explanation, 'source': _source(topic, index, revision)})
    return bank

def load_bank():
    return (_load_file('cyber_practice_v1.txt', LEGACY_REVISION)
            + _load_file('cyber_practice_v2.txt', BUILD_B_REVISION, offset=10)
            + _load_file('cyber_practice_v3.txt', REVISION, offset=25))

BANK = load_bank()
for question in BANK:
    if question['id'] == 'network-21':
        question['source'] = {'title': 'RFC 4033: DNSSEC services and limitations (updated by later RFCs)',
            'url': 'https://www.rfc-editor.org/info/rfc4033/', 'reviewed': '2026-10-28'}


def lessons():
    return [{**module, 'revision': REVISION, 'sections': [{
        'id': topic, 'title': TOPICS[topic][0], 'objective': 'Apply ' + TOPICS[topic][0].lower() + ' to an evidence-based decision.',
        **supplements(topic), 'body': TOPICS[topic][2] + ' ' + EXTENSIONS[topic], 'source': further_reading(topic),
        'worked_cases': [{'objective': q['objective'], 'situation': q['prompt'], 'reasoning': q['explanation']} for q in BANK if q['topic'] == topic]
    } for topic in module['topics']]} for module in MODULES]
