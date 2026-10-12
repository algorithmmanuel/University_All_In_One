# EduCyber Nigeria password recovery (private beta)

## Security model
The API accepts `POST /api/v1/auth/forgot-password` (email) and
`POST /api/v1/auth/reset-password` (token, password). Requests for unknown
or inactive accounts return the same 202 response as known accounts.
Reset tokens are generated randomly, stored only as SHA-256 hashes, expire
after 20 minutes and can be redeemed once. Password changes invalidate all
existing sessions; invitation associations and learner progress are preserved.

## Brevo setup
Configure on the **API server only**, never in NEXT_PUBLIC_ variables:
- `BREVO_API_KEY`: transactional-email API key.
- `EDUCYBER_EMAIL_SENDER`: verified sender email in Brevo.
- `EDUCYBER_PUBLIC_WEB_URL`: external HTTPS web URL where the reset page
  is reachable, e.g. https://<your-current-public-web-host>.
Use localhost HTTP URLs only for local development. Do not store these
values in Git or paste them into support messages.

API access to `https://api.brevo.com/v3/smtp/email` must be enabled.
Reset links are sensitive credentials. Do not add analytics, external assets
or third-party trackers to the password reset page. Configure
`Referrer-Policy: no-referrer` and `Cache-Control: no-store` at your edge
for /reset-password and avoid access logging query strings. Rotate your
ngrok/web URL in the API setting if it changes.

## Migration and verification
Apply Alembic migration 0009 only after verifying the target database.
Never run test schema reset scripts against the main `educyber` database.
Run tests against `educyber_test` on localhost:5434.
Do not infer which database the running server uses from a separate shell's
`DATABASE_URL`; verify the **running API process environment** locally,
without printing passwords or complete connection strings.

## Before public rollout
Add trusted-proxy edge/IP quotas, security monitoring and delivery-failure
alerts. Verify sender domain SPF/DKIM, email delivery, link click-through,
token replay rejection and session invalidation using controlled beta accounts.
