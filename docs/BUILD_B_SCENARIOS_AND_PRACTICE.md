# Build B — replayable scenarios and 250-question practice

28 October 2026 (Africa/Lagos). Development branch: `feature/beta-continuous-improvement`. The owner reported “All test passed” after the Build A navigation correction and authorised continuing. This is owner-reported local acceptance of the previous build, not independent learner/device/security evidence.

## Delivered scope

- Three scenario choices in `/cyber-lab`: the accepted **Defend the branch** plus **Supplier Access Crisis** and **Recovery Under Pressure**. Saved shift cards identify their scenario. All use the same fictional six-asset map; these are distinct rule sets, not three unique 3D worlds.
- Supplier Access Crisis teaches the difference between human MFA and supplier service credentials. The gateway receives recurring credential entry attempts on turns 3, 6 and 9 until supplier access is revoked. Revocation closes that path but does not clear compromise already present. Victory requires revocation, no remaining compromise, verified recovery and at least 80% service from turn 10, by turn 18.
- Recovery Under Pressure starts with confirmed workstation/application/database compromise and encrypted application/database services. Encryption affects service availability; isolation alone does not restore service. The player must contain, verify recovery, restore and reconnect while maintaining enough service. Victory is possible from turn 8, by turn 18. The exposure indicator follows documented fictional rules; encryption alone is not evidence of data theft in a real incident.
- **250 total Cyber Lab practice questions:** 150 new original questions, fifteen per topic family, added to the accepted 100. Every family now contains 25: four foundational, sixteen applied and five challenging. The current bank is separate from existing course banks and mission reviews; this does not complete the later 500-question goal.
- Fresh practice retains mixed-topic balancing, shuffled options and pinned grading. **Review recent mistakes** selects from actual saved incorrect answers. A later correct verdict removes that question from review while it remains the latest graded verdict within the bounded window; no weakness or mastery is invented for unanswered topics. The count selector reflects the eligible topic/difficulty/mode pool and the server validates it independently.
- All three learning modules move to `cyber-lab-v2`: expanded scenario/control explanations, 250 worked decisions, more specific primary-source readings and explanations of older-reference limits. Earlier read-completion records remain stored; the UI identifies earlier-edition completion and lets the learner mark the expanded edition read. No prior score or completion row is deleted or regraded.
- Dashboard and public landing copy reflect 250 questions. The normal student dashboard retains **Cyber Lab** in navigation and **Play Branch Defender →** above saved progress.

English only, programmed adversary, no external AI/model calls, no new app dependencies, no new content-publisher operation and **no migration beyond accepted `0011_strategy_learning`**. Beta is not promoted or operated by this build.

## Preservation and ordinary security checks

The previous engine is retained unchanged as `api/strategy_v1.py`; a dispatcher selects rules by stored revision. Existing `branch-defender-v1` runs continue under those rules without rewriting state. New supplier/recovery runs use `branch-scenarios-v2`, with an allowlisted scenario ID and fixed server rules. Clients cannot submit a seed, score or alternative module. New-rule restoration cannot be followed by reconnection while restoration is still pending. Ownership, command UUID deduplication, expected versions, transaction locks and resource/creation bounds remain enforced.

The original 100-question source file remains byte-for-byte unchanged. Its IDs, answer data and question revision remain `cyber-lab-v1`; the 150 new questions use `cyber-lab-v2` and distinct IDs. Selected questions, options, keys and explanations are still pinned per practice session. New submissions add a server-side submission time within the existing result JSON. Completed old results are not rewritten. Mistake review uses the latest graded verdict within up to 50 recent completed sessions; server submission time determines order where recorded, while older results lacking it use creation order as a documented legacy limit. This is a bounded practice aid, not a longitudinal mastery assessment.

Module edition completion uses existing revision-aware progress rows. Earlier completion is shown as an earlier edition, rather than silently credited for unread additions or deleted. Historic course, assessment, mission and Build A game data remain intact. No schema backfill or automatic startup publication occurs.

## Public reading references

Readings are optional; the core explanations and worked decisions are included in EduCyber. References are links, not copied documents, and were checked on 28 October 2026.

| Topic | Public reference | Context |
| --- | --- | --- |
| Risk/governance | [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) | General risk and outcome structure |
| Phishing | [MITRE ATT&CK T1566](https://attack.mitre.org/techniques/T1566/) | Adversary-behaviour reference; use the defensive explanations in the module |
| Identity | [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) | Authentication, recovery and protection controls |
| Segmentation | [MITRE ATT&CK M1030](https://attack.mitre.org/mitigations/M1030/) | Restricting network paths; validate actual effectiveness |
| Endpoint | [MITRE ATT&CK M1051](https://attack.mitre.org/mitigations/M1051/) | Software updates; distinct from cleaning an existing compromise |
| Application | [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) | Effective privilege and request-level permission checks |
| Cloud | [NIST SP 800-144](https://csrc.nist.gov/pubs/sp/800/144/final) | 2011 background concepts, not current provider-specific configuration guidance |
| Response | [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) | 2025 incident-response reference |
| Recovery | [NIST SP 800-34 Rev. 1](https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final) | 2010 planning concepts, not a compliance claim or vendor runbook |
| DNSSEC worked decision | [RFC 4033](https://www.rfc-editor.org/info/rfc4033/) | Services/limits background; the document notes subsequent updates |

## Complete PowerShell update, checks and restart

Stop **only development** frontend/API with Ctrl+C. Leave beta running. Run from the existing development worktree root. Preserve local changes. The schema check below uses the existing development-only guard; it is a no-op when the accepted Build A schema is already current. No separate content publication is needed.

```powershell
$ErrorActionPreference = 'Stop'
$buildBBranch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $buildBBranch -ne 'feature/beta-continuous-improvement') {
    throw 'Open the existing development worktree first.'
}
git status --short
git pull --ff-only origin feature/beta-continuous-improvement
if ($LASTEXITCODE -ne 0) { throw 'Update failed; preserve and inspect local changes.' }

& .\api\.venv\Scripts\python.exe .\scripts\migrate_development.py
if ($LASTEXITCODE -ne 0) { throw 'Development schema verification/migration failed.' }

$buildBPreviousDatabaseUrl = $env:DATABASE_URL
$buildBPreviousTestUrl = $env:TEST_DATABASE_URL
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
    $env:DATABASE_URL = $buildBPreviousDatabaseUrl
    $env:TEST_DATABASE_URL = $buildBPreviousTestUrl
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

## One Build B acceptance pass

Open the development frontend, sign in with a synthetic student and choose **Cyber Lab**, or open `/cyber-lab` on that same development origin.

1. Confirm the **Scenario** selector offers all three choices. Resume a previously saved Build A shift and verify its turn, resources, timeline and outcome have not been reinterpreted. Existing 30 case-study missions remain separate.
2. Try Supplier Access Crisis. Compare staff MFA with **Revoke supplier access** on the gateway. In one run revoke early and verify recovery; advance to the scenario goal. In another allow entry, then revoke: existing compromised assets must still require containment/recovery. Check saved reopening and the explicit scenario title.
3. Try Recovery Under Pressure. Inspect initial encrypted services and service availability. Contain affected assets, queue recovery verification, restore isolated assets, wait for the turn to finish, then validate/reconnect. Restoring a still-connected asset or reconnecting during a pending restoration must not bypass the new scenario's rules. Compare an ignored incident with a deliberate recovery sequence.
4. In Learn, inspect the new explanations, worked decisions and specific public reading links. Earlier-edition completion should remain acknowledged without marking the new edition read automatically. Mark the new edition complete and verify persistence after reload. Report confusing concepts, ambiguous questions or broken external reading links for correction.
5. In Practise, confirm 250 total questions and topic/difficulty choices. Try a challenging five-question topic session. Submit one or more incorrect answers, choose **Review recent mistakes**, and check that review contains actual saved mistakes. Correct an item and verify that its later graded verdict removes it from that eligible review set. Empty review pools must explain that practice is needed, not manufacture weaknesses. Reopen an old saved result and confirm its original grading/explanations.
6. Check keyboard/touch controls, desktop/narrow viewport, reduced motion, saved history, failed-load recovery and logout. The map pans on narrow screens; this is not a measured physical-device performance guarantee. Keep independent learner/content/accessibility/operational/final security gates open.

## Verification checkpoint

Local full backend checkpoint: 609 tests and 11 subtests passed with 21 PostgreSQL-dependent skips; subsequent focused Build B checks passed all 16 cases after the final review-window/pending-restore fixes. Frontend 15 unit tests, TypeScript and production build passed; pip check passed. Both source-preservation checks confirm byte-for-byte original rules/question files.

All seven Cyber Lab browser cases passed locally against actual FastAPI and a disposable SQLite database: the two original desktop/mobile journeys, four new supplier/recovery desktop/mobile journeys, and actual saved-mistake review. No intercepted API responses were used in those seven tests. The supported headless shell is used locally; CI supplies ordinary Chromium and PostgreSQL coverage. The initial checkpoint is not a new full PostgreSQL, independent educational or final security pass; CI and owner Build B acceptance remain pending here.

## Recovery and next action

Prefer a forward fix while retaining all saved state. Build A code cannot continue new v2 scenario runs correctly; a source rollback after learners create those runs needs an explicit reviewed preservation plan. Do not delete new runs or downgrade the accepted schema as routine recovery. Practice snapshots and prior module editions remain stored.

Next: verify Build B CI, then use this single complete update/check/restart guide and acceptance pass. Do not infer owner acceptance of Build B from the earlier Build A report. The next planned bank milestone after accepted feedback is 500, with further game/content improvements driven by learner evidence.
