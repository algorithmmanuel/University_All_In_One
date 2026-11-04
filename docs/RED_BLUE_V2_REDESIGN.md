# Red/Blue live-state and alternating-turn redesign

## Stage 5 RB2-B3 implementation checkpoint — 4 November 2026

Stage 4 B2 was merged via PR #9 (merge `65d816d62b9f345699e293b30b85ce75efd7cb7c`); the reviewed PR head `2ab73a5` passed backend, frontend, V2 contract, actual-API/PostgreSQL browser and browser gameplay CI. This is source evidence, not proof of owner laptop/worker rollout. The development branch subsequently contains separate password-recovery incident changes, which are not a Red/Blue release.

**B3 initial Development-only UI slice:** `web/app/red-blue/AssetBoard.tsx` commit `eed1aa6` replaces the prior three-column diagonal SVG lines with orthogonal trust-path routing using the existing *seat-filtered* `match.assets` and `match.connections`. It rejects missing edge endpoints, retains the accessible directed-edge list and marks the last observed match revision/round. The board continues to consume only authorised `match.observations`; no raw private event payload or opponent intent is introduced. Existing GET polling remains unchanged; no backend asset truth, game rules, database or Beta runtime was modified.

**Unverified:** complete frontend/browser/real-API regression on this exact new commit, six-scenario topology acceptance, dense/multi-row path crossing, keyboard/mobile accessibility, and proof of reactive evidence differences after adversarial actions. Orthogonal routing reduces direct diagonal links but does not guarantee crossing-free arbitrary graphs. The browser progression CI failure on an unrelated subsequent development change (run 41872057895) is still untriaged. Do **not** promote B3 or claim completion.

**Next B3 steps:** review final-head CI; fix failed checks; add geometry coverage and dense-edge layout handling (lane allocation/grouping), verify selected-asset evidence across two authenticated Red/Blue sessions and all six scenarios, then perform release acceptance and promotion only with green gates. Preserve original V1 replay and Beta data.


## Stage-one release candidate — 4 November 2026

Implemented isolated V2 outcome adapter `api/cyber_warfare/v2_events.py` with template-generated Red/Blue evidence, preventing retroactive alerts from newly installed sensors and guarding ID collisions; added five pure transition tests in `test_v2_events.py`. This is **not integrated with the authenticated game engine or API**. Existing `AssetBoard.tsx` now groups already-authorised observations by asset, showing evidence counts and the latest eight asset messages on network/list views. These appear on the existing simultaneous-round cadence; the 90-second alternating turns remain a separate future milestone. PR [#6](https://github.com/algorithmmanuel/University_All_In_One/pull/6) is ready for review, not merged. Frontend quality gate 41816649012 passed on `f9fddf9`; V2 contract 41816648952, backend 41816649018, browser 41816649008, real-API 41816648971 remained queued at inspection. No full green suite, Beta deployment or user acceptance claimed. Verify the **final PR head** after documentation commits before promotion.


**Incremental Beta Release Policy (owner-approved 4 November 2026):** The previous 'development only until all stages are done' rule is superseded. Every **complete, tested and independently deployable** RB2 milestone will be merged/promoted to `feature/secure-password-recovery` for external tester feedback, while incomplete work stays in development. A stage must have passing relevant CI and regression/secrecy tests; prior to any schema/data change, provide and execute guarded database backup/migration/readiness procedure, never discard tester records. A GitHub merge does not update local services or public ngrok; provide complete owner PowerShell update, preflight, build, restart and verification instructions. Preserve stage-by-stage status of dev commit/CI, beta commit/CI, local deployment and tester acceptance. If a milestone cannot safely function in isolation, group it with its dependency into a single releasable stage, rather than exposing unfinished UI to beta. Source releases may contain isolated scaffolding that does not change player behaviour; label that limitation clearly. This policy does **not** approve unsafe changes, bypass release gates or imply any beta merge has happened.


**Decision date:** 4 November 2026 (Africa/Lagos)  
**Owner approval:** begin development, document every milestone; 90-second turns; Blue opens; one 30-second disconnection grace period.  
**Status:** implementation plan and acceptance contract committed; implementation and verification not yet complete.  
**Development only:** `feature/beta-continuous-improvement`. Do not merge/promote to `feature/secure-password-recovery` without separate owner permission and green acceptance.  
**Source inspection:** `api/cyber_warfare/engine.py`, `scenario.py`, `opponent.py`, `api/red_blue_routes.py`, `red_blue_models.py`, `web/app/red-blue/{page.tsx,AssetBoard.tsx,AfterAction.tsx,useArena.ts,types.ts}`, `docs/RED_BLUE_{SIMULATOR_PLAN,API,AUTHORING,RELEASE}.md`.

## Motivation and explicit non-goals

Owner completed a Red/Blue playthrough and reported *only* these defects: stale-looking opponent effects and topology; insufficient asymmetrical evidence; missing learning/realistic modes; no timed reactive turns; crossing network connectors; overwhelming debrief; incomplete first-run guide. Preserve all unmentioned behaviour, other EduCyber products, authentication, private-beta eligibility, saved progress, existing courses and scenarios. Proposed future player-built networks and purchased tools are **not authorised for implementation** yet.

Current engine truth does change after resolution (access, monitoring, isolation, disruption, leakage, fraud), but `view()` exposes sparse per-asset evidence and the interface uses a static grid with straight lines. The current engine seals both sides' choices per round, resolves Blue then Red, and the bot commits at the same time as the human; none of this meets an alternating reactive-turn requirement. Existing history/replay semantics must not be modified in place.

## Milestones and traceable gates

| ID | Scope | Acceptance gate | Status |
| --- | --- | --- | --- |
| RB2-00 | Record owner feedback, decisions, risks and release plan | Repository documents reference current implementation and precise next action | Documented |
| RB2-A1 | Versioned authoritative asset/evidence schema; tool capabilities; event taxonomy | Deterministic unit tests, no hidden data in either seat projection, all 6 scenarios | **Implementation expanded**: validation, six-scenario starting adapter, negative tests and dedicated CI workflow committed; repository CI and trusted event-generation integration pending |
| RB2-A2 | Side-filtered observations; asset event badges and detail evidence; monitoring-based fidelity | Two-seat tests: stealth remains hidden; alerts do not assert compromise; Red sees confirmed own access; stale intel marked | Not started |
| RB2-B1 | New alternating-turn engine edition; Blue starts; turns/rounds and objectives defined | Single-authorised action per turn, immediate resolution and replay; old edition still replays | Not started |
| RB2-B2 | Durable server-clock and expiration; bot scheduling, reconnect grace and idempotence | Actual PostgreSQL race/expiry tests, client clock does not grant or reset time | Not started |
| RB2-B3 | Topology/asset UI with tidy routed links and timely refresh | Desktop/mobile, keyboard, accessibility, no unsafe disclosure, cross-node route tests | Not started |
| RB2-C1 | Learning/realistic presentation, contextual hints | Both roles, modes and scenarios; hints never expose private engine truth as telemetry | Not started |
| RB2-C2 | First-launch game guide and worked turns | Persist completion per user; can reopen; keyboard and narrow-screen acceptance | Not started |
| RB2-C3 | Short ranked turn-specific debrief for both sides | 3-5 most consequential turns, <=2 tested alternatives each, qualified counterfactual claims | Not started |
| RB2-D | Integrate and validate complete separate-account + bot sessions | CI backend/frontend/browser/actual PostgreSQL; replay, time, secrecy, saved records; owner acceptance | Not started |
| RB2-F | Player-built network and offensive/defensive acquisition | **Design compatibility only** pending owner's separate approval | Deferred |

Every code milestone must update this table and `docs/DEVELOPMENT_STATUS.md` with exact commit(s), tests that ran (not merely proposed), risks and next action. Keep in-progress changes out of beta. Do not equate GitHub commits/CI to locally running application updates.

## A. Authoritative state and per-seat intelligence

Single server-authoritative match truth: versioned assets, trust edges, controls, vulnerability/availability state, compromise/access, persistence, data impacts, deployed capability identifiers and ordered state transitions. Add append-only events with bounded IDs, turn/sequence, asset IDs, actor side, action category, actual effects, detection/telemetry and rule edition. Internal event truth is never returned wholesale during a match.

Create seat-specific, versioned **observations** derived solely from allowed information:
- **Blue**: inventory, own installed controls, service availability, alerts/findings and logs permitted by installed monitoring. Never Red's selected orders, inferred intent, hidden foothold, private seed or success roll unless supported by investigated evidence. An alert is **suspicion**, not confirmation.
- **Red**: starter knowledge, scoped recon discoveries, knowledge timestamp, confirmed results of own actions and effects detectable by probing. Unknown Blue controls stay unknown; a failed attack does not reveal secret defense details via error messages.
- Asset knowledge status: `confirmed`, `suspected`, `stale`, `unknown`. These are **epistemic labels**, not a leaked authoritative health flag. Include per-asset bounded visible events, observed turn and evidence source; preserve an empty/unknown representation when no evidence exists.
- Monitoring and defensive capability catalogue must be data driven (e.g., authentication events, endpoint/flow telemetry, alerting) rather than only a yes/no global reveal. Future player build phase can install/remove capabilities. Offensive inventory similarly scopes legal actions; actual acquisition is deferred.
- Use identical side projections for humans and bots. Both learning and realistic modes share outcome rules; Learning mode adds clearly labelled hypothetical educational hints grounded in the player's current knowledge, never disguises omniscient truth as telemetry.
- Do not expose full private match state, opponent sealed intentions, seeds or rolls in normal API responses, error payloads, ordinary logs, or cached content. HTTP responses retain no-store.

## B. New rule edition: reactive turns

Legacy version stays **unchanged and replayable**. Create a separately identified rule edition and migration path for *new* matches only. Pin rule digest, scenario snapshot and clock policy per match. Do not silently reinterpret old `rounds`/pending records.

One **round** consists of a Blue action then Red action. Blue always opens round 1 with a defensive preparation action. The server resolves each authorised action immediately; the opposite seat receives only its fresh filtered observation. Existing finite budgets, AP caps, action semantics and scenario turn limits remain as close to existing as possible; explicitly test balance because fixed first mover changes outcomes.

Victory evaluation: check irreversible fraud/leak goals immediately after each action where applicable; evaluate consecutive availability objectives at a documented consistent round boundary so a half-round cannot produce an accidental win. The round limit applies to **completed** Blue+Red pairs unless a victory already occurred. No draws introduced without approval. Do not let a timeout pass undo already achieved effects.

### Timer / connection contract

- Every active **human** turn: 90 seconds from a UTC server deadline committed with the turn transition. Response includes authoritative `active_side`, `turn_id`, `round`, `deadline_at`, `server_now`, `clock_state`, and whether its grace has been used; no opponent-private information.
- Expiry is a persisted **automatic pass** for that seat, then advance once. Enforce inside a locked transaction before accepting an overdue action; deadline cannot be reset by reload, duplicate command, another browser or process restart. Resolve races with existing `SELECT FOR UPDATE` and actor-scoped command IDs. A display countdown uses server time offset and refreshes at transitions; browser time is presentation only.
- A single 30-second extra grace **per human seat per match** on server-confirmed disconnection, not on each refresh. A client-side tab close alone is insufficient proof. Heartbeats/presence leases and disconnect qualification must be robust against tab suspension/network jitter; document precise detection threshold and whether detection must happen before expiry. Do not promise magic detection of offline devices.
- No unrestricted manual pause for competitive human matches. Training-session pause may be separately proposed; not part of this release.
- **Computer turns**: server policy uses only its observation; schedule/resolve without requiring a connected browser or worker-local memory. Use a durable worker or transactionally claimed job; explicit deployment strategy/operational tests required before claiming reliable bot deadlines. Provide a short UI transition without falsifying server progress.
- During opponent turn show active side, clock, waiting state and evidence changes; absent player may resume independently with existing authentication and receipts.
- Consider private beta, fairness, clock abuse, reproducibility, migrations and legacy unfinished sessions before any switch.

## C. Interface and teaching

- Render topology nodes from seat's current authorised asset observations; update after action/poll or push. Map visible action evidence onto asset badges; status text must distinguish confirmed from suspected. Asset click reveals only that seat's available logs, telemetry, history, controls and next permitted moves.
- Replace three-column direct diagonal connector geometry with zone-based layered layout, orthogonal channels, edge grouping and a focus/list fallback for dense graphs. Do not claim every possible dense graph can be crossing-free without edge bundling or grouping. Retain keyboard focus, reduced motion, low bandwidth and accessible asset-list option.
- Distinct game **Learning** and **Realistic** modes. No rule/probability advantage from mode; Learning provides comprehensible hints, explanations and recommended next action based on what is available to the viewer. Realistic suppresses hints, retains evidence constraints.
- First-run guide inside the simulator, reopenable. Cover opposing objectives, turns, resources, timeouts, connection policy, assets/state labels, monitoring, visible vs hidden evidence, win conditions and at least one Blue/Red/Blue worked sequence. Persist dismissed/completed state per user, not as shared browser storage.
- Terminal debrief may reveal full histories **only when match ends** to authorised participants. Default show 3-5 ranked pivotal decisions, own-side first, maximum 2 measured alternatives per key turn, measured consequences and uncertainty; provide optional complete transcript. Current counterfactual routine focuses on Blue: add symmetric Red evaluation and avoid asserting a guaranteed different winner from single-round evidence.

## Future build-phase compatibility (NOT approved to build)

Proposed lifecycle: **Prepare** (Blue places assets/trust zones, installs controls/tools; Red acquires conceptual offensive capabilities) -> **Engage** (current versioned turn engine and observations use those capabilities) -> **Debrief** (impact and decisions). Track tools with capability IDs, owner, cost, visibility coverage, action prerequisites and event provenance; assets with owner, zone, connectivity, business value and constraints. All purchased/placed state must be validated by the server and bound to a scenario budget. A short standalone proposal must be given for owner approval before implementing construction, deployment UI, acquisition economy or editing custom network configurations.

## Test matrix / evidence requirements

1. Two **distinct authenticated human sessions**: Blue preparation -> Red targeted attempted compromise -> Blue refreshed information; verify each session's legal actions, available asset events and no leaked opponent intent.
2. Same seeded action with monitoring vs absent monitoring: alert fidelity changes appropriately, absence does not imply asset clean; investigation can confirm evidence where rules permit.
3. Red changes access to a workstation, escalates, then Blue isolates; visible Red access reflects confirmed and newly stale connectivity while Blue sees only authorised health/alerts/findings.
4. Deadline: on-time action, zero time, expired auto-pass, duplicate expiry calls, simultaneous action/timeout race and late command rejection; no double spend/double turn.
5. Disconnection: exactly one granted 30-second extension, none from reload/tab toggles/second session or repeated disconnect, reconnect restores remaining authoritative time; bot does not hang when no browser polls.
6. Learning vs Realistic: same seed/actions/outcomes and same hidden-state boundaries; only assistance/labels differ.
7. Topology: six scenarios and discovered partial graphs, mobile/list, keyboard and reduced-motion; ensure no drawn connection implies previously undiscovered trust path.
8. Debrief: bounded rank, both sides, counterfactuals tied to specific decisions, old match edition preserved.
9. Regression: courses, assessments, missions, Cyber Lab, invitations, password recovery, logout/session independence, existing beta runtime untouched.
10. CI evidence: synthetic unit/engine, migrated PostgreSQL concurrency, frontend unit/type/build, browser intercepted API and actual API/PostgreSQL journeys. Note any blocked tests explicitly.

## Risks / unresolved engineering choices

- Legacy replay/engine edition: use side-by-side support, with explicit new-match selection, not mutation of current digests.
- Deadline advancement without browser traffic: needs durable scheduler/worker design, observable health and recovery after outage.
- Disconnect attestation: browser presence is imperfect. Prefer bounded, documented grace with anti-reset and fairness tests.
- Turn-one defensive advantage: six scenario win-rate/balance review, preserve clear player objectives.
- Topology connectors: planarity limits require edge bundling/focus representation.
- Privacy: event schema may hold private truth; never pass it directly to client.
- Future tools/build economics: model the capability interface now, defer gameplay and purchasing.
- Keep current lesson publication/owner laptop update status separate. No beta rollout is implied by this redesign.

## Release grouping — owner direction 4 November 2026

**First tester-visible beta release = RB2-A1 + RB2-A2**, not A1 scaffolding alone. Stage-by-stage beta promotion means a complete deployable gameplay stage, not every code commit or unseen internal class. Group the V2 foundation with the first authorised asset-event/evidence UI and API integration. Do not replace legacy replay or leak hidden state. Remain on draft PR #6 until the first Beta-visible stage meets the full release gates. Later completed stages go to Beta separately.

## Implementation checkpoint — 4 November 2026

- **Committed** additive `api/cyber_warfare/v2_state.py` (commit `798644d`) and `api/cyber_warfare/test_v2_state.py` (commit `4bc6487`). Defines immutable asset truth, side-scoped knowledge, sensor/evidence capability, bounded event objects and an intentionally side-filtered JSON-safe projection. Existing API, legacy `engine.py` and beta are unchanged.
- **Verification distinction:** Four equivalent isolated Python unit cases passed locally in a scratch environment (`python -m unittest`); the committed pytest file has **not yet been run** against the repository environment or CI. There is no two-player simulator acceptance evidence yet.
- **Open:** strengthen validation of event contents/provenance, integrate V2-only scenario structures and versioned reducer, verify all six configurations, run committed tests and regression gates. The initial model is scaffolding, **not** secure live telemetry functionality; trusted engine generation of event audiences and sensor gating is a mandatory follow-up.

### Additional source work and evidence — same date

- `api/cyber_warfare/v2_validation.py` (`ab9e16b`): bound identities, assets, references, evidence audience/certainty, capabilities, duplicate records and time horizons; rejects Blue alerts that purport to confirm compromise.
- `api/cyber_warfare/v2_state.py` (`f66ec4c`): validates every projection and deterministically orders visible evidence. Models are still unused by the old live engine.
- `api/cyber_warfare/v2_scenario.py` (`d87bbaf`): additive conversion of validated existing scenario configurations to V2 opening snapshot, without changing saved scenarios or databases.
- `api/cyber_warfare/test_v2_state.py` (`f39a8e1`): tests six scenarios plus hostile references, future events, duplicate IDs, missing sensors and role isolation.
- `.github/workflows/red-blue-v2-contract.yml` (`136e961`): dedicated isolated scenario and contract CI gate, with results pending.
- Local **analogous** isolated contract tests in a scratch copy: 15 passed (`pytest`, 0.05 s). These are not evidence that the committed GitHub files, full application, PostgreSQL or browser suites ran successfully. Latest GitHub workflow query returned no result; do not mark green.
- Event texts/audiences still require an audited server-generated reducer and full encrypted/private state boundary. **Strict validation alone cannot prove telemetry truth or prevent a trusted reducer from assigning an overbroad audience.** RB2-A2 must address this before any tester-visible release.

## Immediate next step

First verify committed workflow and existing regression gates, then implement a **server-generated, V2-only evidence reducer** and scoped API/UI asset inspector for RB2-A2. Preserve original engine edition and replay and current beta. Release the combined A1+A2 user-testable vertical slice only after CI, separate-session PostgreSQL/browser acceptance, and guarded beta promotion. Record both source promotion and owner laptop/public ngrok deployment separately. At every milestone, preserve current beta and verify old replay compatibility.
