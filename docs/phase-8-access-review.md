# Phase 8 — Learning and gameplay authorization review

## Authorization invariants
- Learners can access only their own mission runs, scores, and histories.
- Learners must enroll in a published course before viewing its lessons, marking progress, or taking quizzes.
- Draft courses are unavailable to students regardless of previous enrollment.
- Quiz grading and mission scoring use server-side answer keys, not browser-submitted scores.
- Teachers cannot access student-only endpoints simply because they are approved.
- Missing and unauthorized mission-run IDs should both return 404, limiting object enumeration.

## Regression evidence
`api/test_access_boundaries_http.py` uses real HTTP endpoints and isolated PostgreSQL `educyber_test` to test cross-account object access, course enrollment, draft visibility, teacher restrictions, quiz score injection, and missing-resource handling. It cleans up temporary records.

## Remaining release gates
- Verify the new HTTP integration test and complete backend suite locally.
- Confirm GitHub Actions success on the latest commit; CI currently runs database-independent tests, not PostgreSQL integration tests.
- Add PostgreSQL service-backed integration CI and a secret-scanning gate.
- Review database migration status for each deployment environment.
- Review browser/frontend authorization handling and conduct a security-focused release assessment.
