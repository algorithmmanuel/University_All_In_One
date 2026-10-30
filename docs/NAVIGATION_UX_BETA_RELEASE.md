# Consolidated navigation UX release — beta promotion gate

**Owner approval:** 30 October 2026. One coherent navigation and onboarding release; ongoing beta testing is desired. **Do not change existing games.** This is frontend-only; no database migrations or changes to gameplay engines are intended.

**Review:** [Pull request #4](https://github.com/algorithmmanuel/University_All_In_One/pull/4) targets `feature/secure-password-recovery` from `feature/beta-continuous-improvement`. It must remain a draft until acceptance evidence exists.

## Included

- Start Here / Help explanation and persistent navigation.
- Different recommended starts and purpose descriptions for Cyber Explorers, Cyber Academy and Cyber Command; existing eight stages still open to everyone.
- An optional shared six-question introduction on `/preview`, away from the homepage games catalogue.
- End-of-preview score, explanation review, retry and *advisory* next-stage navigation; guest answers remain unsaved.
- Plain-language action labels.

## Mandatory verification before beta merge

In the *development* worktree, first inspect local changes and protect generated files; do not reset, clean or force changes. Stop/restart **development** only while running tests. From the development root:

```powershell
$ErrorActionPreference = 'Stop'
$branch = (git branch --show-current).Trim()
if ($branch -ne 'feature/beta-continuous-improvement') { throw 'Not in the development branch.' }
git status --short
git pull --ff-only origin feature/beta-continuous-improvement
if ($LASTEXITCODE -ne 0) { throw 'Cannot fast-forward: preserve and inspect local changes.' }
Push-Location .\web
try {
  npm.cmd test
  if ($LASTEXITCODE -ne 0) { throw 'Frontend unit tests failed.' }
  npm.cmd run typecheck
  if ($LASTEXITCODE -ne 0) { throw 'TypeScript typecheck failed.' }
  npm.cmd run build
  if ($LASTEXITCODE -ne 0) { throw 'Frontend production build failed.' }
} finally { Pop-Location }
```

Run the repository's existing Playwright, API/PostgreSQL and workflow checks for the development environment using their maintained documented commands, and record exact pass counts and run links in DEVELOPMENT_STATUS.md. Confirm: guest /help; 3 distinct selected Discover recommendations; 8-stage later entry; /preview displays exactly 6 questions and never the 30-game library; each question explains a submitted answer; completion stops rather than cycling; correct/review explanation lists; retry; low/high score suggestions; optional override; keyboard focus and mobile; browser back and direct reload; assessment state never transfers between signed-in browser sessions; prior game library, workshops, courses, auth, game routes and saved progress unchanged.

### Safe beta source promotion

Promote **only after** all required CI and actual-browser gates pass and review confirms the changed files exclude gameplay. Use the draft PR to review the complete diff and mark it ready, then merge into the beta source with its exact verified head SHA. Verify the resulting beta branch SHA. Beta **source** merge does not update the running app on the owner's Windows laptop.

### Owner laptop rollout

Use the existing two-worktree workflow. Verify beta backup and active branch before pulling `feature/secure-password-recovery`; never merge development configuration, database volumes or secrets. Because this change is frontend-only, do not run an Alembic migration or reset data. Stop/restart **only the beta frontend** per existing beta instructions and check beta on port 3000, API health on port 8000 and the ngrok-facing site. Leave development on 3010 and its isolated database unchanged. Confirm existing testers can access the same beta address, their accounts and progress persist, and no existing games changed. Record exact operator evidence independently of CI.

## Current state

UX source and documentation committed to development. **No verified test results or beta source promotion at this checkpoint.** The draft PR is not evidence of readiness. Follow up with CI and operator checks before merge.
