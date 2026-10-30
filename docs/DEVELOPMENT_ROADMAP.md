# Approved development roadmap

Approved by Emmanuel on 26 October 2026 (Africa/Lagos).

## Product direction and standing decisions

EduCyber serves secondary, university and professional cybersecurity learners. Keep beta testing open while development proceeds in a separate checkout and database. This decision supersedes the earlier pause on major redevelopment during beta.

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
| 6. Build consequential gameplay and deeper cybersecurity learning | Original browser strategy simulation inspired by ThreatGEN; richer source-linked cybersecurity teaching; extensive topic practice with a proposed 500-question platform bank. English only; Nigerian languages deferred and AI reserved for later. See the current gameplay plan. | Complete replayable pilot with meaningful consequences, reliable saved state, aligned teaching/practice and independent learner/device checks before expansion. |
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


## Approved Phase 5 batching — 28 October 2026

The owner confirmed Phase 5.2 had not been installed and requested all remaining Phase 5 work in one release to reduce update/acceptance cycles. Complete the progression/results/dashboard, mission next-step/history, onboarding/mobile/dark-theme/logout and load-recovery implementation together; run automated checks as one batch and provide one [combined release guide](PHASE_5_RELEASE.md). Earlier incremental Phase 5.2 acceptance sequencing is superseded. Phase 5.1 local acceptance remains recorded. This changes delivery size, not evidence: retain accurate historical data, access controls, independent learner/device evidence, operational targets and the deferred final formal security audit. Do not require separate installation of 5.2 before this combined build.


## Owner vision correction — 28 October 2026

The owner explicitly deferred Yoruba, Igbo and all other Nigerian-language additions. Current priorities are a cybersecurity-focused browser video-game experience inspired by ThreatGEN, richer cybersecurity courses with optional public reading, and extensive practice across topics (potentially around 500 questions). AI is a long-term option. The earlier six-investigation plus study-helper next-build recommendation is superseded.

[The gameplay and learning plan](PHASE_6_GAMEPLAY_PLAN.md) records these decisions and proposes a complete first strategy-game slice, supporting lessons and cumulative 100 → 250 → 500 reviewed question milestones. The exact gameplay style, 500-total assumption, allocations, release sizes and measurable targets are recommendations under discussion, not separately approved owner specifications. Preserve existing games/progress and beta isolation; ordinary secure engineering, independent educational/device checks, operational readiness and the deferred final formal audit remain required.


## Authorised temporary-beta promotion — 29 October 2026

After owner-reported acceptance through Branch Siege, the owner explicitly requested merging completed development into the existing tester-facing beta before a new major development area. This authorises the bounded source promotion and the documented beta backup/additive-migration/content-publication/restart procedure while retaining development isolation, existing accounts/progress/feedback and ongoing assurance gates. It supersedes earlier “no beta promotion” scope statements for this rollout only. It does not imply a production hosting launch or completion of independent learner/device/operational/final-security gates. See [the promotion guide](BETA_PROMOTION_2026_10_29.md) and status for source versus actual runtime evidence.


## Approved Red/Blue simulator phase — 29 October 2026

The owner reports the latest beta developments are uploaded and both beta and development environments restarted successfully. This is owner-reported runtime evidence, not independently observed deployment logs.

The next major development is the [Red/Blue simulator plan](RED_BLUE_SIMULATOR_PLAN.md): scenario-driven two-seat hidden planning, deterministic resolution and filtered evidence, six industry scenarios, mapped educational actions, three readable opponent levels, later authenticated two-human sessions and a responsive interface/debrief. This brings multiplayer forward from the earlier demand-led expansion phase for this bounded module; external generative AI and all Nigerian-language additions remain deferred. Simulating an AI-service security incident does not change the external-AI decision.

Delivery is explicitly staged: inspect/summarise the existing architecture before code; build the engine/loader/resolver and unit/determinism tests; **stop and show results before building any interface**. Next, prove additive persistence/authentication and separate-session concurrency, then build the interface, educational/balance checks and release evidence. Reuse current authentication; keep match roles separate from account roles. Do not overload existing single-user runs or grant instructors access without an explicit policy. See the plan for assumptions, public framework sources and security gates, and [authoring guidance](RED_BLUE_AUTHORING.md).

Keep the existing beta running separately. New simulator work is development-only until a further authorised promotion. The prior successful beta rollout does not authorize automatic promotion of this new work or establish independent learner/device/production/final-audit acceptance.


## Authorised simulator continuation — 29 October 2026

After the verified engine checkpoint, the owner explicitly authorised additive match persistence/authenticated APIs, proof using two actual sessions on isolated PostgreSQL, and then the responsive interface. This satisfies the earlier stop-for-engine-review gate. Ownership, hidden-choice secrecy, idempotency, stale commands, atomic resolution and concurrent submissions are mandatory evidence before interface implementation. Existing beta remains separate; no simulator promotion is authorised. Instructor review remains disabled pending an explicit policy. See [the API contract](RED_BLUE_API.md) and status for implementation versus verified evidence.


## Simulator interface delivery checkpoint — 29 October 2026

The separate-session PostgreSQL API gate passed before interface work. The additive responsive simulator interface, wiki/debrief and development release guide are implemented; current automated evidence and pending final CI are recorded in status. This is a source/technical milestone, not owner or independent educational/balance/device acceptance. Keep the operational/final-security gates, beta isolation and explicit future promotion requirement. New raw-body and safe-storage-error boundaries support the standing security-by-design requirement without changing existing game/authentication rules.


## Verified simulator technical milestone — 29 October 2026

Combined source `fe5de75` passed 805 PostgreSQL backend tests plus 11 subtests, 22 actual-API/PostgreSQL browser cases, 147 existing browser journeys, frontend unit/type/build and dependency gates. The persistence/concurrency gate passed before interface work. These close the automated implementation gates for the bounded simulator release, with the [development installation/acceptance guide](RED_BLUE_RELEASE.md) and status as handover. Owner acceptance, independent educational/balance/device evidence and operational/final-security gates remain open; beta promotion still requires a separate instruction.


## Approved journey organisation — 29 October 2026

Following owner-reported simulator acceptance and the source-based learner-material inventory, the owner adopted the eight-stage experience: Discover → Understand → Check understanding → Investigate with guidance → Manage consequences → Command an incident → Face an adaptive opponent → Compete and reflect. Make this the main homepage/student-dashboard navigation and provide a shared journey hub. Cyber Explorers, Cyber Academy and Cyber Command tailor material recommendations within the same journey; they are not separate locked ladders or account roles. Beginners receive an explicit stage-1 entry, experienced learners may enter any later stage, and Python remains optional. Preserve all existing material, saved progress, auth/eligibility and direct activity access. Navigation must not award mastery or automatically create activity. See [the journey release guide](LEARNING_JOURNEY_RELEASE.md) and status for implementation versus evidence. Development only; beta promotion and independent educational/device/operational/final-security acceptance remain separate.


## Verified journey navigation milestone — 29 October 2026

Source `1f23cfa` passed 150 browser regressions (147 existing plus three journey cases), 24 actual-API/PostgreSQL browser cases (22 existing plus two journey cases), 18 frontend unit tests, TypeScript and production build. The approved eight-stage, audience-assisted navigation is technically verified; no backend, schema, content-bank, rule or eligibility change was required. Follow [the development release guide](LEARNING_JOURNEY_RELEASE.md) for owner acceptance, then gather beginner/experienced/device evidence before further changes. Independent educational/operational/final-security gates and separate beta-promotion authorisation remain required.


## Authorised combined beta bundle and development pause — 29 October 2026

Following owner-reported journey acceptance, the owner requested global EduCyber display branding, a darker reddish theme and deeper options across all eight journey stages in one build, then explicitly authorised promotion to the existing beta for a personal playthrough. This supersedes prior development-only/no-promotion instructions for this bounded bundle. Preserve the three audience recommendations, open later-stage entry, existing materials/accounts/progress and separate environments.

The bounded implementation adds three saved decision workshops per stage (24 cases/72 decisions), a six-question public introduction and solo final-stage role reversal alongside the existing full games. These are authored guided exercises with decisions/consequences/replay, not new network engines or measured mastery. Additive workshop storage and authenticated owned APIs require isolated-PostgreSQL concurrency/preservation evidence and complete browser/backend/frontend gates before guarded source promotion. Use [the combined release guide](EDUCYBER_BETA_BUNDLE.md); source promotion is distinct from the owner's laptop backup/migration/restarts. Independent learning/device/operational/final-security acceptance remains open.

After the verified release and handover, **pause feature/content/theme redevelopment until Emmanuel completes the playthrough and explicitly resumes development**. Collect bugs using [the owner checklist](OWNER_BETA_PLAYTHROUGH.md), address requested blockers within scope, and do not automatically begin the next roadmap phase or another promotion.


## Verified combined beta handover — 29 October 2026

Implementation `3f4d4ab` passed 838 isolated-PostgreSQL backend tests plus 11 subtests, 150 browser regressions, 27 actual-API/PostgreSQL browser cases, 20 frontend unit tests, TypeScript, production build and dependency gates. Beta source was advanced from `5824fb7` to the verified implementation with ancestry and expected-head checks. Only documentation follows the verified source in the final handover. Actual owner laptop rollout and acceptance remain pending, distinct from source promotion. Follow [the combined guide](EDUCYBER_BETA_BUNDLE.md) and [checklist](OWNER_BETA_PLAYTHROUGH.md). **Feature development is paused until Emmanuel completes the playthrough and explicitly resumes it.** See status for exact evidence and remaining independent assurance gates.


## Owner visual-feedback correction — 29 October 2026

The owner prefers navy/teal as the primary brand for long learning sessions, with crimson deliberately scoped to Red and blue/teal to Blue in the simulator. This supersedes the global crimson palette in the previous bundled release. Keep the EduCyber name, journey, workshops, content and progress. Apply this bounded visual correction to the beta bundle after frontend/browser checks, then maintain the development pause pending owner playthrough. It does not authorise a new feature phase.


Verified visual correction: `467b896` passed 150 browser regressions, 27 actual-API/PostgreSQL browser cases, 21 frontend tests, TypeScript and production build; expected-head/ancestry checks preceded beta source promotion. Runtime update is frontend-only for an already installed bundle. The playthrough pause continues; see status for precise evidence.


## Owner playthrough navigation remediation — 30 October 2026 (planned, not implemented)

The owner's five populated findings in the six-page `Testing Observations.docx` identify a serious learning-journey usability gap: unclear start/help and Decision Workshop purpose; audience tabs that appear to lead to the same material; repeated public six-question preview and awkward double-verb CTAs; game library visible beneath assessment; and completion without a next-step/placement recommendation. The screenshots support the reported UX problem, not a claim of broken underlying gameplay. See [the complete scoped remediation plan](OWNER_NAVIGATION_REMEDIATION.md) for six work packages (UX-NAV-01 to UX-NAV-06), evidence, design choices, prioritisation, tests and release gates.

**Priority:** address pathway meaning/differentiation and completion next steps before new content/feature expansion. Preserve a shared eight-stage teaching model but make each audience's content recommendations and entry points materially different, retaining free later-stage entry. Treat six questions as an optional, non-gating diagnostic, not a permanent competence placement. Add accessible orientation and a focused quiz screen. Existing functionality not raised by the owner is assumed working; do not broaden scope silently. This is planning/triage only; no source implementation or beta promotion is authorised by writing this plan. The prior feature-development pause remains for unrelated work.


## Consolidated UX release approved — 30 October 2026

Owner authorised implementing all prioritised onboarding, pathway, focused six-question diagnostic, completion and navigation fixes in one major release, then merging the **verified** source into the tester-facing beta branch for ongoing feedback. Do not change any actual games or simulator internals. Maintain development/beta separation until approval gates pass. The work began on development; documentation and source presence do not establish CI success or runtime publication. See [navigation remediation specification](OWNER_NAVIGATION_REMEDIATION.md) and status for progress.


## Approved distinct pathway materials — 30 October 2026

The owner clarified and authorised beginning three distinct eight-stage content routes, so switching pathways offers different materials rather than the same exercises at greater difficulty. Keep the eight-stage names and existing engines, allocate the existing teaching/topic/case/scenario material first, and add content only where needed. [The allocation](PATHWAY_CONTENT_RELEASE.md) defines this bounded implementation, including distinct six-question introductions, exclusive workshop/topic/scenario allocations and final-stage onward navigation. General direct entry stays open. This supersedes the earlier shared-material navigation model, not authentication/ownership or educational/release gates. Existing saved activity records remain authoritative; no pathway completion or mastery is inferred from navigation. Beta promotion and independent assurance remain separate.


## Authorised two-environment pathway/help release — 30 October 2026

The owner confirms the distinct pathways are not yet personally tested and authorises synchronising development and tester-facing beta, adding a detailed public Help player guide, then testing development locally and beta via ngrok on the laptop. Preserve the three distinct eight-stage routes as the framework for future content enrichment. Use [the combined rollout guide](PATHWAYS_HELP_BETA_RELEASE.md) and current-head regression gates. Reconcile both source histories before promotion; retain accounts/progress and environment isolation. Source promotion is authorised without inventing owner acceptance or implying laptop processes were operated. No new curriculum expansion or gameplay rule change is required by this release.


## New approved product direction — 24 production courses (30 October 2026)

Owner identified that My Learning currently offers three short demo-style courses and requested a substantial reading-first academy: 3 audiences × 8 shared pedagogical stages = **24 different substantial courses**, each with multiple lessons and a curated further-reading section. Games remain untouched. Treat the 24 courses as separate coherent curricula, not identical content at harder difficulty, and ensure reading-only users can engage for substantial periods without gaming. The [course-library specification](PRODUCTION_LEARNING_LIBRARY_PLAN.md) provides initial 24-title matrix, recommended 8–12 deep lessons/course, quality/accessibility requirements, source verification and preservation/release gates. This is a new content-phase scope, **not** an implemented or published catalogue. Maintain the ongoing beta while development remains isolated.
