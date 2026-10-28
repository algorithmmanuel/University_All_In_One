# Phase 6 — source inventory and next build

Inspected 28 October 2026 (Africa/Lagos), branch `feature/beta-continuous-improvement`, source `9950eedb928dfe90f6d91e802ce2ebe6a2ab6b35`. This is a source inspection and implementation contract for the next build, not a delivered feature release or new owner acceptance. The [approved roadmap](DEVELOPMENT_ROADMAP.md) remains authoritative; [current status](DEVELOPMENT_STATUS.md) distinguishes implementation, CI and owner reports.

## Confirmed inventory

`api/game_catalog.py`, `api/mission_data.py` and `api/mission_learning.py` agree on 30 playable games mapped one-to-one to 30 missions and 30 guides. Each pathway has ten games. Every mission has three engine stages, three guided tasks and five optional review questions: 90 stages, 260 detailed stage artifacts and 150 review questions altogether. Artifact counts vary by stage; do not assume three records everywhere. There are no planned/unplayable catalogue entries at this revision.

Each guide provides objectives, role/workflow/completion instructions, hints and post-decision finding explanations. Existing game IDs, mission IDs and saved progress must be retained. The count target is already met; another 30 games or another blanket guidance rollout would duplicate delivered work.

### Cyber Explorers

| Catalogue title | Mission ID |
| --- | --- |
| Scholarship Detective | `phishing-investigation` |
| Password Fortress | `password-fortress` |
| Privacy Patrol | `privacy-patrol` |
| Scam Spotter | `scam-spotter` |
| Safe Social | `safe-social` |
| Device Defender | `device-defender` |
| Wi-Fi Wise | `wifi-wise` |
| Digital Footprints | `digital-footprints` |
| MFA Guardian | `mfa-guardian` |
| Backup Buddy | `backup-buddy` |

### Cyber Academy

| Catalogue title | Mission ID |
| --- | --- |
| Midnight Login Alerts | `soc-alert-triage` |
| Operation Firewall | `operation-firewall` |
| Network Watch | `network-watch` |
| Web Defense | `web-defense` |
| Cloud Perimeter | `cloud-perimeter` |
| Forensics Desk | `forensics-desk` |
| Malware Clues | `malware-clues` |
| Identity Lab | `identity-lab` |
| Secure Code Review | `secure-code-review` |
| Threat Hunter | `threat-hunter` |

### Cyber Command

| Catalogue title | Mission ID |
| --- | --- |
| Branch Resilience | `incident-response` |
| Risk Command | `risk-command` |
| Zero Trust Briefing | `zero-trust-briefing` |
| Cloud Incident | `cloud-incident` |
| Supply Chain Watch | `supply-chain-watch` |
| Ransomware Recovery | `ransomware-recovery` |
| Identity Crisis | `identity-crisis` |
| Boardroom Breach | `boardroom-breach` |
| AI Governance | `ai-governance` |
| Audit Trail | `audit-trail` |

## Actual investigation gaps

| Source evidence | Implication for Phase 6 |
| --- | --- |
| `web/app/missions/MissionWorkspace.tsx` selects `MissionArtifacts` whenever `run.learning.stage` exists; all current active missions have it. | The normal guided 2D experience is an artifact-card reader. The themed `ExplorerInvestigation`, `AcademyInvestigation` and `CommandInvestigation` components are fallback code, not evidence that those tools appear in current guided journeys. |
| `MissionLearning.tsx` marks a record inspected on opening; `CorrelationBoard.tsx` connects arbitrary inspected pairs and accepts a local hypothesis. | Interaction exists, but connections/hypotheses are not checked for correctness. Opening records is not proof of understanding. Notebook and board state reset locally; do not promise saved investigation reasoning. |
| `SocScene.tsx` shares one room, mission labels/accents and the same stage artifacts with 2D. | Keep useful mode parity and fallback; 30 games do not mean 30 distinct worlds or unique investigation mechanics. New tasks should be available from either mode without requiring walking or WebGL. |
| `api/mission_routes.py` saves stage decisions, scores and feedback under owned runs; review is optional and nonpersistent. | Preserve the existing scoring/history contract. The API does not enforce reading every artifact and the client inspection gate is UX, not an integrity boundary or mastery measure. |
| `api/mission_contract.py` publishes manifest version 1; guides have separate revisions, while `MissionRun` does not pin a complete content snapshot. | Do not rewrite existing scored stages/keys in place. Additive practice must have explicit content revisions; changing scored content later needs a separate version/preservation design. |

The remaining expansion is deeper evidence reasoning and verification, rather than catalogue count or missing briefings. Distinct titles, source assertions and synthetic browser journeys do not establish independent educational value.

## Tutor inventory and prerequisites

A tracked-source search for `tutor`, `Yoruba`, `Igbo`, `openai` and `chat/completions`, followed by inspection of API router registration (`api/main.py`), frontend pages, models and dependency manifests, found **no implemented web/API tutor**, language selector, Yoruba/Igbo teaching content, retrieval corpus, model adapter or tutor evaluation suite. `MODERNIZATION.md` describes curriculum-grounded AI tutoring as a future milestone; it is an older proposal, not an implementation record. The AI Governance mission teaches risk concepts; it is not an AI tutor. Legacy Android remains outside this development scope.

Consequently, “stronger Yoruba/Igbo tutor support” requires a foundation, not merely a prompt change. No external AI provider, model, spend, data transfer or generated translation quality is assumed approved by the roadmap.

| Prerequisite | Required evidence before release |
| --- | --- |
| Curriculum grounding | Versioned, allowlisted references to the three foundations courses, their stable objectives and source lesson links. Do not retrieve private accounts, feedback, attempt answers or unpublished content. |
| Yoruba and Igbo quality | Fluent language reviewers validate meaning, diacritics, technical terminology, age appropriateness and consistency against the English source. Record source revision, locale, review state and review changes. Machine-generated drafts remain unpublished until reviewed. No reviewer approval is currently supplied. |
| Safe help | Age-appropriate defensive explanations; avoid requests for real passwords/codes, personal records or live targets. Separate hints/explanations from hidden assessment/mission keys; refuse unsupported topics and explain limitations. |
| Access and privacy | Reuse actual student/authentication and published/enrolled-course access rules. Derive identity on the server. Minimise retention; avoid free-text chat storage and secrets in logs. |
| Future generative AI | Explicit provider/data/cost decision, bounded requests/output, timeouts, quotas/rate limits, isolation of untrusted retrieved text, safe output rendering and grounded citations. Evaluate injection, sensitive-data requests, harmful/off-topic prompts, unsupported answers and all supported languages before enabling. Deterministic safety templates alone do not validate a future model. |

## Cohesive next build: investigation practice and grounded help foundations

Implement one development release containing the following two related parts. This is the recommended engineering slice within Phase 6, not a claim that all Phase 6 language, learner or security gates can be completed from source alone.

### Six deeper Cyber Academy investigations

Use the approved five-to-six-game batch size. Add distinct optional, server-checked investigation practice to six existing games, within the active guided workspace:

| Game | New practice objective | Evidence/action and explanation |
| --- | --- | --- |
| Network Watch | Correlate network signals without treating periodicity as proof. | Select records supporting a host/time correlation; explain the missing process context. |
| Web Defense | Separate attempted attacks from demonstrated application impact. | Match request, handling and outcome evidence; explain why a detector label alone is insufficient. |
| Cloud Perimeter | Reason about effective access and its limits. | Compare fictional policy/context records; identify the justified exposure conclusion. |
| Forensics Desk | Reconstruct a sequence while preserving time uncertainty. | Order records using a supplied clock offset; explain preservation and uncertainty. |
| Malware Clues | Distinguish an indicator from a supported behaviour conclusion. | Link static clues to the supported hypothesis; explain what execution evidence is absent. |
| Identity Lab | Review effective privilege against lifecycle approval. | Reconcile role, end-date and approval records; identify proportionate authorised action. |

Practice should use static synthetic record IDs and bounded selections, with server-owned keys and per-choice explanations. Bind requests to the owned active run/current stage and allowlisted practice revision; reject other users, wrong stages, unknown IDs, malformed/oversized input and submitted scores/keys. Withhold private answer keys. Practice is ungraded and nonpersistent for this first slice; label its limits clearly and keep saved mission decisions/score as the existing progress record. Return explanations after a practice check, independently of the original scored finding. Do not use the new practice to silently alter legacy score opportunities or completion requirements.

Render the practice in the shared workspace so switching 2D/3D retains one task/run. Test keyboard/touch, focus, errors/retry, duplicate submission, small screens and no-WebGL recovery. Do not simply reconnect the old themed fallback components and claim deeper learning.

### Curriculum-grounded tutor foundation

Start with a clearly labelled **guided study helper** using curated topic/question choices and deterministic, source-linked explanations for Python Foundations, Cyber Safety Foundations and Digital Citizenship. This establishes useful grounding without inventing a live AI integration. It must not be described as open-ended AI chat. Keep assessment answer keys and mission finding keys outside the response corpus.

Use an explicit locale/revision/review-state contract. English can ship after content checks; Yoruba/Igbo entries remain unavailable with a clear English fallback until fluent review is recorded. An empty locale must never produce fabricated translations or a claim of supported tutoring. Structure content for subsequent reviewed language additions. Do not publish provisional Yoruba/Igbo prose merely to fill a language selector.

The helper and investigation practice should share plain explanations of evidence limits and source references, while keeping their authorization/content rules separate. No provider keys, new external calls, automatic content publication or schema migration are needed for this bounded foundation.

## Verification and release gates

Before handing over the implementation:

1. Run backend content/HTTP and isolated PostgreSQL checks for ownership, student/course access, bounded input, non-disclosure, unchanged existing scores/history and valid source/revision references. Exercise incomplete/historic runs and failure paths.
2. Run frontend unit/type/build checks and the existing 30-game matrix. Add focused desktop/mobile browser cases for the six new activities and helper navigation, unsupported locales, focus/error recovery and mode parity. Include real-API persistence/reopening and logout; intercepted replies alone are insufficient for backend claims.
3. Supply one complete development update/test/restart/acceptance guide after verified source delivery. Include publication/migration commands only if implementation later makes them necessary. Preserve beta and existing Phase 5 behavior.
4. Keep fluent Yoruba/Igbo review, independent beginners/physical devices, accessibility, operational recovery/capacity and final formal security assurance as separate open gates. No automatic beta promotion.

## Evidence from this inspection

- Fresh local clone: correct branch, clean working tree at `9950eed` before documentation edits; no `AGENTS.md` found in tracked source. No owner runtime or database was accessed.
- Executed Python imports/inventory checks using only static catalogue/mission/guide modules: 30 games = 30 missions = 30 guides; ten per pathway; 90 stages; 260 artifacts; 150 review questions; artifact counts match engine evidence at every stage; active public guidance withholds review until completion. The initial scratch probe incorrectly assumed exactly three artifacts per stage; corrected checks use each stage’s actual count. This was a probe assumption, not an application defect.
- Seven dependency-free frontend assertions passed. The full Node unit invocation could not load two test files because TypeScript is not installed in this fresh checkout; pytest is also unavailable. No new full unit, typecheck, build, browser, PostgreSQL or dependency-audit pass is claimed. Earlier Phase 5 CI evidence remains historical and unchanged.
- Documentation-only checkpoint. No application/dependency/schema/content publication changes, security audit execution or user-facing installation required.

**Next action:** implement the six-game investigation practice and deterministic study-helper foundation above as one development build; keep Yoruba/Igbo publication gated on fluent review and generative AI disabled pending its separate prerequisites.
