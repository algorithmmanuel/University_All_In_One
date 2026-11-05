# EduCyber Beta — Password reset delivery incident (4 November 2026)

**Priority:** Block further feature rollouts until affected learners can reset passwords.

## Evidence (from owner screenshot)

- Existing Beta launcher starts Uvicorn on `127.0.0.1:8000`; beta database target is `127.0.0.1:5433/educyber`; application startup completes.
- On at least one real reset attempt the API logs `password_reset_delivery_failed`.
- `api/password_recovery.py` logs that only when `_send_reset_email` raises a transport / Brevo HTTP error. The generic HTTP 202 response to end users is intentional to avoid revealing registered email addresses.
- Screenshot alone **cannot determine** whether the actual failure is invalid/revoked API key, sender verification, transactional permission/suspension, recipient policy, provider rate limit, DNS/TLS connectivity, or provider outage.

## Safe remediation on Development

- Commit `6270b30`: distinguish `HTTPError` before `URLError`. Record only `provider_http_status=<integer>` for rejected Brevo HTTPS calls; for network failures record only `transport_error_type=<class>`. Never log exception message, account email, API credentials or reset URL.
- Commit `01428b5`: add `api/mail_diagnostics.py`; a **read-only** probe of `GET https://api.brevo.com/v3/account` and `GET https://api.brevo.com/v3/senders`. Report only booleans and provider HTTP status. The probe sends no mail and cannot prove final recipient delivery.
- Commit `bc6eded`: guarded `beta.py mail-check` action invokes the probe with existing private Beta configuration. Requires exactly Beta checkout and its `api/.venv`; credentials are not displayed or copied into Development.
- Commit `b47697d`: isolated mock-provider tests for no-send diagnostic behavior.

## Operator actions

1. **Do not paste or share** `BREVO_API_KEY`, `EDUCYBER_EMAIL_SENDER`, `EDUCYBER_PUBLIC_WEB_URL` full values, real recipient addresses or password reset links. No direct database cleanup or token resets.
2. **Without updating or restarting** the existing Beta, run the one-time, read-only Python snippet supplied in the owner chat from the Beta checkout. It loads `api/.env.beta` using `dotenv_values(..., interpolate=False)`, reads account and sender metadata, and prints only configuration boolean, GET HTTP statuses and sender active/registered status.
3. Interpret findings: `account 401/403` -> Brevo API key/account/IP permission; `senders 200` but no matching/active sender -> register/verify sender or authenticate sending domain. `account 200` and active sender **do not** prove transactional sending activation or actual inbox delivery. Check Brevo dashboard **Transactional > Logs**, account credit/queue, sender domain/DKIM/DMARC, blocked contacts and transactional platform activation. Brevo's dashboard contains private details: do not post screenshots with email addresses or tokens.
4. After CI on the full hotfix head is green, fast-forward Beta through reviewed PR and restart Beta **only** if log diagnostics are required. Avoid changing configuration unless the provider probe establishes the problem; use existing guarded `beta.py configure-mail` only for approved mail settings or changed public ngrok origin.
5. Retest with **one real existing Beta account** and check: server returns a generic response; Brevo accepts the API request (check safe status log); one reset link reaches that mailbox; link uses current public ngrok origin, expires in 20 minutes, is single-use, updates password, and revokes old sessions. Failure before provider acceptance differs from successful API acceptance but later blocked/bounced mail.
6. Monitor next real requests for new `password_reset_delivery_failed provider_http_status=...` / `transport_error_type=...` metadata. Provider `2xx` means accepted, **not guaranteed delivered**.

**Do not introduce account enumeration**: never expose provider rejection status, whether the email is registered, or message tracking IDs in public forgot-password response. Do not print exception object or raw response body, which may include sensitive recipient/headers.

**No new migrations, no secret file changes, no learner-data reset or automatic mail resend.** A user must request a new link after fixing a previous failed send. Existing sessions and accounts are preserved.
