# Red/Blue Stage 3 / B1 — authenticated alternating preview release

**Owner direction:** each completed, tested stage is promoted to Beta source, maintaining existing learner accounts, recorded games and environment separation.  
**Scope:** new Blue-first V2 edition plus a separate, **Development-only** preview UI and authenticated match support. **Beta gameplay remains the original sealed-round mode** until the 90-second server timer and single 30-second reconnect grace pass acceptance. This is a safe foundation/source release rather than the final player-facing timed-mode launch.

## Exact scope and constraints

- `api/cyber_warfare/v2_alternating.py`: an immutable, edition-tagged deterministic engine. Blue resolves the first action; Red acts using side-filtered evidence; the round closes after Red. Retains old objective and action semantics; does **not** rewrite historical V1 transcripts.
- `api/cyber_warfare/v2_session.py`: authenticated caller's private-match adapter that chooses the correct old/new engine from the pinned transcript, preserves replay, handles join, projects seat-only state, and lets a computer take a move using its own observed state. Follows existing row-locking and receipt semantics when called from routes.
- `api/red_blue_routes.py`: default `ruleset='sealed'` remains the same; the optional `alternating_preview` can create new matches **only when the running server sets `EDUCYBER_ENV=development`**. Beta explicitly rejects creation with HTTP 403. Existing Beta records cannot be silently converted.
- `web/app/red-blue/{page.tsx,useArena.ts,types.ts,Planner.tsx}`: capability-gated preview selector appears only when the Development API advertises it; turn instructions say **no timer**; legacy layout/choice wording remains for all Beta players. All API fetches use existing bearer session and no-store response.
- `api/test_red_blue_api.py` and `api/cyber_warfare/test_v2_session.py`: verify two real bearer-auth users, isolated SQLite and PostgreSQL persistence, Blue-first action, ID reuse, filtered side projections, both bot roles, versioned replay and refusal in Beta. Existing regression gates guard legacy matches.

**Not included yet:** 90-second server-owned deadlines; one-time 30-second disconnection grace; robust background expiry; learning vs realistic UI; full per-action V2 telemetry refinement, topology routing, dual-role counterfactual debrief, user-built networks. Do **not** label the untimed Development preview as production-ready multiplayer.

## Beta and Development private environment policy

Follow [ENVIRONMENT_AWARE_RESTART.md](ENVIRONMENT_AWARE_RESTART.md) **exactly**.

- Beta checkout: `C:\Users\dNA1991\University_All_In_One`, branch `feature/secure-password-recovery`, Beta API **8000**, web **3000**; root `.env` supplies the beta DB password and `api/.env.beta` supplies Brevo recovery mail and public ngrok web origin. No changes to these files; never print them.
- Development checkout: `C:\Users\dNA1991\University_All_In_One_Development`, branch `feature/beta-continuous-improvement`, API **8010**, web **3010**, `api/.env.development` contains the isolated database URL. The Development launcher sets `EDUCYBER_ENV=development`; do not copy a Beta `.env` or `api/.env.beta`.
- If port 8000 is already in use, first stop existing **Beta** API through its foreground terminal; if a stray process remains, verify its executable path and full Uvicorn port command before stopping. Never stop generic Python processes or development port 8010. On update, preserve generated `web/next-env.d.ts` using selective stash only after examining it; never `reset --hard`/`clean`.
- No migration, backup/restore, `beta.py courses`, private credential copy, or database reset is required for this source-only release. Continue to verify the running Beta's existing API, schema, 24-course state and ngrok independently.

## Verify and publish when green

1. Verify the **exact final PR source commit** passes the V2 contract, backend+PostgreSQL, frontend TypeScript/build, browser gameplay and real API/PostgreSQL runs. PR must not be merged without green evidence.
2. Merge via the approved reviewed PR into Beta; record merge SHA. Synchronise Development from Beta using non-forced fast-forward.
3. Stop only Beta API and web terminals, inspect listener ownership and generated-file changes, fetch/fast-forward the Beta checkout, rebuild using `api/.venv/Scripts/python.exe scripts/beta.py build`; restart through `beta.py api` and `beta.py web` in separate foreground terminals; `beta.py check` from another terminal. Keep Docker/PostgreSQL and ngrok running.
4. Test legacy Red and Blue accounts, existing saved matches and course flows. Confirm Beta catalog does **not** advertise `alternating_preview_available` to an authenticated tester and new API preview requests receive 403.
5. For Development, independently fetch/fast-forward its own branch, check `api/.env.development` exists (do not reveal content), start `development.py api` and `development.py web`, then `development.py check`. Choose “Alternating preview · no timer”; run two independent authenticated browser sessions. Blue first, Red second, save/restore and compare role-filtered evidence. Do not expose Development web **3010** through public ngrok.
6. Record owner runtime/browser feedback and CI source evidence as separate facts. The timer/timeout stage remains the next release.

## Release evidence

**Pending final run and source merge:** see the top of [DEVELOPMENT_STATUS.md](DEVELOPMENT_STATUS.md) and [PR #8](https://github.com/algorithmmanuel/University_All_In_One/pull/8). Update these explicitly after CI checks; do not infer the owner laptop has updated simply because a GitHub merge succeeded.
