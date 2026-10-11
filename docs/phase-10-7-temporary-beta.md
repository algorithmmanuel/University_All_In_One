# Phase 10.7: six-person temporary ngrok beta

Status: implementation in progress; **do not share a public URL until CI and local smoke tests pass**.

## Design

- One ngrok HTTPS tunnel exposes only the Next.js web port 3000. Next.js rewrites `/api/v1/*` to local FastAPI on 127.0.0.1:8000. No second tunnel and no public backend port are required.
- `EDUCYBER_PRIVATE_BETA=enabled` on the FastAPI process enforces adult-only, student-only, invitation-required registration and rejects login and protected access for pre-existing accounts without adult age classification.
- Six cryptographically random invite codes are stored as SHA-256 digests. Each is redeemed once at account creation; **the resulting account may sign in repeatedly** while the laptop and services are running. Code expiration only affects redemption, not account lifetime.
- Authenticated adult learners submit categorized feedback and 1–5 ratings at `/feedback`; submissions are saved to `beta_feedback` and linked to their `users.id`. The `GET /api/v1/beta/feedback/mine` endpoint returns only the caller's feedback.
- Existing local development database is used only with deliberate backup and additive migration `0008_private_beta`; never reset or restore blindly.

## Before external access

1. Verify latest GitHub Actions quality gates, back up local PostgreSQL and run Alembic migration `0008_private_beta`. The previous backup is for `0007`; create a **fresh** one before migrating again.
2. Ensure the laptop has OS updates, disk encryption, firewall and reliable power/network. Avoid running elevated terminals.
3. Set `EDUCYBER_PRIVATE_BETA=enabled` in the **API process environment**, not in a public frontend variable. Confirm the API refuses registration without a code. Do not expose a development instance with beta mode disabled.
4. Configure `EDUCYBER_CORS_ORIGINS` for explicit local origins only. Same-origin proxy avoids cross-origin requests for testers.
5. From `api/` with the correct `DATABASE_URL`, run `python create_beta_invites.py --count 6 --days 30 --confirm`. **Do not run this twice**: maximum six total codes. Distribute codes individually using a private channel. Codes are displayed once, not stored in plaintext.
6. Start FastAPI bound to **127.0.0.1:8000**, and Next.js on port 3000. Do not expose FastAPI directly or publish PostgreSQL.
7. Start `ngrok http 3000`, use the HTTPS URL. Test from a separate network/device: unauthenticated registration rejected, invalid code rejected, invited adult registers, logs out, logs back in, completes mission and submits feedback.
8. Restrict the ngrok endpoint to invited users where available (e.g., ngrok edge access policy). Invitation codes protect account creation, **not the public visibility of the landing page**. If access controls are unavailable, treat the URL as publicly reachable.
9. Tell testers the service is temporary and goes offline when the laptop, Next.js, API, database or ngrok stop. Do not promise continuous uptime.

## Reviewing feedback locally

From the repo root:

```powershell
docker compose exec -T postgres psql -U educyber -d educyber -c "SELECT f.id, f.created_at, u.email, f.category, f.rating, f.page, f.message FROM beta_feedback f JOIN users u ON u.id=f.user_id ORDER BY f.created_at DESC;"
```

This displays personal data; run locally and never publish raw feedback without tester consent. To review summary counts without names or message text:

```powershell
docker compose exec -T postgres psql -U educyber -d educyber -c "SELECT category, count(*) AS submissions, round(avg(rating),2) AS average_rating FROM beta_feedback GROUP BY category ORDER BY submissions DESC;"
```

## Beta limitations and safeguards

- No guardian workflow: do not recruit minors.
- Do not ask testers to use real incident data, production credentials or sensitive personal information.
- The beta database holds email, DOB and free-text feedback. Inform testers about the purpose, storage, access, retention and how to request deletion; secure laptop and backup copies.
- The feedback UI and API are **not** an operator moderation system; use local SQL for review.
- Testers can access the app only while the laptop and services are running; ngrok URL may change on restart.
- Prior to a public launch: formal security review, threat modeling, independent penetration testing, edge abuse protection, tested recovery, privacy and safeguarding governance.
