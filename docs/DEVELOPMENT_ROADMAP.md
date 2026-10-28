# Approved development roadmap

Approved by Emmanuel on 26 October 2026 (Africa/Lagos).

## Product direction and standing decisions

EduCyber Nigeria serves secondary, university and professional cybersecurity learners. Keep beta testing open while development proceeds in a separate checkout and database. This decision supersedes the earlier pause on major redevelopment during beta.

Prioritise learning quality, beginner accessibility, mission clarity and reliable operation before enlarging the catalogue. Keep the long-term target of **10 games per category**, useful 2D/3D modes and low-bandwidth alternatives. Audit the implemented catalogue before assigning remaining counts; earlier snapshots are not current inventories.

Security by design, OWASP-aligned engineering, server-side validation and authorisation, meaningful tests, readable modular code, useful comments/docstrings, architecture decisions and maintainer documentation apply throughout. Preserve serverless portability without premature complexity. The owner is currently the sole developer collaborating with an assistant.

## Feedback evidence and priority backlog

Source: the private beta-feedback export reviewed on 26 October 2026. These are anonymised product themes from a small sample, not proof of overall satisfaction. Keep the raw export, tester identifiers and private records out of Git.

| ID | Observation | Planned response | Acceptance evidence |
| --- | --- | --- | --- |
| FB-01 | Lessons do not sufficiently prepare beginners for assessments. | Map questions to objectives; expand explanations, worked examples and guided practice. | Every assessed concept is taught; beginner walkthroughs demonstrate independent completion. |
| FB-02 | Mission tasks and expected actions are unclear. | Briefings covering objectives, evidence, actions, completion conditions and contextual hints. | New testers start and finish representative missions without developer assistance. |
| FB-03 | Learners need strengths/weaknesses analysis. | Topic-level results, mistake explanations and next-step recommendations. | Results derive from actual attempts and distinguish insufficient evidence from demonstrated weakness. |
| FB-04 | 2D/3D interactions were unresponsive and added little value. | Diagnose responsiveness and redesign interactions around meaningful learning tasks; retain accessible lightweight fallback. | Supported devices complete relevant actions in both modes; visuals serve explicit objectives. |
| FB-05 | One post-mission question is insufficient. | Varied review questions, typically around five where appropriate to the objectives. | Questions cover distinct concepts and explain answers. |
| FB-06 | Some assessment content repeats, including Cyber Safety Foundations. | Audit accidental duplicates and overlap; retain intentional varied reinforcement. | Reviewed question bank with documented reinforcement rather than duplicated checks. |
| FB-07 | Lessons need interactivity and practical examples. | Short exercises, predictions, immediate explanations and worked examples. | Learners apply each concept during the lesson. |
| FB-08 | Python variables and conditional logic lack adequate examples. | Prioritise values, types, conditions, expected outputs and guided exercises. | Learners explain variable values and predict simple conditional outcomes. |

Each implemented item must link to its source feedback, code/commit, acceptance criteria and verification result. Preserve deferred suggestions with reasons. Add application version metadata to future feedback.

## Delivery phases

| Phase | Scope | Gate |
| --- | --- | --- |
| 1. Protect the open beta | Verify source/database baseline; export feedback; create and restore a backup; separate development checkout, database and services; establish release/recovery procedures. | Demonstrated isolation and recovery; tester accounts, progress and feedback preserved. |
| 2. Establish security assurance | Baseline audit with Cloudflare security-audit skill; review authentication, authorisation, recovery, data access, AI interactions and deployment; verify dependency, code and secret checks. | Validated, prioritised findings tracked; confirmed critical issues fixed before affected releases. |
| 3. Repair learning foundations | FB-01, FB-06, FB-07, FB-08: deeper lessons, assessment alignment, examples and reviewed questions. | Content review and beginner testing show lessons prepare learners for assessments. |
| 4. Improve missions | FB-02, FB-04, FB-05: briefings, hints, evidence interaction, purposeful responsive 2D/3D and post-mission checks. Perfect one beginner journey first. | Independent completion plus evidence of understanding on representative devices. |
| 5. Improve progression and usability | FB-03; useful results/recommendations; verify outstanding onboarding, mobile, dark theme, logout and dashboard previews before implementing gaps. | Accurate persistent progress; learners can choose suitable next steps. |
| 6. Expand proven patterns | Work towards 10 games per category, broader investigations and stronger Yoruba/Igbo tutor support. Validate language quality and safe AI responses. | Distinct reviewed objectives, reliable interactions and saved progress for every published activity. |
| 7. Prove production readiness | Dependable hosting beyond a laptop, monitoring, useful logs/alerts, backup restoration, email monitoring, performance/load testing, accessibility, privacy and maintainer runbooks. | Demonstrated recovery/capacity, core real-backend browser journeys and agreed operational targets. |
| 8. Validate and expand | Broader pilot, independent security/content review; demand-led institutional dashboards, adaptive learning or multiplayer. | Educational value, reliable operation and sustainable costs demonstrated before expansion. |

Security assurance runs throughout; phase order does not defer urgent security fixes.

## Cloudflare audit decision

The requested mechanism is [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill), **not** Cloudflare WAF, Tunnel or account Security Insights. No hosting migration or paid Cloudflare service was approved merely by selecting this skill.

At the planning checkpoint, its README describes reconnaissance, coverage-led hunting, independent candidate validation, structured findings and reporting. Read the current SKILL.md and referenced workflow before running it; record the exact upstream revision used.

Run a baseline audit, retest fixes and review significant security-sensitive changes. Preserve confirmed, needs-validation and rejected outcomes with evidence and coverage gaps. The audit has **not yet been installed or executed**.

Execution-based validation must use the skill's required OS-enforced sandbox: no external network, sanitised environment, resource limits and restricted scratch writes. A disposable database alone does not satisfy all those controls. Keep unresolved source leads as needs-validation when execution prerequisites are unavailable. Do not run active audit tests against the tester-facing beta.

## Release practice and definition of quality

Develop against separate data, use feature branches and small releases, review diffs, test migrations/recovery, record versions and communicate brief update windows. Feature flags may protect incomplete work. Do not trust client-submitted scores or expose other learners' data.

Agree measurable targets for independent task completion, learning gain, accessibility, supported-device performance, reliability, restoration and maintainability. Passing a scanner or reaching a game count alone does not establish world-class quality.

Future educator/organisation features require validated demand, proper access controls and tenant isolation. Do not let advanced expansion displace the core learning experience.

## Maintenance

Update this roadmap when scope is explicitly changed. Keep operational progress and the immediate next action in [DEVELOPMENT_STATUS.md](DEVELOPMENT_STATUS.md). Do not silently turn proposed work into completed work.

## Approved refinement — 26 October 2026

Following successful owner-reported baseline learner checks, the owner approved selectable assessment lengths (Quick, Standard, Extended and Custom within the available bank) and automatic scrolling/keyboard focus when opening activities as the next bounded build. These additions support the assessment and usability phases and will be included in the baseline audit scope. Preserve the security audit and all other phase gates. See [the feature contract](ASSESSMENTS_AND_ACTIVITY_NAVIGATION.md) and the current status for implementation versus acceptance evidence.


## Sequencing update — 26 October 2026

The owner deferred the formal Cloudflare security-audit-skill workflow until the end of development and instructed that Phase 3 proceed now. Security by design, secure coding/review, authorization/input checks and meaningful ordinary tests remain required in every build. Resume the formal audit against the final source, revalidating changed code and unresolved checkpoints. This change provides no security clearance and does not remove final assurance/release gates. Phase 3 starts with the [Python foundations pilot](PYTHON_FOUNDATIONS.md); the other course reviews remain pending.



## Approved delivery-size update — 28 October 2026

After reporting Phase 4.2 passed, the owner requested larger batches to move the remaining games to the accepted guidance/interaction/review standard faster. The owner approved the proposed next six-game batch. Work in bounded batches of five to six related games where the shared framework supports it; retain per-game distinct evidence/tasks/hints/review, automated checks, secure coding and focused local acceptance. This changes delivery size, not security, educational or release gates. The next batch is Privacy Patrol, Scam Spotter, Safe Social, Device Defender, Wi-Fi Wise and Digital Footprints. Three guides were implemented before this batch; completing its source brings the count to nine of 30 existing games, not 30 independently validated experiences.
