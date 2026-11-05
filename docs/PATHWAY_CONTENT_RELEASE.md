# Three distinct pathways across eight stages

30 October 2026. Owner-authorised continuation from `a6cbe8e` on `feature/beta-continuous-improvement`. The owner clarified that switching pathways must offer different actual material, rather than the same activity at a harder setting. This supersedes the shared-content recommendations for this bounded development release. It does not authorise unverified beta promotion or waive independent educational/device/security gates.

## Core content matrix

The eight stage names and engines remain shared. Core materials are allocated exclusively between pathways, with separate introductions and existing authored cases. General libraries, saved history and direct experienced entry stay available; choosing to browse another pathway does not delete or rewrite any record.

| Stage | Cyber Explorers | Cyber Academy | Cyber Command |
| --- | --- | --- | --- |
| Discover | Six original everyday-security questions | Six original technical-boundary questions | Six original governance/assurance questions |
| Understand | Digital Citizenship, Cyber Safety, Protect the branch module | Defend connected services module; optional Python | Respond, recover and assure module |
| Check understanding | Fundamentals, phishing, identity, endpoint pools (200 existing questions) | Network, application, cloud pools (150 existing questions) | Governance, response, recovery pools (150 existing questions) |
| Investigate with guidance | Ten Explorer missions | Ten Academy missions | Ten Command missions |
| Manage consequences | Defend the branch | Supplier Access Crisis | Recovery Under Pressure |
| Command an incident | The reconnection decision: focused saved workshop | Branch Siege: full eight-asset capstone; clinical-containment workshop | The urgent executive change: focused saved workshop |
| Face an opponent | Ledger Under Pressure (microfinance) | Open Bucket, Closed Doors (software/cloud) | The Maintenance Window (third-party access) |
| Compete and reflect | Night Shift Outage (hospital) | Instructions in the Evidence (AI service) | The Trusted Session (payment/insider) |

Stage eight uses a different scenario from stage seven within each pathway, with solo role reversal or optional two-learner play. A hospital scenario is an introductory asset/service trade-off in the Explorer route, not clinical training. Scenario industry and audience are not age/access permissions. Stage six for Explorers and Command is explicitly a workshop, not a newly built full simulation. This release reorganises the existing games; it creates no new engine or revised game rules.

## Exclusive workshop allocation

One existing saved workshop per stage per pathway: eight per pathway, 24 overall. Previously all three stage workshops appeared for every audience. Workshop source, original IDs, authored consequences, owned history and replay snapshots are unchanged.

| Stage | Explorers case | Academy case | Command case |
| --- | --- | --- | --- |
| Discover | The scholarship deadline | The shared computer | The surprise approval |
| Understand | An invoice that still opens | The changing role | The backup dependency |
| Check | Which session is still alive? | The rule below the allow | The encrypted public file |
| Investigate | Two clocks, one alert | The midnight export | The supplier's assurance |
| Manage consequences | The patching window | The payment trust path | Close the recurring door |
| Command | The reconnection decision | Containment on the night shift | The urgent executive change |
| Opponent | Two orders, one round | Predict the trust crossing | The foothold that changed |
| Reflect | Ready for the second learner | The response that disappeared | The second playthrough |

These are teaching allocations rather than assertions that all concepts are exclusive to one audience. Related security principles recur through different records and decisions. Reuse within a pathway is deliberate; no case is a core allocation in two pathways. The all-pathways view is explicitly combined browsing, not a fourth campaign. General assessment and match-history screens remain shared utilities, rather than repeated core learning materials.

## What changes and what stays compatible

- `web/lib/learning-journey.ts` owns the reviewed allocation: teaching, topics, missions, workshops, defender and two Red/Blue scenarios. Core destinations differ across pathways at every stage. Scenario titles match the actual catalogue.
- The preview has 18 new explained questions (six per pathway). The general public sample remains available separately. It is local, unsaved and advisory; changing the pathway remounts the preview and clears answers so they cannot be scored against another bank.
- Stage workshop cards and the workshop chooser respect the pathway allocation. Deliberate general browsing and all previously owned history remain accessible. The command workshop appears once, not duplicated as two activities.
- The final-stage page offers Explorers → Academy → Command onward navigation. This is an invitation after the learner's challenge, not an automatically awarded completion or mastery credential. Existing activity results remain saved in their original tables. A new cross-activity completion engine, prerequisites, certificates and automatic unlocking are outside this bounded content-organisation release.
- No API/backend, model/schema, migration, published bank, workshop content, original guide, game engine/rule, auth/session or dependency change. No database rows are rewritten. No new publication command or migration is required for an already installed beta bundle. Revert the frontend source and restart development to recover from this navigation change; do not roll back learner databases.

## Complete development update/check blocks

Stop only the development API/frontend with Ctrl+C; keep beta running. Use the existing development worktree. Preserve local generated declarations, local Compose configuration and unrelated changes.

```powershell
$ErrorActionPreference = 'Stop'
$pathwayBranch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $pathwayBranch -ne 'feature/beta-continuous-improvement') {
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
    if ($LASTEXITCODE -ne 0) { throw 'Production build failed.' }
}
finally { Pop-Location }
```

Start development API in one terminal, from the development root:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py api
if ($LASTEXITCODE -ne 0) { throw 'Development API stopped.' }
```

Start development frontend in another terminal, from the development root:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py web
if ($LASTEXITCODE -ne 0) { throw 'Development frontend stopped.' }
```

Verify and open the journey in a third terminal, from the development root:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py check
if ($LASTEXITCODE -ne 0) { throw 'Development isolation verification failed.' }
Start-Process 'http://127.0.0.1:3010/journey?stage=discover&pathway=secondary'
```

## Acceptance and verification

1. Compare all eight stages across the three pathways against the matrix. The actual case, module, topic pool, mission set or scenario must change, not just difficulty or colour. All-pathways browsing should remain clearly labelled.
2. Complete each pathway's six-question preview. Check distinct questions, explanations, advisory onward links and no saved grade. Back/reload must retain pathway context; changing pathway must not reuse another preview's answers.
3. Open allocated workshops and select All stages: exactly eight allocated cases appear for that pathway. Browse all explicitly to see the complete library. Reopen older owned attempts and replay without changing their content or history.
4. Check the three defender scenarios, Academy Branch Siege, six Red/Blue allocations, 2D/3D guided missions and ordinary saved results. Stage six Explorer/Command must clearly identify its workshop format. No activity may start merely from navigation.
5. At stage eight, follow the next-pathway link; confirm the new material begins at Discover and no completion/mastery is awarded by that click. Test keyboard, mobile width, reduced motion and logout.

Local checks passed: 24 frontend unit tests, TypeScript and production build. New unit cases verify all 24 workshop IDs/stages against actual source, disjoint topic/scenario allocations, distinct core destinations after removing context parameters, and 18 unique explained preview questions. Browser cases added for all pathways on desktop/mobile, every stage, previews, onward navigation and actual-API workshop filtering. CI is pending at this checkpoint; no local browser success or fresh full backend result is claimed. The known local full-Chromium socket restriction remains. No owner laptop, beta database or services were operated.

Beta promotion remains separate. PR #4 tracks the earlier navigation work and now shares the development branch with this explicitly authorised broader content allocation; do not merge an earlier checked head or imply that its prior CI validates these edits. Obtain complete current-head regression evidence and record the release scope before a separately authorised promotion. Formal audit stays deferred; independent content/learning/device and operational gates remain open.


## Verified API/browser follow-up — 30 October 2026

Corrected source `002b680` passed [actual-API/PostgreSQL browser run 41050824395](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/41050824395): all 30 cases passed. These include the three new actual-catalogue pathway filters plus all 27 previous API/game/workshop journeys, persistence, separate sessions and safe acknowledgement retries. Initial runs failed on a real same-page onward-navigation bug and test-entry/wait assumptions; corrections and their causes are recorded in status. The broader browser gameplay gate is pending at this follow-up checkpoint. No owner local acceptance, beta promotion or independent educational result is implied.


## Final automated verification

Implementation `002b680` passed [browser quality run 41050824453](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/41050824453): all 24 progression/journey browser cases and all 132 gameplay cases (156 total), 24 frontend unit tests, TypeScript and production build. Together with the 30 actual-API/PostgreSQL cases above, all required automated gates for this frontend/content-allocation release are green. This supersedes earlier pending-CI statements. Owner development acceptance and independent educational/device/operational/final-security evidence remain separate. No beta promotion or owner runtime operation was performed.
