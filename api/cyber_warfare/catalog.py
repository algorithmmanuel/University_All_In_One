"""Versioned, conceptual actions; never execute commands or contact a network."""
from dataclasses import asdict, dataclass
import hashlib
import json

ENGINE_VERSION = 'red-blue-v1'


@dataclass(frozen=True)
class Action:
    id: str
    side: str
    phase: str
    cost: int
    success: float
    detection: float
    technique: str
    explanation: str
    prerequisites: str
    rule: str
    relation: str

    def public(self):
        return {**asdict(self), 'framework': 'MITRE ATT&CK',
                'url': f'https://attack.mitre.org/techniques/{self.technique}/'}


# Probabilities are teaching abstractions, not measured threat frequencies.
ACTIONS = {a.id: a for a in (
    Action('recon', 'red', 'reconnaissance', 1, .95, .10, 'T1595',
           'Study the simulated inventory and adjacent trust relationships.', 'Known, reachable asset.',
           'Success reveals adjacent assets and a dated weakness assessment.', 'represents'),
    Action('phish', 'red', 'initial access', 2, .70, .25, 'T1566',
           'Test the organisation’s simulated resistance to deceptive messages.', 'Known exposed workstation; no believed foothold.',
           'Phishing susceptibility raises success; hardening lowers it.', 'represents'),
    Action('cloud_access', 'red', 'initial access', 2, .70, .25, 'T1190',
           'Test a simulated public service configuration boundary.', 'Known exposed cloud or server; no believed foothold.',
           'A configuration weakness raises success; hardening lowers it.', 'represents'),
    Action('escalate', 'red', 'privilege escalation', 2, .65, .30, 'T1068',
           'Attempt to raise the privilege of an existing simulated foothold.', 'Believed user foothold.',
           'An unpatched privilege weakness raises success; patching lowers it.', 'represents'),
    Action('lateral', 'red', 'lateral movement', 2, .65, .30, 'T1021',
           'Attempt to cross one simulated trust connection.', 'Known target connected to a believed privileged foothold.',
           'Weak access boundaries raise success; segmentation blocks the crossing.', 'represents'),
    Action('persist', 'red', 'persistence', 2, .70, .20, 'T1098',
           'Attempt to retain simulated access through an account change.', 'Believed privileged foothold.',
           'Hardening lowers success; retained access survives containment but cannot act while isolated.', 'represents'),
    Action('exfiltrate', 'red', 'exfiltration', 3, .70, .50, 'T1041',
           'Attempt to move fictional data beyond the simulated boundary.', 'Believed privileged foothold; target not already copied.',
           'Hardening and access controls lower success; isolation blocks it.', 'represents'),
    Action('disrupt', 'red', 'impact', 3, .75, .70, 'T1486',
           'Attempt a fictional ransomware availability impact; no files are touched.', 'Believed privileged foothold; target not already disrupted.',
           'Patching and hardening lower success; isolation blocks the action.', 'represents'),
    Action('fraud', 'red', 'impact', 3, .65, .50, 'T1565',
           'Attempt to alter a fictional payment record.', 'Believed privileged foothold; target not already altered.',
           'Access review and hardening lower success; isolation blocks the action.', 'represents'),
    Action('prompt_injection', 'red', 'initial access', 2, .70, .35, 'T1698',
           'Test an AI service’s simulated separation of untrusted content and instructions. No prompt is generated.',
           'Known exposed AI cloud service; no believed foothold.',
           'An instruction-boundary weakness raises success; hardening lowers it.', 'represents'),
    Action('monitor', 'blue', 'monitoring', 1, 1., 0., 'T1595',
           'Improve telemetry on one asset; this alone does not reveal a compromise.', 'Asset in owned inventory.',
           'Always installs monitoring, raising later attack detection probability.', 'addresses'),
    Action('patch', 'blue', 'patching', 2, 1., 0., 'T1068',
           'Remediate simulated software weaknesses without removing existing access.', 'Asset in owned inventory.',
           'Always removes the privilege weakness and lowers software attack success.', 'addresses'),
    Action('harden', 'blue', 'hardening', 2, 1., 0., 'T1190',
           'Tighten service configuration and untrusted input boundaries.', 'Asset in owned inventory.',
           'Always removes configuration/instruction weaknesses and lowers attack success.', 'addresses'),
    Action('segment', 'blue', 'segmentation', 2, 1., 0., 'T1021',
           'Restrict lateral trust connections to an asset.', 'Asset in owned inventory.',
           'Always blocks new lateral crossings to or from the asset.', 'addresses'),
    Action('access_review', 'blue', 'access review', 2, 1., 0., 'T1098',
           'Revoke simulated sessions and retained access; strengthen access boundaries.', 'Asset in owned inventory.',
           'Always clears footholds and persistence and tightens access control.', 'addresses'),
    Action('detect', 'blue', 'detection', 1, .85, 0., 'T1098',
           'Investigate account and endpoint evidence. A quiet result is not proof of safety.', 'Asset in owned inventory.',
           'Monitoring raises investigation sensitivity; success can identify a present foothold.', 'addresses'),
    Action('contain', 'blue', 'containment', 2, 1., 0., 'T1021',
           'Isolate an asset, accepting temporary business unavailability.', 'Asset in owned inventory.',
           'Always isolates; removes ordinary access, but retained access needs review or recovery.', 'addresses'),
    Action('recover', 'blue', 'recovery', 3, .90, 0., 'T1486',
           'Restore a service from a simulated backup and revoke access. Historical leakage cannot be undone.',
           'Asset in owned inventory.',
           'A backup is required at resolution; success clears disruption, isolation and retained access.', 'addresses'),
    # Waiting is an economy operation, associated with the technique a side is delaying/reviewing.
    Action('wait_red', 'red', 'planning', 0, 1., 0., 'T1595',
           'Conserve resources and review reconnaissance.', 'No target.', 'Always succeeds; adds no intelligence.', 'context'),
    Action('wait_blue', 'blue', 'planning', 0, 1., 0., 'T1595',
           'Conserve resources and review existing telemetry.', 'No target.', 'Always succeeds; adds no intelligence.', 'context'),
)}


def catalog_digest():
    payload = json.dumps([ACTIONS[k].public() for k in sorted(ACTIONS)], sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()
