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

## GitHub acceptance evidence — 30 October 2026

The PR #4 initial head `a2c5105` ran three CI workflows after marking the PR ready for review:

- [Frontend quality gate 41039843563](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/41039843563): **passed**.
- [Real API browser integration 41039843610](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/41039843610): **failed** (25 passed, 2 failed); both journey tests expected the prior `Open Cyber Academy investigations` label.
- [Browser gameplay quality gate 41039843708](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/41039843708): **failed** (15 passed, 3 failed in the named journey suite); journey tests expected prior `Open Practise governance` and `Open Cyber Safety Foundations` labels.

The new labels unexpectedly broke existing selectors, not game rules. The scoped fix at `252fc3b` restores familiar `Open <activity>` labels while continuing to avoid the owner's redundant `Open Try…` and `Open Browse…` combinations. **Re-run/verify all workflows on the updated head before merging.** Prior CI results cannot be reused as proof of a later commit. No laptop deployment or beta merge is implied.

## Final verified source release — 30 October 2026

**Release source promotion COMPLETE:** [PR #4](https://github.com/algorithmmanuel/University_All_In_One/pull/4) merged into `feature/secure-password-recovery` at commit `bf6a850af9b128d6e347563a71402b1830142c92`. The verified PR head was `a6cbe8ecfcbad9f9f85fb667f39e4ffc07642b41`; expected-head SHA protection was used on merge. The source branch comparison before merge showed 24 ahead, 0 behind, with changes limited to help/journey/preview/navigation/test/documentation files. No game engine or database content was changed.

**Final acceptance CI for exact verified head:**

- [Frontend quality gate 41041880908](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/41041880908): **SUCCESS**; 22 frontend unit tests passed, 0 failed (plus frontend gate).
- [Real API browser integration 41041880756](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/41041880756): **SUCCESS**; 27 browser/API cases passed, 0 failed.
- [Browser gameplay quality gate 41041880904](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/41041880904): **SUCCESS**; 22 unit tests, 18 focused browser cases and 132 broader browser cases passed, 0 failed in each reported suite.

### Required owner beta laptop deployment — frontend only

**Source is merged; the beta currently running on the owner's Windows laptop has NOT been updated by GitHub.** Apply in the **beta checkout**, not the development checkout, after verifying that the running beta and development terminals/directories are distinguishable. Preserve all unrelated local changes, secrets, databases and tester records. Stop only the beta web terminal (Ctrl+C), not the beta API or development frontend/API. From the beta checkout root:

```powershell
$ErrorActionPreference = 'Stop'
$branch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $branch -ne 'feature/secure-password-recovery') {
    throw 'Wrong checkout: expected the beta branch.'
}
git status --short
# If there are locally modified tracked files, STOP and inspect them before pulling.
if ((git status --porcelain) -match '^ [MADRUC]|^[MADRUC?]') {
    throw 'Local changes require review before pull; do not reset, clean or stash blindly.'
}
git fetch origin feature/secure-password-recovery
if ($LASTEXITCODE -ne 0) { throw 'Fetch failed.' }
git merge --ff-only origin/feature/secure-password-recovery
if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed; investigate without force.' }
$head = (git rev-parse HEAD).Trim()
Write-Host "Beta source checkout commit: $head"
Push-Location .\web
try {
    npm.cmd ci
    if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
    npm.cmd run build
    if ($LASTEXITCODE -ne 0) { throw 'Frontend build failed.' }
} finally { Pop-Location }
```

Restart the beta frontend **in its existing terminal and using the same beta environment variables** (default command from the beta checkout `web` directory: `npm.cmd run dev -- -p 3000`). Do **not** run migrations, wipe volumes, change API settings or change the development web port 3010. Confirm `http://127.0.0.1:3000/help`, `http://127.0.0.1:3000/preview`, `http://127.0.0.1:3000/journey`, and `http://127.0.0.1:8000/health` return expected pages/healthy response. Confirm the existing ngrok tester link still resolves to the beta frontend. Test all three pathway choices and a six-question completion, and verify an existing tester can sign in and resume prior progress. Do not treat this checklist as completed operator evidence until the laptop has actually been updated and checked.
