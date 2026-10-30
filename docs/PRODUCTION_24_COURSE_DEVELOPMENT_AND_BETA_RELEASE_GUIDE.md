# EduCyber — 24-course development and beta release guide

**Release state: BLOCKED — NOT READY FOR BETA.** This is a safe operational guide, not evidence that the requested complete production content release exists. As of this checkpoint there are **three authored stage-one course manuscripts** and **one additional eight-lesson draft**. The remaining courses and editorial reviews are unfinished. No new production course has been published to the learner database. Do not merge or deploy this branch as the promised 24-course release.

## Scope and acceptance contract

Deliver **24 different courses** mapped to three paths × eight stages, each with eight to twelve independently written 600–1,000-word lessons, original scenarios, worked decisions and answer explanations, a synthesis activity and verified relevant further-reading links. A course with a short summary, title-only lesson or unsourced link does not meet the release specification. Keep reading-only learning viable without requiring games; preserve all current games, API protections, enrollment and assessment history.

Current development artifacts include the syllabus for 21 remaining courses, three Discover manuscripts, an Explorers/Understand draft, and a guarded publisher. The publisher intentionally imports only three original stage-one manuscripts, insists on exactly 24 registered courses, enforces a minimum 600 words per lesson, and uses one database transaction for an approved batch. Therefore it is **expected to reject publication** until the complete manuscripts are present and accepted.

## Stage A — Safe development checkout and dry-run

Use the separate **development** worktree, NOT the beta worktree. Do not copy beta data into development or reset any PostgreSQL volume. From a PowerShell terminal in the *verified* development worktree root:

```powershell
$ErrorActionPreference = 'Stop'
$branch = (git branch --show-current).Trim()
if ($branch -ne 'feature/beta-continuous-improvement') { throw "Wrong checkout or branch: $branch" }
git status --short
if ((git status --porcelain).Count -gt 0) { throw 'Uncommitted changes: review before updating, do not discard.' }
git fetch origin feature/beta-continuous-improvement
if ($LASTEXITCODE -ne 0) { throw 'Fetch failed.' }
git merge --ff-only origin/feature/beta-continuous-improvement
if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed.' }
Push-Location .\api
try {
  python -m unittest test_production_course_manuscript
  if ($LASTEXITCODE -ne 0) { throw 'Manuscript structure tests failed.' }
  # The following command MUST NOT change the development database:
  python publish_production_learning.py
  if ($LASTEXITCODE -ne 0) { throw 'Publisher dry-run validation failed.' }
} finally { Pop-Location }
```

**Expected current result:** The original test suite may pass; the publisher dry-run should report an incomplete registered manuscript set (3/24) rather than writing data. This is not permission to publish. **Never run `--publish` until all 24 fully reviewed manuscripts are registered and a separate database backup, restore test and release acceptance are complete.**

## Stage B — Required engineering and editorial acceptance before any merge

1. Author the **21 remaining full course manuscripts** (168 original lessons) and expand the 3 Discover manuscripts plus the new Understand draft to the required depth. All 24 unique courses need their own verified further-reading list.
2. Integrate the 24-course manifest, stable pathway/stage identity mapping and a complete Browse Courses interface including stage/path selection, lesson navigation, reading progress and resume. Test reading-only learners who never launch a game.
3. Use versioned, additive publication. Protect the existing three demo-course IDs, enrollments, lesson completion, quiz history, beta invitations and test feedback from deletion or renumbering. Demonstrate a repeat publication is idempotent and a failure rolls back all 24 course inserts.
4. Execute unit, API/PostgreSQL, frontend build, browser, security and mobile/accessibility suites. Record exact commit SHAs and links to the successful workflows. Test that all 24 catalog courses open with expected lesson counts and real content, that 24 final reading lists contain checked working URLs and that games/auth remain unchanged.
5. Only after all acceptance evidence is green, open and merge an explicit production-content PR from `feature/beta-continuous-improvement` into `feature/secure-password-recovery` using the verified expected head SHA. A green workflow for an earlier commit is not enough.

## Stage C — Beta rollout only after the complete production-content PR is merged

**These steps are not authorised for the unfinished content release.** Once a completed and tested content PR has actually merged, update the user's existing beta worktree, preserving all local changes. Do not run `git reset --hard`, `git clean`, volume deletion, demo reseeding or database migration without reviewed backups.

In the *verified* beta checkout root, inspect branch and status:

```powershell
$ErrorActionPreference = 'Stop'
$branch = (git branch --show-current).Trim()
if ($branch -ne 'feature/secure-password-recovery') { throw "Wrong beta branch: $branch" }
git status --short
if ((git status --porcelain).Count -gt 0) { throw 'Local modifications must be reviewed before beta update.' }
git fetch origin feature/secure-password-recovery
if ($LASTEXITCODE -ne 0) { throw 'Fetch failed.' }
git merge --ff-only origin/feature/secure-password-recovery
if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed.' }
Write-Host "Beta checkout: $(git rev-parse HEAD)"
```

Once the complete release's own instructions specify its exact publication operation and backup/restore procedure, apply additive content to the existing beta PostgreSQL database **exactly once or idempotently**, confirm all course counts and existing learner progress, then build/restart the beta frontend in its existing terminal (not the development terminal):

```powershell
cd C:\Users\dNA1991\University_All_In_One\web
npm.cmd ci
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
npm.cmd run build
if ($LASTEXITCODE -ne 0) { throw 'Build failed.' }
# Stop the previous beta frontend terminal with Ctrl+C first.
npm.cmd run dev -- -p 3000
```

Keep the development web port 3010 and existing FastAPI/DB deployments independent. Test `http://127.0.0.1:3000/learn`, sign-in, three distinct path filters, all 24 courses, reading progress, existing progress, and the public ngrok tester link. Do not announce a successful public rollout merely because the source branch merged.

## Current outcome and next release blocker

The requested full release **has not been completed or merged**. The development branch has a guarded work-in-progress manuscript publisher; attempting beta promotion now would misrepresent short or missing course content as production quality. The next release must include complete original content, reader interface and passing tests before this guide can be marked completed.
