const {test} = require('node:test');
const assert = require('node:assert/strict');

test('proxy preserves beta default and accepts explicit loopback or HTTPS origins', async () => {
  const {apiOrigin} = await import('../config/api-origin.mjs');
  assert.equal(apiOrigin({}), 'http://127.0.0.1:8000');
  assert.equal(apiOrigin({EDUCYBER_API_ORIGIN:'http://127.0.0.1:8010/'}), 'http://127.0.0.1:8010');
  assert.equal(apiOrigin({EDUCYBER_API_ORIGIN:'https://api.example.com'}), 'https://api.example.com');
});

test('proxy rejects credentials, paths, queries and non-loopback plaintext', async () => {
  const {apiOrigin} = await import('../config/api-origin.mjs');
  for (const value of ['', 'garbage', 'http://remote.example', 'file:///tmp/a',
    'https://user:password@api.example.com', 'https://api.example.com/v1',
    'https://api.example.com?host=other', 'https://api.example.com#fragment',
    ' https://api.example.com']) {
    assert.throws(() => apiOrigin({EDUCYBER_API_ORIGIN:value}), value);
  }
});

test('isolated development fails closed if destination or browser override targets beta', async () => {
  const {apiOrigin} = await import('../config/api-origin.mjs');
  const env = {EDUCYBER_LOCAL_DEVELOPMENT:'enabled', EDUCYBER_API_ORIGIN:'http://127.0.0.1:8010'};
  assert.equal(apiOrigin(env), env.EDUCYBER_API_ORIGIN);
  assert.throws(() => apiOrigin({...env, EDUCYBER_API_ORIGIN:'http://127.0.0.1:8000'}));
  assert.throws(() => apiOrigin({...env, NEXT_PUBLIC_API_BASE_URL:'http://127.0.0.1:8000'}));
  assert.throws(() => apiOrigin({EDUCYBER_LOCAL_DEVELOPMENT:'enabled'}));
});

test('API and health rewrites use the same configured backend and retain reset headers', async () => {
  const {default:config} = await import('../next.config.mjs');
  const previous = process.env.EDUCYBER_API_ORIGIN;
  const previousMode = process.env.EDUCYBER_LOCAL_DEVELOPMENT;
  try {
    process.env.EDUCYBER_API_ORIGIN = 'https://api.example.com';
    delete process.env.EDUCYBER_LOCAL_DEVELOPMENT;
    assert.deepEqual(await config.rewrites(), [
      {source:'/api/v1/:path*', destination:'https://api.example.com/api/v1/:path*'},
      {source:'/health/:path*', destination:'https://api.example.com/health/:path*'},
    ]);
    const reset = (await config.headers()).find(item => item.source === '/reset-password');
    assert.ok(reset.headers.some(item => item.key === 'Referrer-Policy' && item.value === 'no-referrer'));
    assert.ok(reset.headers.some(item => item.key === 'Cache-Control' && item.value === 'no-store'));
  } finally {
    if (previous === undefined) delete process.env.EDUCYBER_API_ORIGIN;
    else process.env.EDUCYBER_API_ORIGIN = previous;
    if (previousMode === undefined) delete process.env.EDUCYBER_LOCAL_DEVELOPMENT;
    else process.env.EDUCYBER_LOCAL_DEVELOPMENT = previousMode;
  }
});
