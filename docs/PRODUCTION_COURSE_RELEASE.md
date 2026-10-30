# Production 24-course content release — architecture and publication audit

**Date:** 30 October 2026. **Status: in development, not ready for beta.** The owner has authorised a single complete release followed by merge to ongoing beta, with game changes explicitly excluded.

## Verified source inspection

- `api/models.py`: `Course` has integer ID, academy ID, title, description and draft/published status. `Lesson` has integer ID, course ID, title, plain-text content and position. `Enrollment` references immutable course IDs and `LearnerProgress` references lesson IDs. Deleting or recreating published courses/lessons would strand or alter historical progress.
- `api/seed_learning.py`: exactly three idempotently seeded demonstration courses, three short lessons each. The script inserts only missing courses/lessons. Existing courses and completion records are left untouched.
- `api/learning_routes.py`: public published-course catalogue; authenticated student enrollment; lesson access requires enrollment; completing a lesson writes per-user progress and has idempotent handling.
- `api/curriculum_registry.py` and `api/learning_content.py`: existing reviewed teaching releases (Cyber Safety, Digital Citizenship, Python). A lesson guide is selected by its course identity and exact content marker; merely seeding course titles is insufficient for full guided lessons, and marker/version collisions could break active assessments.
- `web/app/learn/page.tsx`: currently shows enrolled courses and a general course catalogue with lessons, progress and enrollment. It does not yet represent a 3-path × 8-stage production course catalogue with verified further-reading links.

## Release implementation requirements

1. Author 24 **individually reviewed** courses from `PRODUCTION_LEARNING_LIBRARY_PLAN.md`, with 8–12 substantial lessons per course, original prose, worked examples, checks, case studies and further reading. No filler or demo text may be labelled production.
2. Give every course a stable unique identity and explicit pathway/stage mapping. Decide versioning and content metadata before migration; never reuse an existing course's ID for a different course.
3. Write additive, idempotent publishing logic. Do not execute `seed_learning.py` as a replacement/migration mechanism for the new library. Preserve current three courses until audited enrollment/progress migration policy is approved; do not delete them.
4. Verify the actual authoritative public URLs and licensing/relevance. Keep link labels, provider, topic and last-verification date with the authored course.
5. Implement the reading-focused `Browse Courses` catalogue and course reader. Ensure existing `foundation` and journey links still work; stage/pathway suggestions must use actual published course IDs rather than fictional hard-coded IDs.
6. Write PostgreSQL preservation tests to compare pre/post enrollment, lesson progress, attempts and existing course/lesson IDs. Validate zero duplicate publications after repeated runs, zero score resets, guest/account access behavior and session isolation.
7. Test editor/readability/accessibility/mobile, all 24 course lesson loads, navigation/progress, external links and regression of auth, workshops, missions and Red/Blue. Run existing frontend, browser and real-API workflows.
8. Promote one coherent *verified* release to `feature/secure-password-recovery`, using expected-head merge protection, then provide the owner's Windows beta update, content publication, post-update verification and non-destructive recovery instructions.

## Explicit current limits

No production course data has been published, no full 24-course editorial acceptance has been performed, no beta database or server has been touched, and the content merge remains pending. The project must not claim the 24-course release complete simply because this publication architecture has been inspected or because the catalogue displays 24 titles.

**Next development action:** produce the 24 unique lesson manuscripts and reference checks, then implement content publication and reader integration together. Preserve the running ongoing beta until the full quality gate is green.

## Editorial implementation checkpoint — 30 October 2026

The current source includes the **first original eight-lesson manuscript** for Cyber Explorers / Discover at `api/production_learning/explorers_discover.py`. It covers risk recognition, independent verification, account protection, privacy, misinformation, device hygiene, incident response and a personal safety plan. The final lesson contains curated links as editorial leads that still require link/source checking. A guarded command `api/publish_production_learning.py` defaults to dry-run validation; `--publish` is an explicit additive insert with identity/content collision checks and no modification to existing learner courses or lesson IDs.

**This is one of 24 courses and is not a complete 24-course content release. No publication command has run and the new course is not live.** The remaining 23 substantial course manuscripts, content QA, automated tests, links and complete release gates are outstanding. Do not merge this partial work into beta or state that 24 courses exist. Keep the beta running and preserve enrolled learners' records.

## Three distinct Discover manuscripts authored — 30 October 2026

Development now contains three individually authored stage-one courses (8 lessons each; **24 lessons total, not 24 courses**): `api/production_learning/explorers_discover.py`, `academy_discover.py`, and `command_discover.py`. The three courses target different concepts: everyday digital safety and decisions; networks/identity/cloud evidence; and organisational risk/control governance. They share a pedagogical Discover stage but not identical text. New structure checks were added in `api/test_production_course_manuscript.py`. The guarded publisher now knows these three authored courses and **rejects `--publish` until the complete 24-course manifest exists**, preserving the current beta and enrolments. No publisher execution, CI success or beta deployment has been claimed for these commits. The remaining 21 course manuscripts, verified external reading links, editorial review, reader UX and end-to-end tests are outstanding. No actual game code changed.


## Remaining 21-course editorial architecture — 30 October 2026

Added [21-course syllabus with 168 distinct chapter requirements](PRODUCTION_REMAINING_21_COURSE_SYLLABI.md), mapped to the remaining seven stages for all three audience pathways. This is a complete **chapter-level curricular specification**, not the 168 full lessons themselves; it is deliberately not counted as production published content. The three prior Discover manuscripts remain the only authored course manuscripts. The publisher still blocks premature 24-course rollout, and beta remains untouched. Full-length lesson manuscript writing, independent fact-checks, verified further-reading URLs, course reader UX, database preservation and CI are outstanding. Do not merge partial materials into beta.


## Repository access verification — 30 October 2026

The existing GitHub connection successfully read this file; publication remains prohibited until the complete curriculum and test gates are met. This checkpoint verifies the development branch only and does not indicate beta deployment.


## Development continuation — 30 October 2026

GitHub read/write verified on the development branch (checkpoint `3685c42`). The guarded publisher now commits an entire approved 24-course batch in one transaction, or rolls back all writes on failure (commit `e89092e`), avoiding partial library publication. A fourth course draft, **Cyber Explorers / Understand — Accounts, Privacy & Secure Online Habits**, has eight original lesson drafts in `api/production_learning/explorers_understand.py` (commit `408d93d`). Their roughly 130–150-word bodies are **below the agreed 600–1,000-word editorial lesson standard** and are deliberately *not* registered for publication. Three earlier Discover manuscripts also need editorial-depth review. This is ongoing writing, not production content or a release. There is no beta merge, publication execution or learner-data change.


## Catalogue placement correction — 30 October 2026

The owner confirmed that **all 24 distinct production courses belong under the existing `My learning` → `Course catalogue` heading**, not on a separate website or in the games area. Development commit `387cba96` defines the approved 24-title allowlist; commit `ad8c3a59` renders only actually published matching courses there, with all three pathway filters. Three historical demo courses are preserved in a separately labelled `Existing courses` section with enrolment and progress untouched. This is **placement engineering only**, not a claim that 24 published courses exist. The remaining manuscripts, database publishing, testing and beta source promotion are pending; do not announce completion.


## Full-length manuscript checkpoint — 30 October 2026

Expanded `api/production_learning/explorers_understand.py` to **eight individually written lessons of 603–638 whitespace-counted words**, covering sensitive account information, passwords/recovery, MFA, data sharing, permissions, link verification, account recovery and practical routines. Added an explicit content-length test in `api/test_production_course_manuscript.py` (source commit `806b193`). This is a meaningful manuscript milestone, **not** finished editorial verification: references need independent validation and the full course needs reviewer assessment. No new course has been published because the guarded release manifest still contains only three prior Discover courses, which themselves have too-short content for the final 600-word publication rule. The remaining 20 course manuscripts are not complete, and the three Discover courses require expansion. No CI or beta merge is claimed.


## Cyber Explorers Stage 3 draft — 30 October 2026

Created `api/production_learning/explorers_check.py` with eight original, topic-specific **drafts** for Spotting Scams, Misinformation & Manipulation (pressure and impersonation, evidential reliability, source dates, payment scams, emotional manipulation, images and captions, safe reporting, verification reflection). Added a manuscript structure test. **These drafts are currently 127–170 words each, below the mandatory 600-word lesson minimum**, and are intentionally not included in the publishable 24-course manifest. This is manuscript development, not a completed production course. Source commit `2d4690a`; structure test commit `b3da7dd`. The existing production catalogue and beta are unchanged; full curriculum authoring, editorial validation and release CI remain pending.


## Substantial manuscript and reader checkpoint — 30 October 2026

Five of the 24 approved courses now have **eight individually written lessons of at least 600 words each** (40 substantial lesson drafts): Cyber Explorers / Discover, Understand and Check; Cyber Academy / Discover; Cyber Command / Discover. The other 19 course manuscripts remain unwritten at the approved full depth, so the 24-course release is **still blocked**, regardless of earlier syllabus completeness. The guarded publisher now audits five course manifests (`dad6f59`), requires exactly three paths × eight stages, contiguous lesson positions, unique course identity, the 600-word minimum, and one atomic database transaction (`4e3a837`). No content has been published to an application database. The learner-facing existing Course Catalogue filters to actually published approved titles, preserves old demo enrolments separately, and renders safe HTTPS external reading references as hyperlinks in long lessons (`a8d0aad`). A [draft PR #5](https://github.com/algorithmmanuel/University_All_In_One/pull/5) is open for early CI only and is explicitly **not approved for merge**. All source URLs and editorial quality still require review; CISA web pages return 403 to automated browsing, so accessibility from users' browsers must be checked rather than assuming link validation. Existing beta remains unchanged.


## Deep manuscript checkpoint — 30 October 2026

Six distinct course manuscripts now have eight originally authored lessons each (48 lesson drafts; each lesson at least 600 words): Cyber Explorers stages 1 Discover, 2 Understand, 3 Check understanding and 4 Investigate; Cyber Academy stage 1 Discover; Cyber Command stage 1 Discover. Original full-length content, examples and reflective tasks were committed under `api/production_learning/`. The six are registered for **read-only editorial audit** by the guarded publisher (source `820f11c`); source tests include a 600-word requirement and the new guided-investigation manuscript (`2ce925e`). Other 18 course manuscripts and independent editorial/source verification are **outstanding**. No content has been deployed to any database or beta site. The production-only Course Catalogue UI and HTTPS further reading links are developed but have not been accepted by full CI. A draft [PR #5](https://github.com/algorithmmanuel/University_All_In_One/pull/5) is open solely for early validation and must NOT be merged until 24/24 substantive courses, verified source URLs, preservation tests and green CI gates are satisfied. The owner requested one coherent release, not 6 partial courses on beta.


## Course Catalogue eight-stage navigation — 30 October 2026

Added an eight-stage selector to the **existing** My Learning → Course catalogue, alongside three pathway filters. `web/lib/approved-course-catalog.ts` binds each of the exact 24 approved titles to its correct academy and stage without schema migration; `web/app/learn/page.tsx` displays only titles actually returned as published by the API, without falsely showing missing courses. Existing three demo courses remain accessible separately, preserving their enrolment/progress. Unit assertions added in `web/tests/production-course-catalog.test.cjs`. Source commit `a1e198b7`; CI four workflow checks were queued at the time of inspection and cannot yet be claimed green. Six full manuscripts (48 lessons) have been drafted; 18 course manuscripts and independent source/editorial review remain outstanding. PR #5 is draft and not ready for beta merge.
