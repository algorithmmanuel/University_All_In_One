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
