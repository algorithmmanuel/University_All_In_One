'use client';

import { FormEvent, Suspense, useState } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';

const API = (process.env.NEXT_PUBLIC_API_BASE_URL || '').replace(/\/$/, '');

function ResetPasswordForm() {
  const params = useSearchParams();
  const token = params.get('token') || '';
  const [password, setPassword] = useState('');
  const [confirmation, setConfirmation] = useState('');
  const [visible, setVisible] = useState(false);
  const [notice, setNotice] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (busy) return;
    setError('');
    if (password !== confirmation) {
      setError('Passwords do not match.');
      return;
    }
    setBusy(true);
    try {
      const result = await fetch(API + '/api/v1/auth/reset-password', {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({token, password}),
      });
      const data = await result.json();
      if (!result.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'Reset failed. Please request a new link.');
      setPassword(''); setConfirmation('');
      setNotice(data.message);
      // Remove bearer-equivalent token from the address bar after success.
      window.history.replaceState({}, '', '/reset-password');
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unable to reset password.');
    } finally {setBusy(false);}
  }

  return <main style={{maxWidth:500,margin:'4rem auto',padding:'1.5rem',fontFamily:'system-ui'}}>
    <Link href="/account">← Back to sign in</Link>
    <h1>Reset your password</h1>
    {!token && !notice && <p role="alert">Missing reset link. Request a new one from the sign-in page.</p>}
    {token && !notice && <form onSubmit={submit} style={{display:'grid',gap:16}}>
      <label>New password<input required type={visible?'text':'password'} minLength={12} maxLength={128} autoComplete="new-password" value={password} onChange={e=>setPassword(e.target.value)} style={{display:'block',width:'100%',padding:12}}/></label>
      <label>Confirm new password<input required type={visible?'text':'password'} minLength={12} maxLength={128} autoComplete="new-password" value={confirmation} onChange={e=>setConfirmation(e.target.value)} style={{display:'block',width:'100%',padding:12}}/></label>
      <label><input type="checkbox" checked={visible} onChange={e=>setVisible(e.target.checked)}/> Show passwords</label>
      <button disabled={busy} type="submit">{busy?'Please wait…':'Update password'}</button>
    </form>}
    {notice && <p role="status">{notice} <Link href="/account">Sign in</Link></p>}
    {error && <p role="alert" className="status-error">{error}</p>}
  </main>;
}

export default function ResetPassword() {
  return <Suspense fallback={<main>Loading password reset…</main>}><ResetPasswordForm /></Suspense>;
}
