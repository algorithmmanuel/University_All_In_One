# Phase 3.1 — Python foundations pilot

This build addresses FB-01 (lesson/assessment alignment), FB-06 (repeated or unrelated questions), FB-07 (interactive learning) and FB-08 (variables/conditions examples). It is the first Phase 3 pilot; Cyber Safety Foundations and Digital Citizenship still need their own content review. The owner deferred the formal security-audit-skill stage until the end of development. Ordinary secure coding, review and regression checks continue.

## Learner experience

The existing Introduction to Python course keeps its three lesson IDs. Each lesson now has three named objectives, four teaching sections, worked examples with expected output, and two prediction checks with option-specific explanations. Variables cover reassignment/types/conversion; conditions cover comparisons, thresholds, branches and indentation; loops cover sequence/range/while/termination/accumulation/break/continue. All examples are text; learner code is never executed.

Practice checks are low stakes. They never create an assessment attempt or mark a lesson complete. The enrolled learner explicitly marks completion as before. Choice changes and feedback do not scroll/focus the course workspace again. The screen reader feedback region announces the explanation. Existing plain text lessons still render.

Twenty reviewed assessment items map to the nine taught objective IDs in `api/python_foundations.py`. Quick (5), Standard (10), Extended (20) and Custom within the available bank remain supported. The bank uses application questions, varied trace scenarios and explained answers. This pilot deliberately replaces the active 50-question miscellaneous Python selection with 20 taught questions after explicit publication. Longer does not mean repeating the same question to fill a quota.

## Publication and data compatibility

Nothing is published by app startup or by pulling source. The guarded development launcher reads only its existing local development configuration and enforces its branch/venv/database checks. No migration or dependency change is required.

`api/publish_python_foundations.py` previews or atomically applies the release to the seeded university Python course. It refuses missing/duplicate courses, missing/duplicate/customized lesson content and conflicting question answer keys. Course row locking serializes this publisher. Repeated application adds no duplicates.

Stable text markers in the existing lesson content column select the reviewed source curriculum. Only the maintained academy/course identity and all three matching lesson markers activate the curated bank. API responses resolve these markers into teaching content and an optional structured `learning_guide`. Plain text `content` remains available for older API consumers. Practice answer keys stay server-side; assessment keys are revealed only through existing submission feedback.

Old question rows and all attempt answers/scores/totals remain stored. No old question is deleted or has its answer key rewritten. Lesson/course IDs, enrollments, completion records, users, feedback and mission records are retained. Completed lessons remain completed; learners can reopen them for the richer explanations. This is a development content release, not a beta deployment or a production rollback procedure. Before a later production release, version the content activation/recovery process and preserve every referenced curriculum revision; a source rollback alone does not revert database markers.

## Complete PowerShell blocks

Run from the root of the existing **development worktree**, using its `api/.venv`. Stop its development API/frontend before updating. Leave tester-facing beta services running. Local setup/credentials are not recreated by these commands. If Git refuses the update, stop and inspect the reported local changes; never reset them automatically.

Update and preview:

```powershell
$ErrorActionPreference = 'Stop'
if ((git branch --show-current).Trim() -ne 'feature/beta-continuous-improvement') {
    throw 'Open the development worktree first.'
}
git pull --ff-only origin feature/beta-continuous-improvement
if ($LASTEXITCODE -ne 0) { throw 'Git update failed; preserve and inspect local changes.' }
& .\api\.venv\Scripts\python.exe .\scripts\development.py content-preview
if ($LASTEXITCODE -ne 0) { throw 'Content preview failed; do not apply.' }
```

After a successful preview, apply explicitly:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py content-apply
if ($LASTEXITCODE -ne 0) { throw 'Content publication stopped; inspect the safe error message.' }
```

Restart the development API in one terminal:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py api
if ($LASTEXITCODE -ne 0) { throw 'Development API stopped.' }
```

Restart the development frontend in a second terminal:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py web
if ($LASTEXITCODE -ne 0) { throw 'Development frontend stopped.' }
```

Verify in a third terminal:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py check
if ($LASTEXITCODE -ne 0) { throw 'Development isolation verification failed.' }
```

## Acceptance checklist

1. Open My learning, enroll in or reopen Introduction to Python. Confirm the course heading receives focus and the page scrolls to it.
2. Read variables, conditions and loops. Check that all worked examples show expected output, with readable wrapping/scrolling on mobile.
3. In each lesson choose an incorrect practice answer, check its explanation, choose the correct answer and check again. Nothing should mark the lesson complete or add an assessment score. Keyboard focus should remain usable; feedback should be announced.
4. Mark a lesson complete; refresh/sign in again and confirm completion remains saved. Previously completed lessons must stay completed after publication.
5. Open the Python assessment. Try 5, 10, 20 and a custom length. Questions should test taught concepts without exact repeated prompts. Submit a mix of correct/incorrect answers; confirm explanations and the actual selected total are saved.
6. Check an old attempt: its score and total remain unchanged. Open a different course: its existing content and bank are unchanged.
7. Check reduced-motion behavior, mobile width, keyboard navigation and continued beta availability. Report the first error with a sanitized message; never share credentials or raw learner data.

## Verification recorded in assistant workspace

- 45 focused backend tests passed, plus 11 unittest subtests, using synthetic SQLite and mocked identity. Includes actual practice/quiz HTTP handlers, idempotent publication, conflicting/customized content refusal, preserved records, strict input checks and existing assessment/isolation regressions. No PostgreSQL concurrency or full authentication claim.
- All 15 existing frontend unit tests passed; TypeScript typecheck and production Next.js build passed. Build retains the pre-existing CSS alignment compatibility warnings.
- Two desktop/mobile browser cases were added and wired into the browser workflow alongside existing learning usability cases. Chromium launch is blocked here by a required socket operation denied by the execution environment; browser assertions remain unexecuted.
- Full backend collection was attempted but stopped because the available workspace environment lacks Alembic. It is not a full regression pass. CI dependencies already declare Alembic.
- Browser/backend workflows now include this development branch. Backend CI's isolated PostgreSQL host port is aligned with the existing password-recovery test refusal guard; this configuration change was inspected but not executed here.
- No owner database, beta service, mail provider or live account was accessed. Publication and owner acceptance remain pending.

Next: owner development acceptance of this pilot, then the same objective/content/assessment review for Cyber Safety Foundations and Digital Citizenship. Formal audit resumes at the end of development against the changed source.
