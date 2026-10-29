# EduCyber — interactive cybersecurity game and learning plan

Planning revision: 28 October 2026 (Africa/Lagos). Baseline source inspection: `9950eed`; inspection handover: `e4245dd`. Owner direction below supersedes the earlier six-investigation/study-helper next-build recommendation in `PHASE_6_SCOPE.md`. This document proposes scope and acceptance targets; it does not report implementation or owner approval of every proposed detail.

## Owner direction and scope boundaries

The owner wants a browser experience that feels like a video game focused on cybersecurity, citing ThreatGEN as a reference; deeper cybersecurity courses with optional publicly readable sources; extensive practice across topics, potentially around 500 questions; and an AI component in the longer term.

- English only for current development. Defer Yoruba, Igbo and all other Nigerian-language additions, translation scaffolding and language selectors until explicitly requested again.
- Prioritise consequential gameplay, cybersecurity teaching and practice. Defer the previously proposed guided study helper as a separate deliverable; it is not the current product priority.
- AI is a future option, not a dependency for the first game. A rules-based opponent can react to game state without any external model.
- Preserve beta, accounts, progress and historic results. Continue separate development, ordinary secure engineering and the existing operational/final assurance gates. No beta promotion or deployment is requested by planning.

## Reference and present gap

ThreatGEN's public [Red vs. Blue description](https://threatgen.com/red-vs-blue) describes turn-based cybersecurity strategy, choices with costs/consequences, an opponent and debrief/replay, within a broader education offering. Its [public FAQ](https://threatgen.com/red-vs-blue/faq) describes a network-level simulation. These are vendor descriptions reviewed on 28 October; no signed-in game session was played and no private implementation was inspected. Use the design principles as inspiration for original EduCyber rules, writing and visuals.

EduCyber already has 30 guided missions with persistent decisions, a shared 3D room and optional review. The normal guided flow largely consists of artifact reading and choosing findings/responses. A new strategy simulation needs evolving asset state, limited resources, meaningful counterplay and multiple possible outcomes. More artifact questions or a different camera alone would not deliver the requested experience. Retain the current missions as case studies and teaching material; do not relabel all 30 as completed strategy games.

Three curated foundations releases currently contain three lessons and 20 assessment questions each (60 course questions total in these releases). This is committed source, not a count of installed owner-database rows. The separate 150 mission review questions are not part of that assessment count. Current length-based selection is deterministic: the same bank and length yield the same questions. The 100-question explicit-request cap is a per-attempt bound, not a bank-size target.

## Proposed product structure

| Area | Learner experience | Shared learning connection |
| --- | --- | --- |
| Learn | Substantial cybersecurity lessons, diagrams, worked examples and guided checks | Teach the objectives tested by practice and used in gameplay |
| Practise | Topic/difficulty selection, mixed sessions, mistake review and saved results | Explain each answer and link back to relevant lessons/public reading |
| Play | Interactive scenario map, resource decisions, evolving incidents and recovery | Show the consequence of applying or neglecting the same controls |
| Review | Timeline, outcome breakdown and recommended next activity | Separate simulation performance from demonstrated knowledge or mastery |

## Proposed first game: Operation Firewall — defend the branch

Build one complete original scenario before expanding the strategy catalogue. This can be a new strategy mode associated with the existing Operation Firewall entry; retain its current three-stage mission and saved history. First target: desktop/laptop browser, with touch-capable controls and an accessible lightweight presentation. Suggested session length is 10–20 minutes, to be tested rather than promised.

The player manages a fictional organisation's branch network. A top-down or isometric board shows roughly 6–8 connected assets, such as staff workstations, an identity service, application/database services and backup storage. A clear HUD shows service availability, incident status, budget and available staff actions. Use animated traffic, changing asset states, event notifications and optional sound with mute; do not require free-roaming 3D to make the game engaging.

### Play loop

1. **Prepare:** inspect the map, learn critical services and spend a limited budget on controls such as MFA, monitoring, patching, segmentation and protected backups. Every control has an explicit fictional effect/cost; no product provides universal protection.
2. **Observe:** advance a turn, receive partial telemetry and investigate relevant assets. Some real simulated problems remain hidden until the player has visibility; some alerts are benign.
3. **Act:** choose bounded actions such as investigate, isolate, revoke access, patch, segment or recover. Actions cost staff/time/budget and may have delayed effects or disrupt service.
4. **Adapt:** a rules-based attacker progresses along allowed simulated paths according to exposures, controls and the scenario seed. Event timing and starting conditions vary within reviewed bounds; actions change what can happen next.
5. **Recover and debrief:** meet explicit containment/recovery conditions or reach a justified loss outcome. Reconstruct the timeline, explain tradeoffs, connect decisions to lessons and replay a different strategy.

Example: isolating a compromised workstation may limit spread while reducing service availability; patching a service takes time and may create a maintenance outage; restoring before resolving the entry condition can allow simulated recurrence. These effects must follow documented scenario rules, not arbitrary penalties.

Prefer discrete turns with visual animation for the first build. They allow deliberate decisions, pause/save/resume, fair testing and intermittent connections. An optional timed challenge can follow later. First playable role is Blue Team against a simulation; playable Red Team, multiplayer and an open-ended world are later design options.

### Game systems and implementation boundaries

| System | Initial contract |
| --- | --- |
| Scenario definition | Versioned assets, connections, control effects, action prerequisites/costs/durations, adversary transitions, event conditions and win/loss rules |
| Authority | FastAPI owns state transitions, hidden adversary state, budgets, legal actions and scoring. Browser sends action requests rather than resulting state or points. |
| Persistence | Separate versioned strategy runs and action/event history; do not overload legacy three-stage runs. Pin scenario/rule revision so resume and debrief retain their original meaning. Review an additive migration with populated-data preservation checks. |
| Fair recovery | Validate run ownership and expected revision; deduplicate repeated commands, serialize conflicting turns and handle reconnects without double-spending or advancing twice. |
| Replay | Server-owned scenario seed and event history make failures reproducible. Do not expose hidden state/seed information that reveals future events through the public run response. |
| Client | Reuse Next.js/TypeScript and existing account/navigation/results patterns. Choose the lightest renderer that meets the interaction needs after a small technical spike; avoid committing to a second engine before measuring. Existing Three.js can support later optional presentation. |
| Learning feedback | Explain availability, protection, detection, response and recovery separately. Reward relevant results/tradeoffs rather than fastest clicking; avoid treating a game score as certification or mastery. |

All activity uses fictional systems and simulated actions. The runtime performs no live scanning, exploitation, credential testing or malware execution.

## Richer cybersecurity curriculum

Organise the learning catalogue around the same topic families as the practice bank. Preserve accepted foundations and learner progress; add or version content deliberately. Python can remain a supporting skill where it helps log analysis and defensive automation, while cybersecurity becomes the main teaching focus.

Each substantive lesson should include objectives/prerequisites, an accessible explanation, a diagram or worked incident, a practical check with feedback, a game application, a short recap and optional further reading. Learners should be able to finish the core lesson without leaving EduCyber.

Maintain a source register: publisher/title, exact public URL, covered objective, publication/version where available, last link/content review date and permitted use. Link to useful sections, state whether reading is beginner or advanced, and label external links. Public access does not imply permission to reproduce entire documents. Write original teaching and questions; avoid copied commercial exam banks. Check links before publication and on later content reviews.

Initial primary-source candidates reviewed for this plan:

- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework): risk-management structure and outcomes.
- [OWASP Top 10](https://owasp.org/projects/top-ten): web application security risks; choose the relevant version explicitly when authoring lessons.
- [MITRE ATT&CK](https://attack.mitre.org/): adversary-behaviour references for scenarios and defensive analysis, with beginner explanations supplied by EduCyber.
- [CISA public safety tip sheet](https://www.cisa.gov/sites/default/files/2024-09/Secure-Our-World-4-Easy-Ways-Stay-Safe-Online-Tip-Sheet.pdf): personal safety, phishing, passwords, MFA and updates. The CISA HTML landing page returned 403 to the research fetch; verify learner access and provide an alternative when needed.

These are reference families, not a claim that detailed new lessons or all deep links have already been reviewed.

## Proposed 500-question practice blueprint

Treat 500 as a first substantial bank **across the platform**, not 500 per course and not one 500-question sitting. This is a planning assumption to confirm with the owner. Count only published, distinct, reviewed cybersecurity questions with objective mappings; do not inflate the count with archived rows, reordered options, superficial rewordings or the separate mission reviews.

| Topic family | Proposed final count |
| --- | ---: |
| Cybersecurity fundamentals and risk | 50 |
| Phishing and social engineering | 50 |
| Identity, passwords and access control | 50 |
| Network security and segmentation | 50 |
| Endpoint security, malware and patching | 50 |
| Web/application security and secure development | 50 |
| Cloud security and configuration | 50 |
| Monitoring, logs and incident response | 50 |
| Data protection, cryptography, backups and recovery | 50 |
| Governance, audit and third-party risk | 50 |
| **Total** | **500** |

Start with 20 foundational, 20 applied and 10 challenging questions per family as an editorial allocation, subject to review. Use scenario questions, log/configuration interpretation and practical decision-making as well as recall. Each question needs a stable ID/revision, topic/objective/difficulty tags, plausible choices, an unambiguous answer, explanations of the correct and incorrect choices, lesson references and relevant public source links.

Before expanding publication, add server-owned practice sessions that pin the selected question IDs/revisions and preserve historic result snapshots. Support fresh random selection, topic-balanced mixes, avoid-recently-seen selection until the eligible pool is exhausted, and deliberate mistake review. Do not grade a new random sample on submission or let a bank edit change an in-progress session. Keep answers/keys private until the relevant feedback point. Existing attempts remain readable without invented topic history. Retain short sessions such as 5/10/20, with larger optional sets where useful, rather than loading the entire bank.

Publish in reviewed cumulative milestones: 100, then 250, then 500 cybersecurity questions. Existing items may count only after checking mapping, currency and duplication. Run content checks for duplicate concepts/prompts, answer ambiguity, option bias and coverage. Automated checks support editorial review; they do not certify factual quality. Use learner results and feedback to revise poor questions without silently regrading history.

## Proposed delivery sequence

| Build | Concrete outcome | Acceptance before expansion |
| --- | --- | --- |
| A — complete first playable slice | One Operation Firewall strategy scenario, its tutorial/debrief, 2–3 supporting cybersecurity modules and a cumulative 100 reviewed practice questions; versioned simulation/practice persistence | Player can complete and replay a consequential game; save/resume and reconnect preserve the run; lessons teach tested concepts; fresh practice actually varies |
| B — replay and curriculum expansion | Tune the first game from learner observation, add two scenario variants using distinct mechanics/objectives, broaden lessons and reach 250 questions | Different strategies/variants change outcomes for documented reasons; difficulty and learning recommendations are understandable |
| C — substantial learning release | Reach 500 reviewed questions across ten topic families, fill teaching gaps, polish campaign progression/accessibility and selectively adapt suitable existing missions | Topic coverage, reliable progress, usable device performance and evidence of independent learner completion; no game-count-only completion claim |
| D — later capabilities | Evaluate AI coaching grounded in approved content, richer adversary behaviour and demand-led multiplayer | Separate data/cost/safety evaluation and demonstrated value; authoritative game rules and scoring remain controlled |

These are delivery milestones, not calendar estimates or instructions to rush content. Split internal engineering into reviewable changes but provide cohesive tested releases and complete PowerShell update/test/restart guides. Before estimating dates, validate the new engine/persistence needs and the content authoring/review effort.

## Proposed pilot acceptance targets

- A player inspects assets, spends resources, observes changing events and wins/loses under explained rules; two materially different strategies can produce different documented outcomes.
- A tutorial makes controls/goal/turn progression understandable; observe at least five new learners as an initial usability check, aiming for four to finish without developer intervention. This small sample is diagnostic, not proof of overall educational effectiveness.
- Reload, interrupted requests and duplicate action submissions do not lose progress, reveal another run or spend resources twice. Cross-user/role boundaries and hidden-state disclosure receive tests.
- Target a smooth primary game view on the agreed baseline laptop (provisionally 30 fps), then measure actual hardware, load time and transferred bytes before claiming support. Provide keyboard/touch alternatives, reduced motion and mute. Do not require permanent animation or a running WebGL scene.
- Game outcomes and practice history are saved; debrief recommendations trace to observed actions/answers and taught objectives. Test actual API/PostgreSQL browser journeys, not only intercepted responses.
- All published new questions have objective and source mappings with explanations, and required teaching is available. Retain independent educational/content review, operational readiness and final formal security assurance gates.

## Current continuation — 29 October 2026

Builds A and B were implemented, passed their recorded automated gates and received owner-reported local acceptance. Following the owner's “go on”, Build C source now implements the cumulative 500-question milestone, additional teaching/reflections, derived campaign activity guidance and an asset-list alternative. This supersedes the original pre-Build-A immediate-action discussion. See [the current Build C guide](BUILD_C_CAMPAIGN_AND_500_QUESTIONS.md) and status for actual verification, CI and owner acceptance versus outstanding evidence. No claim of phase completion, ThreatGEN parity, independent learning effectiveness or production readiness follows from source counts.

Next: verify Build C CI and development acceptance, collect independent beginner/content/device observations, and use that evidence to select further gameplay improvements. The current three scenarios remain freely playable on the same six-asset map. AI and Nigerian-language work remain deferred.
