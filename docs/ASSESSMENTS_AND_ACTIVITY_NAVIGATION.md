# Assessment length and activity navigation

Approved by the owner as the next bounded build on 26 October 2026. Development branch only; beta deployment is a separate release decision.

## Learner behaviour

Select an enrolled course, then choose Quick (5), Standard (10), Extended (20) or a Custom whole number. Presets larger than the available bank are disabled. Custom supports 1 through the available number of unique prompts, capped at 100. Small banks default to a valid custom length. The displayed estimate uses approximately one minute per question; there is no timer or enforced duration.

Starting a test loads exactly the selected count. Submission requires all selected answers. Results and history show the question count with the score/percentage. Short attempts provide less evidence of mastery; this build records the necessary denominator and explains the limitation, but does not add a mastery/recommendation algorithm.

Opening or reopening a course, starting/resuming a mission, choosing an assessment course and starting its test move the viewport and keyboard focus to the loaded activity heading. Reduced motion uses an immediate scroll. Headings have scroll margin for navigation clearance. Merely answering a question, completing a lesson or receiving a mission decision does not trigger this opening behaviour.

## Server contract and integrity

- `GET /api/v1/quizzes/courses/{id}/options` requires a student enrolled in a published course and returns the available unique question count and supported preset counts.
- `GET /api/v1/quizzes/courses/{id}?question_count=N` returns the server-selected questions without solutions. Invalid or unavailable sizes return 422.
- `POST /api/v1/quizzes/courses/{id}/submit` accepts `question_count` and the answer map. The server recomputes the selected set and requires exact equality of question IDs, strict integer answer options and valid option ranges. Missing, extra, unrelated or incomplete question sets are rejected before creating an attempt.
- Scores, explanations and saved totals are computed on the server. A five-question submission cannot claim the denominator of a longer test.
- Omitting `question_count` preserves the legacy full-bank GET/submission contract. This deliberately differs from the new UI's unique-prompt selection.
- Existing QuizAttempt answers, score and total fields support variable sizes. There is no schema migration.

Selection is deterministic across GET and submission. It normalises prompt case/whitespace to avoid repeated wording and spreads selections across the ordered bank, rather than always returning its first N questions. Formal topic/objective balancing requires future question metadata and is not claimed here. The bank should remain stable during a practice attempt; if selected IDs change before submission, the answer-set check fails and the learner must restart. This is a practice feature, not a proctored or randomised exam-session system.

## Implementation

- `api/assessment_selection.py`: pure selection/validation/grading helpers.
- `api/quiz_routes.py`: eligibility, options, questions, grading and saved attempt totals.
- `web/app/assessments/page.tsx`: setup, length validation, questions, results and history.
- `web/lib/activity-focus.ts` and `web/lib/use-activity-focus.ts`: shared focus/scroll behaviour after an explicit successful open.
- Course and mission pages increment the focus trigger only for opening/resuming; background state refreshes do not increment it.

## Verification and limits

Automated checks executed in the assistant workspace:

- 21 HTTP tests in `api/test_assessment_lengths.py` passed using disposable SQLite and a synthetic overridden learner. Authentication, PostgreSQL concurrency and end-to-end login are outside those tests.
- Frontend TypeScript typecheck and all 15 unit tests passed.
- Production build passed with existing CSS alignment compatibility warnings.
- Standalone lint is blocked by missing repository ESLint flat configuration.
- New browser cases in `web/tests/browser/learning-usability.test.cjs` cover desktop/mobile presets and custom counts, result payloads, focus/reduced motion, course reopening and mission resuming. They use intercepted synthetic API fixtures, not the real backend. Browser execution was attempted but blocked before assertions by the workspace's local-socket restriction. Do not mark these cases passed.

## Local acceptance checklist

Run against development only after updating source and restarting its API/frontend:

1. Choose Quick, answer five questions and submit. Confirm the score denominator and saved history are five.
2. Choose Extended and confirm twenty questions are displayed and required.
3. Choose Custom, test blank/zero/fractional/over-limit input, then start a valid size such as seven.
4. Verify new tests do not repeat a normalised prompt and unavailable presets are disabled on small banks.
5. Open and reopen a course; verify focus and viewport movement. Marking a lesson complete should not jump back to the heading.
6. Start, exit and resume a mission; verify automatic navigation. Decisions should not trigger the opening scroll.
7. Repeat key checks on mobile and with reduced motion. Check keyboard focus at the heading.
8. Run the existing development isolation check and confirm beta still responds.

Record results in DEVELOPMENT_STATUS.md. The owner's previous baseline acceptance predates these changes and is not acceptance of this build.
