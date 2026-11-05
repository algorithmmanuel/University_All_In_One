# Red/Blue authenticated storage and API

Development only, approved continuation 29 October 2026. No beta promotion is authorised.

## Storage and transaction boundary

Migration `0012_red_blue_matches` adds three independent tables: matches (private pinned replay, status, creator and hashed invitation), seats (one Red/Blue seat each, at most one seat per user) and receipts (actor-scoped UUID and sealed order). Existing learning, assessments, missions, practice and StrategyRun tables are unchanged. Foreign keys cascade simulator records with their owning account/match; no automatic retention purge is introduced. Operational retention/recovery policy remains an acceptance gate.

A match transcript contains the configuration snapshot, engine/rule digest, private seed and at most 60 sealed commands over 30 rounds. Restore recomputes state using the pinned engine; unsupported rules fail closed. Retain old engine code for old editions. The transcript is private trusted storage, not a user import protocol or cryptographic authenticity proof.

PostgreSQL READ COMMITTED transactions acquire `SELECT ... FOR UPDATE` on the match before reading receipts, applying commands, resolving, updating the transcript and inserting a receipt. Commit happens once for the whole operation. No process-local locks, sticky sessions or in-memory authority are required. The second seat submits against the **round**, not a global version changed by the first seat. Actor/UUID/payload retries return the latest filtered projection with no second effect; a changed payload or fresh stale command returns 409. Failed resolution or receipt insertion rolls back the whole operation. Storage exceptions are translated to a generic 503 without logging SQL transcript parameters; the client retains the same command UUID for safe retry. SQLite sequential tests do not establish these locking guarantees.

## Authentication and access

Existing opaque bearer sessions and `student_only`/private-beta checks apply on every request, including resume and join. Red/Blue seats are separate from account roles. Teacher/admin accounts do not obtain participant or instructor-review rights. No instructor or spectator endpoint is enabled; a future review policy needs explicit approval.

A human match waits for a second, distinct eligible learner. Only its creator can issue/rotate an invitation. Tokens contain 256 bits of random entropy, expire after 24 hours, are stored only as SHA256 hashes and are consumed under the match lock. Rotation invalidates the previous token. Tokens are returned only by the explicit invitation POST, never history/resume. Share privately; do not put them in URLs/logs. Join gives no account search or identity disclosure. There is no automatic timeout forfeit or unilateral turn advance. Participants can resume after reconnecting/signing in again. Creator match creation is capped at 100 per day with a database user-row lock; history is paginated in batches of 20.

## Routes (`/api/v1/red-blue`)

| Method/path | Body / result |
| --- | --- |
| GET `/catalog` | Six public scenario summaries, original conceptual action wiki/mappings; no hidden configuration. |
| POST `/matches` | `{scenario, side: red/blue, mode: computer/human, difficulty: easy/standard/hard}`; creator seat bound from authentication. |
| GET `/matches?before_id=` | Participant-only history summaries and next cursor. |
| GET `/matches/{id}` | Only the participant's engine projection plus offered orders/status. |
| POST `/matches/{id}/invite` | Creator of waiting match only; new token/expiry, invalidating old token. |
| POST `/join` | `{token}`; atomically binds empty seat and consumes invitation. |
| POST `/matches/{id}/commands` | `{command_id: UUID, expected_turn: integer, action, target?, source?}`; bounded, extra keys forbidden. |
| GET `/matches/{id}/debrief` | Participants after completion only; action timeline, missed evidence and bounded single-round counterfactuals. |

POST bodies are capped at 4 KiB before JSON parsing, including streamed bodies without a trusted Content-Length; individual fields and extra-key rejection remain stricter. Responses use `Cache-Control: no-store`. Live payloads never include seed, sealed opponent order, full state, private trace or replay. Unknown/non-owned IDs return the same 404. Errors never use hidden truth for legality. Human and computer actions have the same projection/resource rules. The computer chooses from its opening projection **before** the human commitment is applied, then both resolve atomically.

## Evidence

`test_red_blue_api.py` uses actual hashed bearer sessions without authentication overrides. Sequential SQLite checks cover access, beta eligibility, single-use/rotated/expired invites, locked commitments, hidden-choice noninterference, stale/conflicting/repeated commands, completion/debrief, all configurations and rollback failures. The same cases run on isolated PostgreSQL; additional barrier-synchronised races exercise two sessions plus duplicate submissions, conflicting same-seat commands and competing joins. `test_red_blue_migration.py` checks additive migration/downgrade with preserved synthetic legacy records. Full suite and CI results belong in DEVELOPMENT_STATUS.md. These checks establish technical behavior, not independent teaching/balance/device acceptance or a formal security audit.
