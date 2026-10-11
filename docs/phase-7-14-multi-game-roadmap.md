# EduCyber Nigeria: multi-game platform principle

Each pathway (secondary Cyber Explorers, university Cyber Academy, professional Cyber Command) must grow into a library of **multiple distinct games**, not a single mission. A mission is a playable unit; a game may contain many missions, levels and scenarios. Avoid equating a pathway, game and mission.

## Phase 7.14 deliverable

The `CorrelationBoard` component is a reusable optional evidence-linking and hypothesis scratchpad available in the mission workspace across existing missions. It uses only public stage evidence, never answer keys; links and hypotheses are client-local and do not affect authoritative scoring. Reset on stage change. This is a first UI increment, **not** server-graded hypothesis validation or an incident timeline.

## Planned game portfolio (concepts, not implemented games)

| Pathway | Potential independent games |
| --- | --- |
| Cyber Explorers | Phishing Detective; Password Fortress; Privacy Quest; Safe Social World |
| Cyber Academy | Operation Firewall; Network Defender; Digital Forensics Lab; Secure Code Challenge |
| Cyber Command | Incident Commander; Ransomware Response; Cloud Risk Simulator; Cyber Resilience Tabletop |

## Architecture guardrails

1. Use catalog metadata to associate many games and missions with each pathway; never hardcode one game per audience.
2. Allow games to select mechanics independently (decision, investigation, simulation, 3D, quizzes), including accessible 2D paths.
3. Keep scenario data, progression and scoring server-owned; never send answer keys in public manifests.
4. Prefer reusable UI modules over coupling everything to `operation-firewall`.
5. Add games iteratively with automated validation and separate acceptance tests; portfolio entries above are roadmap concepts only.
