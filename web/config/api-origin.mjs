/** Server-only proxy destination. Never expose this setting as NEXT_PUBLIC. */
export function apiOrigin(environment = process.env) {
  const raw = environment.EDUCYBER_API_ORIGIN ?? 'http://127.0.0.1:8000';
  let parsed;
  try { parsed = new URL(raw); } catch { throw new Error('Invalid API origin'); }
  if (raw !== raw.trim() || /[\\?#]/.test(raw) || parsed.username || parsed.password ||
      parsed.pathname !== '/' || !['http:', 'https:'].includes(parsed.protocol) ||
      (parsed.protocol === 'http:' && !['127.0.0.1', 'localhost', '[::1]'].includes(parsed.hostname))) {
    throw new Error('API origin must be an HTTPS origin or loopback HTTP origin');
  }
  if (environment.EDUCYBER_LOCAL_DEVELOPMENT === 'enabled' &&
      (parsed.origin !== 'http://127.0.0.1:8010' ||
       environment.NEXT_PUBLIC_API_BASE_URL)) {
    throw new Error('Isolated development requires its local API and same-origin browser requests');
  }
  return parsed.origin;
}
