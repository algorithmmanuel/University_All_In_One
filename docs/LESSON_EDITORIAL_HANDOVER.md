# Lesson editorial handover — 31 October 2026

**Scope:** development manuscripts only, `feature/beta-continuous-improvement`. Keep beta unchanged and publication blocked. No database operations, publisher execution or editorial approval signatures are authorised by these edits.

## Recovered checkpoint and baseline

Fresh checkout had no uncommitted changes. Remote development head was `befb040926d25c21945ebfbaafb664e2d066e9c2`; `658c357ae15b52f72be611beb483ff475ebe8ade` is an ancestor and documents the batch workflow. The audit implementation was introduced earlier in `d5dff93`; audit regression expectation was later corrected in `d077094`. The two initial Stage 7 revisions are present and preserved exactly. The historical 677-window CI count is superseded by the fresh local baseline below. Earlier status headings describing only six manuscript courses are historical: the present source has 24 draft courses and 192 lessons, with editorial acceptance still incomplete.

Read `api/audit_production_learning.py`, `api/test_audit_production_learning.py`, `api/test_production_course_manuscript.py`, the publication-boundary tests, the course release guide and curriculum plan before continuing. Audit counts are exact normalised-token signatures, grouped by adjacent matches; they are **not counts of duplicated paragraphs**. A clean exact-text audit does not establish semantic originality or educational acceptance.

## Completed batch evidence

| Checkpoint | Global repeated 70-word signatures | Global passage clusters | Course outcome |
| --- | ---: | ---: | --- |
| Fresh baseline at `befb040` | 468 | 15 | Stage 7: six affected lessons; Stage 8: four cross-course matches despite its historical within-course pass |
| Explorers Stage 7 completed | 345 | 7 | All eight reviewed; six rewritten; neither Stage 7 nor Stage 8 remains in the exact-overlap inventory |

Stage 7 lessons 1–2 are byte-for-byte equivalent in parsed content to the recovered checkpoint. Lessons 3–8 now have 653, 666, 638, 650, 656 and 663 words. They teach interruption fatigue, trust boundaries in an attack chain, reversible decisions under uncertainty, secondary recovery fraud, coordinated reporting and bounded counterfactual reasoning. Each includes distinct explanation, a fictional worked case and an exercise with reasoning. All course metadata, lesson titles, positions and relationships are preserved. No application code or assessments changed.

Local checks for this batch: four audit regressions passed; manuscript suite **16 passed, one failed**, solely the remaining whole-library 70-word overlap gate (345 signatures). Exact substantive-paragraph gate and all depth/structure tests passed. Preservation comparison passed for course metadata, lesson identities and both completed revisions. No fresh passing CI is claimed. Publication boundary test initially could not import SQLAlchemy in this fresh environment; rerun after installing the pinned test requirements and record the actual result.

## Reference review

On 31 October, web retrieval of NCSC `https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online` succeeded. It supports optional background on separate email passwords, two-step verification, updates and backups, and is labelled accordingly in Stage 7 lesson 8. CISA `https://www.cisa.gov/secure-our-world` returned HTTP 403; it is not represented as verified and was removed from this revised course's reading list. No source prose was copied. Human editorial review, browser accessibility and broader reference/licensing checks remain release requirements.

## Next work and acceptance hold

Next unfinished course in pathway/stage audit order: **Cyber Academy Stage 2 — Understand, lesson 1**, `api/production_learning/academy_understand.py`. Complete all eight lessons before moving on. Academy Stage 4 Investigate and Stage 5 Defend are independently assigned with separate file ownership in this session; they are not complete until centrally reviewed and validated. Re-run the global audit after each course and record its exact snapshot. The largest remaining families are shared Academy evidence prompts and Command banking decision prompts; replace them with subject-specific instruction, not word substitutions.

Publication remains blocked until both uniqueness gates pass globally, all 24 manuscripts receive substantive independent review and source validation, genuine hash-bound approvals exist, the full CI/reader/PostgreSQL-preservation gates pass, and release is authorised. Do not merge into beta, publish, reseed or alter learner records. CI runs may be pending or failing; distinguish their actual state from local checks.


## Completed batch: academy_defend

Reconstructed service objectives, network flow matrices, workload privilege, monitoring pipelines, deployed patch evidence, restoration checks, bounded containment and retry-safe resilience exercises. The central review checked the distinction between authentication/authorisation, network permission/application authority, backup availability/restoration integrity and timeout/commit uncertainty.

All eight lessons reviewed; word counts: 649, 646, 643, 637, 643, 649, 627, 694. Metadata, schema, titles and lesson positions match the prior committed course exactly. Per-course structure/depth and global exact-match exclusion checks passed; `git diff --check` passed. Proposed-commit global audit: **345 → 343 signatures**, **7 → 7 clusters**. The audit includes all 24 courses / 192 lessons and excludes other in-progress agent edits. A shared passage remains counted while any two other lessons still contain it. Snapshot: `docs/content-audit/2026-10-31-academy-defend.json`. No automatic human approval or fresh green CI is implied.

References: NIST CSF https://www.nist.gov/cyberframework and OWASP Top 10 https://owasp.org/projects/top-ten were opened and relevance checked on 31 October; these are optional overviews, not deployment prescriptions. Independent editorial/licensing acceptance remains open.

Exact next unfinished audit course: **academy_understand, lesson 1** (complete all eight lessons; source `api/production_learning/academy_understand.py`). Parallel assignments are provisional until their individual reviewed batches are recorded here. Beta, databases and publication block remain unchanged.

Dependency follow-up: installed repository-pinned CI requirements in an isolated temporary Python environment. All **five** publication-boundary negative tests passed with a nonconnecting in-memory URL; tests mock approvals and make no publication/database calls. The earlier missing-SQLAlchemy import blocker is resolved.


## Completed batch: academy_investigate

Reconstructed hypothesis testing, dependency scope, timezone-aware timelines, identity versus committed-action evidence, network/process correlation, evidence handling, bounded assessments and testable debrief recommendations. Central review checked the J8 recalculation case, explicit UTC conversions, account-versus-human attribution and limits of absent logs; none of these repeats the defensive-engineering exercises.

All eight lessons reviewed; word counts: 704, 720, 684, 716, 721, 734, 718, 782. Metadata, schema, titles and lesson positions match the prior committed course exactly. Per-course structure/depth and global exact-match exclusion checks passed; `git diff --check` passed. Proposed-commit global audit: **343 → 327 signatures**, **7 → 3 clusters**. The audit includes all 24 courses / 192 lessons and excludes other in-progress agent edits. A shared passage remains counted while any two other lessons still contain it. Snapshot: `docs/content-audit/2026-10-31-academy-investigate.json`. No automatic human approval or fresh green CI is implied.

References: NIST SP 800-61 Rev. 3 https://csrc.nist.gov/pubs/sp/800/61/r3/final and OWASP Logging Cheat Sheet https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html were opened and checked for incident-response and logging relevance on 31 October. Independent editorial/licensing acceptance remains open.

Exact next unfinished audit course: **academy_understand, lesson 1** (complete all eight lessons; source `api/production_learning/academy_understand.py`). Parallel assignments are provisional until their individual reviewed batches are recorded here. Beta, databases and publication block remain unchanged.
