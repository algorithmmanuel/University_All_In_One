# One learning journey — development release

29 October 2026 (Africa/Lagos). Development only: `feature/beta-continuous-improvement`. No beta promotion.

## Learner experience

The homepage and student dashboard lead to `/journey`. New learners can start from stage 1; experienced learners can choose any stage directly. Cyber Explorers, Cyber Academy and Cyber Command tailor suggested materials within the same eight-stage journey. Audience choice is navigation guidance, not an account role, age verification or permission grant.

| Stage | Existing materials |
| --- | --- |
| Discover | Public two-question preview and foundation-course starting point |
| Understand | Maintained foundation courses, applied Cyber Lab modules and optional Python |
| Check understanding | Selectable-length assessments, relevant topic practice and mistake review |
| Investigate with guidance | Existing pathway-filtered 30-mission catalogue and its 2D/3D views |
| Manage consequences | Defend the branch, Supplier Access Crisis and Recovery Under Pressure |
| Command an incident | Branch Siege, supporting response/recovery study and existing replay/comparison |
| Face an adaptive opponent | Red/Blue computer setup, with suggested scenario/seat/difficulty |
| Compete and reflect | Two-human Red/Blue setup, saved matches and participant debriefs |

Every stage remains available. Python is optional. No score, skill level, completion, prerequisite or certificate is inferred from opening or navigating the journey. Existing progress panels and direct collection links remain available. Saved records stay in their existing authenticated activities.

Shared navigation data is in `web/lib/learning-journey.ts`; the hub and compact home/dashboard entry reuse it. Pathway/stage choices use allowlisted URL values and browser Back/reload. Resource links carry advisory `journey_stage`/`journey_pathway` context, so account-based activity return links open the right stage. Global navigation also provides a general hub entry. Unknown values fall back safely. Direct stage entry and deliberate stage changes use the existing reduced-motion-aware focus helper.

Existing pages accept only bounded, known suggestion values: a foundation course is highlighted/sorted first if actually present; practice topic/difficulty/mistake mode and Red/Blue scenario/seat/opponent/difficulty are preselected. Nothing automatically enrols, submits practice, starts a mission or creates/joins a match. Authentication, eligibility, match ownership, hidden-state filtering, scoring and all saved content/rules remain unchanged. Saved-match anchor focus waits for asynchronous content to render.

No backend, migration, dependency or content publication change is required. No external generative AI, new languages or instructor access is introduced.

## Complete PowerShell update and checks

Stop **only development** API/frontend terminals with Ctrl+C. Leave beta running. Run from the existing development worktree root. Preserve the generated `web/next-env.d.ts`, local `compose.development.yaml` and any other unrelated local changes. This release adds no migration; the previously accepted simulator schema `0012_red_blue_matches` remains required.

```powershell
$ErrorActionPreference = 'Stop'
$journeyBranch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $journeyBranch -ne 'feature/beta-continuous-improvement') {
    throw 'Open the existing development worktree first.'
}
git status --short
git pull --ff-only origin feature/beta-continuous-improvement
if ($LASTEXITCODE -ne 0) { throw 'Update failed; preserve and inspect local changes.' }

Push-Location .\web
try {
    npm.cmd test
    if ($LASTEXITCODE -ne 0) { throw 'Frontend unit checks failed.' }
    npm.cmd run typecheck
    if ($LASTEXITCODE -ne 0) { throw 'TypeScript check failed.' }
    npm.cmd run build
    if ($LASTEXITCODE -ne 0) { throw 'Frontend build failed.' }
}
finally { Pop-Location }
```

Start API in its own terminal from the development root:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py api
if ($LASTEXITCODE -ne 0) { throw 'Development API stopped.' }
```

Start frontend in another terminal from the development root:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py web
if ($LASTEXITCODE -ne 0) { throw 'Development frontend stopped.' }
```

Verify in a third terminal from the development root:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py check
if ($LASTEXITCODE -ne 0) { throw 'Development isolation verification failed.' }
Start-Process 'http://127.0.0.1:3010/journey'
```

## One acceptance pass

1. On the homepage, choose **Begin my journey**. Confirm the Discover stage opens and the public preview works. On the dashboard, confirm the journey is prominent and all existing saved-progress panels remain available.
2. Choose an audience, then change stages. New learners have a clear stage 1; every audience can still choose Branch Siege or Red/Blue directly. Reload and use Back; the selected stage/pathway should remain consistent with the URL.
3. Open a suggested foundation course. The recommendation should identify an actually available course, or explain its absence. It must not enrol automatically. Python remains an optional branch.
4. Open suggested topic practice and a guided mission library. Check the topic/difficulty/pathway selection, then use **Learning journey** to return to the relevant stage and audience. Navigation must not create attempts or change scores.
5. Open computer and two-human Red/Blue setup from stages 7/8. Check scenario, opponent, seat and difficulty; starting remains a separate deliberate action. Reopen saved matches/debriefs and an existing Cyber Lab run.
6. Check keyboard focus, a narrow viewport, reduced motion, logout and old courses/assessments/missions/progress. Report confusing wording or links. Navigation preferences do not establish learning gains or mastery.

## Evidence and recovery

Unit tests cover all 32 stage/audience combinations, safe fallbacks, internal resource destinations and return context. New browser journeys cover public/offline discovery, beginner/experienced entry, audience changes, focus, Back/reload, foundation suggestions and no automatic writes. Actual-API journeys check mission/practice/match selections, return context and async saved-history focus. Full source/CI results are recorded in DEVELOPMENT_STATUS.md.

Prefer a forward fix. This is frontend navigation only: no database rollback, learner-data deletion or rule-edition change is needed. Independent learner comprehension, physical-device usability, educational/balance evidence and deferred final security/operational gates remain open. Owner instructions remain necessary before any beta promotion.


## Verified release evidence — 29 October 2026

Source `1f23cfacffebba8b4baa2d109af433a9b36f3111` passed [browser quality CI 40889524297](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40889524297): **150 browser cases** (all 147 previous cases plus three journey cases), **18 frontend unit tests**, TypeScript and production build. [Real API/PostgreSQL CI 40889524360](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40889524360) passed **24 cases** (all 22 previous plus two journey cases). Local combined browser verification passed 31 selected cases, with desktop/mobile screenshots inspected; exact scope is in status.

All automated gates for this frontend navigation release are green. No backend/schema/dependency/content changes were introduced. Owner update/restart/acceptance and independent learner/physical-device/operational/final-security evidence remain pending. Beta is unpromoted and unchanged.
