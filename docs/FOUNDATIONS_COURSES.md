# Phase 3.2 — Cyber Safety and Digital Citizenship

Implemented 27 October 2026 for FB-01 (teaching/assessment alignment), FB-06 (repeated or misplaced questions) and FB-07 (interactive examples). Python remains owner-accepted. The formal audit stays deferred until the end of development.

| Course | Lessons | Focus | Guided checks | Active questions |
| --- | --- | --- | ---: | ---: |
| Cyber Safety Foundations | Recognising phishing; Protecting your accounts; Safer browsing | Independent verification, account protection and safer web/device choices | 6 | 20 |
| Digital Citizenship Essentials | Your digital footprint; Privacy basics; Respectful online conduct | Audience, consent, privacy, trusted help and respectful participation | 6 | 20 |

Each lesson contains three objectives and four teaching sections, including a worked fictional scenario. Every question maps to a taught objective. All 60 maintained questions across these courses and Python have distinct normalized prompts. Digital Citizenship now has its own bank rather than selecting Cyber Safety questions after publication.

Quick (5), Standard (10), Extended (20) and Custom within the available bank remain supported. Each new active bank deliberately contains 20 taught questions, replacing an unrelated 50-question selection. Practice gives option-specific explanations but saves no assessment grade or automatic completion. The learner marks completion explicitly. No real passwords, contacts, school details or incident reports are requested; example hostnames are fictional text. No learner code runs. Account age/guardian policy is unchanged.

## Publication and data compatibility

Pulling source or starting services publishes nothing. The guarded launcher retains its branch, checkout Python environment, development configuration and actual database identity checks. No migration is required.

The shared publisher validates both new courses before changing either. Missing/duplicate courses or lessons, custom lesson content, unpublished courses and conflicting/duplicate question keys stop publication before mutations. Both releases commit in one caller-owned transaction; repeated application inserts no duplicates.

Course/lesson IDs, enrollment, completion, users, feedback, mission records and historical assessment answers/scores/totals are retained. Old question rows and their answer keys remain unchanged. All expected source curriculum markers must match the intended academy/course before the curated assessment bank activates. Clients receive structured guides plus plain text fallbacks. Already-completed lessons remain completed and can be reopened.

Existing `content-preview`/`content-apply` commands remain Python-only. New `foundations-preview`/`foundations-apply` commands publish only Cyber Safety and Digital Citizenship. The Python release is retained.

This is an isolated development release. A later production release still needs a versioned content recovery procedure. Retain source curriculum revisions referenced by stored markers: reverting source alone does not revert publication. Stop development services before applying so no assessment is in progress; leave beta services open.

## Complete PowerShell blocks

Run from the root of the existing development worktree. Preserve local changes if Git refuses an update; do not reset them automatically.

Update and preview:

```powershell
$ErrorActionPreference = 'Stop'
$curriculumBranch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $curriculumBranch -ne 'feature/beta-continuous-improvement') {
    throw 'Open the existing development worktree first.'
}
git pull --ff-only origin feature/beta-continuous-improvement
if ($LASTEXITCODE -ne 0) { throw 'Update failed; preserve and inspect local changes.' }
& .\api\.venv\Scripts\python.exe .\scripts\development.py foundations-preview
if ($LASTEXITCODE -ne 0) { throw 'Preview failed; do not apply.' }
```

After a successful guarded preview, update the two existing dependencies to the reviewed pins and apply:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe -m pip install 'certifi==2026.10.19' 'filelock==4.2.1'
if ($LASTEXITCODE -ne 0) { throw 'Development dependency update failed.' }
& .\api\.venv\Scripts\python.exe .\scripts\development.py foundations-apply
if ($LASTEXITCODE -ne 0) { throw 'Publication stopped; do not continue to acceptance.' }
```

Focused checks with disposable in-memory state; this block restores the terminal's prior database settings:

```powershell
$ErrorActionPreference = 'Stop'
$curriculumPreviousDatabaseUrl = $env:DATABASE_URL
$curriculumPreviousTestUrl = $env:TEST_DATABASE_URL
try {
    $env:DATABASE_URL = 'sqlite+pysqlite:///:memory:'
    $env:TEST_DATABASE_URL = ''
    Push-Location .\api
    try {
        & .\.venv\Scripts\python.exe -m pytest test_foundations_courses.py test_python_foundations.py test_assessment_lengths.py test_development_isolation.py -q
        if ($LASTEXITCODE -ne 0) { throw 'Focused checks failed.' }
    }
    finally { Pop-Location }
}
finally {
    $env:DATABASE_URL = $curriculumPreviousDatabaseUrl
    $env:TEST_DATABASE_URL = $curriculumPreviousTestUrl
}
```

Restart development API in one terminal:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py api
if ($LASTEXITCODE -ne 0) { throw 'Development API stopped.' }
```

Restart development frontend in another terminal:

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

1. Open both courses. Confirm the heading scrolls into view and all three expanded lessons appear without visible curriculum markers.
2. Read phishing and privacy/consent worked scenarios. Check that the courses teach distinct goals and that a beginner can explain the examples without developer help.
3. In all six lessons choose a wrong practice answer, then a correct one. Confirm specific explanations, no saved grade, no automatic completion and no scroll back to the course heading.
4. Use keyboard Tab/Enter. The active control should remain focusable while waiting; repeated activation should not duplicate requests. A new answer should clear its old feedback. Check mobile width and reduced motion.
5. Mark a lesson complete and refresh. Existing completion/enrollment must remain. Reopen Python and verify its accepted lessons and results still work.
6. Try 5, 10, 20 and custom assessment lengths in both courses. Check taught content, distinct prompts, accurate saved totals/scores and explanations. Old attempts must retain previous totals/scores.
7. Re-run preview: publication should require zero new question rows afterward. Confirm beta availability. Share only sanitized errors, never secrets or learner records.

## Verification and CI maintenance

Local backend collection: 179 passed, 20 database-dependent skips, 11 subtests passed. HTTP feature checks use synthetic SQLite and overridden identity, not full authentication or PostgreSQL-lock proof. All 15 existing frontend unit tests, TypeScript and production build passed; existing CSS alignment warnings remain. Dependency consistency and pip-audit passed in a clean environment after updating its own pip bootstrap.

Four new desktop/mobile browser scenarios were added. Local Chromium cannot create a required UNIX socket, so local browser assertions are not counted as executed. CI execution is pending at this source checkpoint; later results belong in DEVELOPMENT_STATUS.md.

Earlier CI found an ambiguous Password locator and practice focus loss caused by disabling the active control. The locator now matches exactly. Pending practice uses a synchronous request guard and accessible busy/disabled states without removing focus. The browser harness installs separately from application dependencies to preserve the application lockfile.

The existing dependency gate reported certifi/filelock advisories. CI lock pins and input floors now use certifi 2026.10.19 and filelock 4.2.1; other locked versions are preserved. These are routine checks and fixes, not a resumed formal audit or proof of deployed exploitability. No owner database, beta service or mail provider was tested.

## Content review references

The wording and fictional scenarios are original. Core principles were cross-checked against these primary sources on 27 October 2026. Lessons do not load their pages, providers or trackers at runtime.

- [CISA Secure Our World](https://www.cisa.gov/secure-our-world)
- [CISA software update guidance](https://www.cisa.gov/secure-our-world/update-software)
- [UNICEF Nigeria: protecting children online](https://www.unicef.org/nigeria/protecting-children-digital-world)
- [UNICEF: understanding and responding to cyberbullying](https://www.unicef.org/stories/how-to-stop-cyberbullying)
- [PyPA certifi advisory](https://github.com/pypa/advisory-database/blob/main/vulns/certifi/PYSEC-2026-4320.yaml)
- [Filelock maintainer release 4.2.1](https://github.com/tox-dev/filelock/releases/tag/4.2.1)

Next: owner development acceptance and beginner walkthroughs, then Phase 4 mission clarity/interaction improvements. Formal audit remains deferred to the end of development.
