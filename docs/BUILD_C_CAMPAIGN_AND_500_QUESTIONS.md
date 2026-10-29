# Build C — 500-question learning and campaign release

29 October 2026 (Africa/Lagos). Branch: `feature/beta-continuous-improvement`. Owner reported Build B tests passed and then instructed “go on”. This guide is the single development update/check/restart/acceptance handover for Build C. It does not promote the tester-facing beta.

## Delivered scope

- **500 distinct cybersecurity question records**, 50 per topic family. Added 250 original questions to the existing 250, rather than counting mission reviews, reordered answers or archived rows. Each topic has 20 foundational, 20 applied and 10 challenging questions. Sessions remain 1–20 questions, server-selected and graded, with saved snapshots and recent-mistake review.
- Broader coverage includes asset handling and risk tradeoffs; phishing delivery and consent; federation and credential lifecycle; routing, firewall order and network attribution; firmware, mobile permissions and sanitisation; browser sessions, password storage, CSRF, SSRF, uploads, deserialization and CSP; cloud management/data boundaries, scoped URLs and storage lifetime; evidence handling/detection chains; recovery chains/failback; governance, sampling and supplier dependencies.
- All three learning modules move to **`cyber-lab-v3`** with 30 additional short teaching sections, ten interactive ungraded reflections and 500 worked decisions. The worked library displays five at a time with previous/next navigation. Reflection feedback is local teaching: it creates no practice score, campaign credit or comprehension claim. Learners can change their choice and reconsider.
- **Three-chapter campaign overview** links module reading, supporting practice and the existing scenario outcomes. Suggestions do not lock games. Current-edition read markers are self-reported; practice milestones count distinct questions submitted, including incorrect answers, in up to 50 recent completed sessions selected by session ID. Five is a navigation target, not a pass mark. Window membership can change as newer sessions are submitted, so coverage milestones can decrease; this is not a permanent qualification. Saved game wins aggregate all owned runs, including legacy branch runs beyond history pagination. Replays do not create new distinct scenarios.
- **Asset list alternative** uses the same game controls without map panning. Keyboard selection, an inspector shortcut, visible focus and 44-pixel minimum buttons support navigation. Text distinguishes encrypted service from detected compromise, and buttons for unaffordable actions are disabled while their costs remain visible. Map, legend, briefing and reduced-motion behaviour remain available.
- Dashboard and landing page show the 500-question bank. Direct development route remains `/cyber-lab`.

The game still has three scenarios on the same six-asset map, not a new world or a claim of ThreatGEN parity. This is a learning/progression/accessibility release. No AI, language additions, external runtime model calls, new app dependencies, content publisher or schema migration. Existing migration head remains `0011_strategy_learning`.

## Preservation and authority

The original 250 complete question objects have a frozen SHA-256 regression check (`6a97d479cfc4014ec9a9f82addb687d20ed14eb4300e2e4c2bd3dcf69681eb46` for sorted-key JSON), covering IDs, revisions, labels, options, grading, explanations and original source metadata. Both original question files and all strategy rule files are unchanged. New question IDs run `topic-26` through `topic-50` with new revision `cyber-lab-v3`; they have decision-level objective IDs mapped to their worked teaching cases. Existing broad topic objective IDs are not rewritten.

Prior practice sessions grade from their stored snapshot, even after publication changes. Earlier read-completion editions remain stored and displayed as earlier editions. The new module edition is not silently marked read. Historical course, mission, assessment and game records remain intact.

Campaign guidance is derived from owned server records. No campaign-write or client-achievement endpoint exists. Counts are bounded practice evidence and server-aggregated game state, not browser-supplied points. The catalog query reuses the bounded graded window already used by mistake review. Strategy totals aggregate in the database, avoiding loading all run states. Existing ownership checks, command deduplication, expected versions, creation limits and transaction protections remain unchanged. Runtime actions remain fictional and perform no live target activity.

## Content and public reading review

New records were checked for duplicate prompts/IDs/options, balanced difficulty/topic counts, matching teaching cases, complete explanations and source mappings. Drafts repeating earlier decisions were replaced with additional concepts; later challenging distractors were revised toward plausible mistaken approaches rather than cosmetic alternatives. Deliberate reinforcement remains across recall, applied decisions and consequence analysis. Automated checks and author review are not independent educator validation; ambiguous or misleading material must be reported and versioned without rewriting old results.

References are optional links to primary public sources, not copied reading documents. Existing reviewed NIST CSF, MITRE phishing/segmentation/software-update, OWASP authentication/authorization and NIST incident-response/recovery/cloud references remain. Older 2010/2011 NIST material is explicitly background, not current vendor configuration instructions. New advanced OWASP links below were checked on 29 October 2026 and mapped to the application questions and lesson reading list:

| Reference | Covered teaching |
| --- | --- |
| [Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) | Cookies, lifetimes and fixation |
| [Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) | Salts and work factors |
| [CSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) | Automatically attached credentials and unwanted actions |
| [SSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) | Server destinations and redirects |
| [File Upload](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) | Paths, storage, content and processing limits |
| [Deserialization](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html) | Constrained data versus unsafe object reconstruction |
| [Content Security Policy](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html) | Enforcement versus report-only observation |
| [Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) | Useful context and sensitive-data minimisation |

The core explanations are included in EduCyber. A learner need not leave the app to finish them. Public access is not permission to reproduce complete documents; new teaching/questions are original writing. Source mappings and review dates live in `cyber_curriculum_v3.py` and versioned question metadata.

## Complete PowerShell update, checks and restart

Stop **only development** frontend/API with Ctrl+C. Leave beta running. Run from the existing development worktree root. Preserve local changes. The schema check below uses the existing development-only guard; it is a no-op when the accepted Build A schema is already current. No separate content publication is needed.

```powershell
$ErrorActionPreference = 'Stop'
$buildCBranch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $buildCBranch -ne 'feature/beta-continuous-improvement') {
    throw 'Open the existing development worktree first.'
}
git status --short
git pull --ff-only origin feature/beta-continuous-improvement
if ($LASTEXITCODE -ne 0) { throw 'Update failed; preserve and inspect local changes.' }

& .\api\.venv\Scripts\python.exe .\scripts\migrate_development.py
if ($LASTEXITCODE -ne 0) { throw 'Development schema verification/migration failed.' }

$buildCPreviousDatabaseUrl = $env:DATABASE_URL
$buildCPreviousTestUrl = $env:TEST_DATABASE_URL
try {
    $env:DATABASE_URL = 'sqlite+pysqlite:///:memory:'
    $env:TEST_DATABASE_URL = ''
    Push-Location .\api
    try {
        & .\.venv\Scripts\python.exe -m pytest -q
        if ($LASTEXITCODE -ne 0) { throw 'Backend checks failed.' }
    }
    finally { Pop-Location }
}
finally {
    $env:DATABASE_URL = $buildCPreviousDatabaseUrl
    $env:TEST_DATABASE_URL = $buildCPreviousTestUrl
}

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

## One Build C acceptance pass

Use a synthetic student in development. Open **Cyber Lab** in dashboard navigation or `http://127.0.0.1:3010/cyber-lab`.

1. Inspect **Your campaign**. Existing wins should appear even when older than the first history page. New-edition read markers should start separately from earlier completion. Follow recommendations into learning and supporting practice. Every scenario remains directly selectable regardless of milestone status.
2. In **Learn**, inspect the added teaching steps and **Pause and decide** reflection. Try a wrong answer, read the feedback, change it and check again. Confirm it creates no saved practice session. Open the worked decisions, move forward/back in five-item pages and check the optional advanced application references.
3. Mark a new-edition module read and reload. Confirm persistence without deletion of earlier completion. Submit supporting practice and verify campaign counts distinct submitted questions, not a claimed pass/mastery. Repeating a question does not inflate distinct coverage. Other users must see only their own activity.
4. In **Practise**, verify 500 total, 50 per topic and 20/20/10 difficulty pools. Try foundational, applied, challenging and mixed short sessions. Review an actual saved mistake, then correct it and verify the current review pool. Reopen a pre-Build-C saved session/result and confirm its original questions and grading remain intact.
5. In a game, switch between **Network map** and **Asset list**. Use Tab and Enter/Space to select an asset and execute a valid action. Follow the selected-controls shortcut, inspect costs and encrypted/isolated labels, and reload to confirm server state. Compare desktop and narrow viewport with reduced motion. The list avoids map panning; it is not a guarantee of measured physical-device performance or a complete assistive-technology audit.
6. Resume old branch/supplier/recovery runs and inspect existing mission/course history. Confirm logout, load-error recovery and development isolation. Report content confusion, broken readings, keyboard difficulties or mismatched progress before beta promotion.

## Verification checkpoint

Local full backend checkpoint: **621 passed, 11 subtests passed, 21 PostgreSQL-dependent skips**. After the content-loader readability/validation refactor, all **46 Cyber Lab/Build B/Build C checks** passed. Frontend **15 unit tests**, TypeScript, production build and `pip check` passed; diff whitespace check passed.

All **nine Cyber Lab browser cases** passed against actual FastAPI and disposable SQLite with a synthetic bearer session, without intercepted responses: original desktop/mobile journeys; supplier/recovery desktop/mobile wins and reopening; actual mistake review; Build C campaign navigation, ungraded reflection, worked paging, new question pools and keyboard asset actions at desktop/mobile widths. Chromium headless execution was available locally. Screenshots of the asset list were inspected at desktop/mobile widths. CI supplies ordinary Chromium/PostgreSQL and broader regressions; those final Build C gates are pending at this source checkpoint.

No owner runtime/database, beta service, mail/model provider or live target was operated. Separate independent content/learner, physical-device, operational recovery and deferred final formal-security gates remain open. Functional test results are bounded evidence, not security clearance or completion of the whole roadmap.

## Recovery and next action

Prefer a forward fix and preserve data. No migration rollback is needed. Older code can still read stored snapshots but does not provide the new edition/bank/campaign; do not delete current completion rows, new question sessions or newer scenario runs as a rollback technique. Build A cannot correctly continue v2 supplier/recovery runs. Retain the accepted recovery procedures and review any source rollback against the revisions already created by users.

Next: verify Build C CI, then use this complete guide for owner development update/check/restart and acceptance. Use learner observations to choose the next gameplay iteration before AI, multiplayer or further catalogue expansion. Independent content review and beginner/device walkthroughs remain important after the 500-question authoring milestone; a count alone does not establish learning quality. Beta promotion and production readiness are separate decisions.
