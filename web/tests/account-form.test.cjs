// Lightweight source-contract checks for the registration UX.
// These run with Node's built-in test runner (no browser or extra dependency).
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const page = fs.readFileSync(path.join(__dirname, '../app/account/page.tsx'), 'utf8');

test('registration requires matching password confirmation before HTTP request', () => {
  assert.match(page, /mode === 'register' && password !== confirmPassword/);
  assert.match(page, /Passwords do not match/);
  assert.match(page, /Confirm password/);
  assert.match(page, /autoComplete="new-password"/);
});

test('password visibility and explicit post-registration sign-in instructions exist', () => {
  assert.match(page, /type={showPassword\?'text':'password'}/);
  assert.match(page, /Show password/);
  assert.match(page, /exact password you just created/);
  assert.match(page, /setPassword\(''\)/);
});

test('login sends raw password, normalizes email and never includes confirmation', () => {
  assert.match(page, /const normalizedEmail = email\.trim\(\)\.toLowerCase\(\)/);
  assert.match(page, /\{email:normalizedEmail,password\}/);
  assert.doesNotMatch(page, /password\.trim\(\)/);
  assert.doesNotMatch(page, /JSON\.stringify\(\{[^}]*confirmPassword/);
});
