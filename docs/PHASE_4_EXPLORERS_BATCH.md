# Phase 4.3 — Six Cyber Explorers games

Implemented 28 October 2026 following owner-reported Phase 4.2 acceptance and approval to work in batches of five to six games. This release improves six existing games for FB-02, FB-04 and FB-05; it does not add games or complete Phase 4.

## Scope and content review

| Game | Stage-specific learning | Five review concepts |
| --- | --- | --- |
| Privacy Patrol | Public profile address; album audience/location; quiz permissions | Data purpose; location exposure; resharing limits; contacts relevance; declining unnecessary access |
| Scam Spotter | Advance-fee prize; claimed bank caller; off-platform sale | Test payments; code screenshots; independent bank contact; platform protections; urgency |
| Safe Social | Unknown follower; repeated harmful messages; copied friend account | Routine exposure; boundaries; private evidence; trusted help; independent verification |
| Device Defender | Official update; shared session; elevated attachment | Update route; restart planning; retained sessions; privilege impact; approved file reporting |
| Wi-Fi Wise | Lookalike hotspot; public connection; certificate warning | Network identity; HTTPS limits; warnings; shared-device sessions; VPN limits |
| Digital Footprints | Photo consent; old profile; misleading post | Publication permission; onward sharing; old contact/routine details; correction; removal limits |

Each game adds three goals, three tasks, six contextual hints, detailed fictional records matching every existing evidence index, finding reasoning after decisions and five explained optional questions. Every review concept is taught in its stage records. Across this batch there are 18 stage tasks, 36 hints and 30 new review questions. Nine of the 30 existing games now use the guided pattern; 21 remain to improve. This is a content/interaction coverage count, not evidence of educational effectiveness.

The six data modules are `privacy_mission_learning.py`, `scam_mission_learning.py`, `social_mission_learning.py`, `device_mission_learning.py`, `wifi_mission_learning.py` and `footprint_mission_learning.py`. They register through the existing static allowlist and share the accepted API and UI. The three previously accepted guide modules are unchanged.

Specific wording and scenarios distinguish related skills: Safe Social covers supportive behaviour and impersonation, while Digital Footprints covers consent and public traces; Privacy Patrol covers audience/permissions; Wi-Fi Wise distinguishes transport protection from destination trust. Reinforcement is intentional. Exact normalized prompt duplication is checked across all 45 guided-mission questions; this is not a semantic review of every course bank.

## Security, scoring and deployment

The shared ownership, student-role, completion and strict-input review checks remain. The server selects review questions using the owned run's mission ID. Reviews cannot change scores, completion, other learners' data or select another mission's answer bank. Finding explanations appear after decisions; public guidance omits answer keys. Inspection is a learning UI aid, not server proof of reading.

Existing mission IDs, step order/count, answer/finding keys and points are unchanged. Historic partial/completed runs retain stage, choices, scores and feedback; new guidance is additive. No migration, seeding or curriculum publication is needed. The release activates in development after source update and service restart. It does not promote anything to beta. Source rollback/restart recovers this additive release; there are no new persisted review records to reverse. Existing published course markers still require their separate recovery policy.

2D remains the default lightweight mode. Both modes open the same stage records and share inspected state and finding selection within that stage. Walking is optional and the existing 3D error boundary permits return to 2D. No real personal routines, images, credentials, financial details or harmful messages are requested. No actual network is joined, external link followed, software elevated or file executed. Content avoids guarantees about privacy controls, HTTPS, VPNs, refunds or the outcome of reporting.

## Complete PowerShell update and checks


Stop only development API/frontend using Ctrl+C. Leave beta open. Run from the existing development worktree root.

```powershell
$ErrorActionPreference = 'Stop'
$missionBranch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $missionBranch -ne 'feature/beta-continuous-improvement') {
    throw 'Open the existing development worktree first.'
}
git status --short
git pull --ff-only origin feature/beta-continuous-improvement
if ($LASTEXITCODE -ne 0) { throw 'Update failed; preserve and inspect local changes.' }

$missionPreviousDatabaseUrl = $env:DATABASE_URL
$missionPreviousTestUrl = $env:TEST_DATABASE_URL
try {
    $env:DATABASE_URL = 'sqlite+pysqlite:///:memory:'
    $env:TEST_DATABASE_URL = ''
    Push-Location .\api
    try {
        & .\.venv\Scripts\python.exe -m pytest test_mission_learning.py test_mission_contract.py test_foundations_courses.py test_python_foundations.py test_assessment_lengths.py test_development_isolation.py -q
        if ($LASTEXITCODE -ne 0) { throw 'Focused development checks failed.' }
    }
    finally { Pop-Location }
}
finally {
    $env:DATABASE_URL = $missionPreviousDatabaseUrl
    $env:TEST_DATABASE_URL = $missionPreviousTestUrl
}

Push-Location .\web
try {
    npm.cmd test
    if ($LASTEXITCODE -ne 0) { throw 'Frontend unit checks failed.' }
    npm.cmd run typecheck
    if ($LASTEXITCODE -ne 0) { throw 'TypeScript check failed.' }
}
finally { Pop-Location }
```

Start API in one terminal from the development root:

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
```

## Acceptance across all six games

Open http://127.0.0.1:3010/missions and select Cyber Explorers. Test Privacy Patrol, Scam Spotter, Safe Social, Device Defender, Wi-Fi Wise and Digital Footprints.

For **every game**:

1. Confirm the role/goals, workflow, completion conditions and current task are clear. Open both hints using keyboard controls. Records must match that game's current story rather than a generic reused scenario.
2. In each stage inspect all records, choose a finding and choose/commit an action. Read feedback, including after an incorrect choice. Confirm each stage resets inspection/selection and that duplicate submission does not advance twice.
3. Finish in 2D, then check a stage in 3D on a supported device. Switch modes after inspection and confirm preserved inspection/finding state. Verify the displayed record content is identical. Walking must be optional and 2D must remain available if 3D fails.
4. Try wrong and correct answers to the five review questions. Check option-specific explanations, cleared old feedback on selection changes, stable keyboard focus, duplicate blocking and retry after an error. Saved mission scores must not change.
5. Reload and view the completed result; resume an older incomplete run if available. Existing scores/history must remain intact. Reopen the three accepted games and foundation courses for regression checks.

Use desktop/mobile and reduced-motion settings across the batch. A full real-device performance study is not established by testing a toggle or a synthetic viewport. Record sanitised device/problem details if an interaction fails.

Independent beginner checks should include whether a learner can finish without developer help and explain one decision in each game: why an address is sensitive; why a small test payment is still a risk; why evidence should stay private; why sign-out matters; what HTTPS does not prove; and why photo permission matters. Preserve those educational/device gates even if automated checks pass.

## Verification checkpoint

Backend tests cover all nine guides through actual HTTP handlers using synthetic SQLite and overridden identity: stage scoring, all review options, historic runs, ownership/role/completion/input boundaries, cross-mission question rejection and key non-disclosure. The legacy 30-mission completion check remains. These local HTTP tests do not establish full authentication or PostgreSQL lock behaviour.

The browser matrix automatically selects every registered guide: 36 journeys (nine games × desktop/mobile × 2D/3D) use actual static stage content with intercepted API responses. One browser process is reused with a fresh context per case to reduce batch overhead while isolating storage and request mocks. API-only edits now trigger this browser job because mission content drives the UI. No dependency pins changed.

Local checks passed: 289 backend tests and 11 subtests (20 database-dependent skips), 15 frontend unit tests, TypeScript, production build and pip check. Existing warnings remain as applicable. The local Chromium UNIX-socket limitation remains; real-browser execution belongs to CI. Later verified test counts, CI links and their limits are recorded in DEVELOPMENT_STATUS.md. Owner acceptance of this new batch, independent learner evidence, complete real-backend browser journeys and final assurance remain separate gates. The formal Cloudflare audit remains deferred until the end of development by owner instruction. No owner database/computer, beta source/services or mail provider was accessed.

Next: verify CI, update/restart development with the blocks above and perform this six-game acceptance checklist. Continue in batches of five to six after acceptance, keeping each game's learning/evidence distinct.

### Subsequent CI verification

Implementation `4e5df28` passed [backend run 40654992864](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40654992864): 309 tests and 11 subtests against isolated PostgreSQL, plus unit/dependency checks. [Browser run 40654992839](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40654992839) passed all 48 browser cases, including the 36 guided-mission desktop/mobile × 2D/3D journeys, as well as 15 frontend unit tests, TypeScript and production build. Browser API responses are synthetic; these checks do not establish a complete real-backend browser journey. Owner acceptance of this six-game batch and independent beginner/actual-device evidence remain pending.
