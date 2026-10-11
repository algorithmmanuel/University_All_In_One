# Phase 8: Authentication Security Review

Status: initial source review; findings require validation before closure.

## Existing controls

- Passwords are salted and hashed with scrypt.
- Bearer session tokens are randomly generated and stored as hashes.
- Sessions expire after 12 hours, and logout removes the active session.
- Authentication errors do not disclose whether the email or password was incorrect.
- Teacher dashboard access requires an approved role.

## Prioritized review items

| ID | Priority | Observation | Acceptance criteria |
| --- | --- | --- | --- |
| AUTH-01 | High | No login throttling observed | Implement shared-store or gateway rate limiting and verify across multiple instances. |
| AUTH-02 | High | Password verification accepts work factors encoded in stored hashes | Validate bounded parameters and malformed hashes before running expensive hashing. |
| AUTH-03 | Medium | Registration reveals duplicate email addresses | Evaluate account enumeration and design appropriate registration responses. |
| AUTH-04 | Medium | Session lifecycle coverage is incomplete | Test expiry, logout, account disablement, and revocation. |
| AUTH-05 | Medium | No confirmed authentication audit event standard | Log security events without credentials, bearer tokens, or sensitive personal data. |
| AUTH-06 | Medium | Database dependencies are duplicated | Consolidate carefully while preserving API behavior. |
| AUTH-07 | High before public launch | Learners may include children | Complete privacy, data minimization, retention, and safeguarding assessment. |

## Implementation sequence

1. Add isolated tests for password-hash parsing, malformed parameters, session expiry, and authorization.
2. Harden password verification without changing valid stored hashes.
3. Add distributed authentication abuse protection suitable for serverless deployment.
4. Validate existing authentication contracts and run the full regression suite.
5. Record test evidence and outstanding risks in the Phase 8 register.

Do not merge security changes until the regression and targeted security tests pass.
