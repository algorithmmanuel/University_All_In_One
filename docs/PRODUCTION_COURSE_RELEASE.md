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
