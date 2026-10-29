# Adding a Red/Blue scenario or action

This is the engine checkpoint; there are no new web routes or database migrations. See [the staged plan and assumptions](RED_BLUE_SIMULATOR_PLAN.md).

## Add a scenario

1. Copy `api/cyber_warfare/scenarios/microfinance.json` to a new lowercase identifier filename, such as `training_branch.json`; set `id` to the same value. No engine registry edit is required. `list_scenarios()` discovers configurations.
2. Keep `schema_version: 1`; start `revision: 1`. Choose title, industry, difficulty, turn limit (3–30), AP allowance (3–6) and equal starting budget (6–100).
3. Define 2–20 unique assets. Kinds: `workstation`, `server`, `database`, `cloud`, `third_party`. Value: 1–100. Mark external exposure. Weaknesses: `phishing`, `privilege`, `configuration`, `access`, `instruction`. Controls: `monitoring`, `patched`, `hardened`, `segmented`, `access_control`, `backup`. Starting access is 0 (none), 1 (user) or 2 (privileged). Assets with initial Red access must appear in Red's starting intelligence.
4. Add directed `source`/`target` trust edges (maximum 60). No self-links, missing endpoints or duplicates. Put every asset in Blue's inventory; give Red only starter-known assets and a plain-language briefing. Do not include credentials, addresses of real targets, personal data, attack payloads or procedural exploitation instructions.
5. Choose objective kind `fraud`, `leak` or `disruption`, target IDs and a threshold no larger than their combined value. `hold_turns` is 1 except for consecutive disruption objectives. Explain exactly what wins and that Blue wins by protecting the objective until the deadline. Isolation also counts as disruption; recoveries cannot undo past leakage or fraud.
6. Run `python -m pytest -q test_cyber_warfare.py` from `api/` in the development virtual environment with the documented synthetic test database setting. Add seeded Red-win and Blue-survival playthroughs, check meaningful route choices and review balance. Existing dynamic scenario tests automatically exercise all three opponent policies.

Unknown keys/types, invalid identifiers, file paths, malformed references and unsupported controls are rejected. Loader inputs are local scenario IDs, never user-supplied paths or remote URLs. Editing a configuration requires a new revision; saved games retain a validated snapshot, not the changed live file. Do not replace the engine revision for an active match.

## Add an action

1. Add an immutable `Action` entry in `api/cyber_warfare/catalog.py`: side, phase, AP/budget cost, success/detection baselines, public MITRE technique, relation (`represents`, `addresses`, `context`), original conceptual explanation, prerequisites and success rule. Review the primary source and avoid working attack instructions.
2. Implement observation-only availability in `available_orders`, authoritative current-state prerequisites in `_feasible`, probability modifiers in `probabilities` and bounded effects in `_effect`. A public offer must not query hidden truth. Any new observation belongs in the seat projection or an explicit evidence event, never a full-state response.
3. Update readable priorities in `opponent.py` if appropriate. It must consume only a projection; never pass it `Match` or the private seed. Easy/standard/hard should differ in decisions, not hidden information.
4. Add meaningful tests for cost, legality, blocked/stale prerequisites, success/failure, detection, secrecy, replay and any objective impact. Update the catalogue inventory test. Adding a new mechanic requires an engine version change and retaining the original resolver/catalogue for old games; the current loader rejects mismatched rule digests instead of silently changing a replay.

The catalogue currently has 18 targeted actions plus two zero-cost planning/wait actions. Probabilities are deliberately simplified teaching values, not empirical estimates.

## Adapter contract for the next checkpoint

Only `view(match, authenticated_participant)` is a live response projection. Never serialize the `Match` dataclass, call private `probabilities` for a player, expose `export_replay` during a match, or log the seed/orders in ordinary request logs. `debrief` checks participant membership and terminal state. Any instructor review needs its own approved policy.

Store a match and pinned rules/configuration server-side. Bind seats using existing authenticated user IDs; clients must not nominate their own identity or submit state, rolls, success, cost or scores. Apply match ownership, private-beta eligibility and invitation rules. Validate bounded HTTP schemas and UUID command IDs; lock/CAS and commit both plans/resolution/receipts atomically; test actual separate sessions and races with disposable PostgreSQL. Round preconditions allow both players to seal the same round even if the other player's commitment changes the storage version.

`export_replay`/`replay` are trusted internal debugging functions, not authenticated storage or a public import protocol. Replays recompute from the pinned snapshot and command receipts; arbitrary JSON object key order is supported. Seed/phase/round SHA256 fractions are deterministic across processes. Keep old rules code available for old matches, validate all restored data and place strict body/retention limits at future persistence boundaries. Exact replay does not authenticate a transcript that an attacker has rewritten.
