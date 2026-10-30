'use client';

import { FormEvent, useState } from 'react';
import Link from 'next/link';
const API = (process.env.NEXT_PUBLIC_API_BASE_URL || '').replace(/\/$/, '');

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (busy) return;
    setBusy(true); setError('');
    try {
      const response = await fetch(API + '/api/v1/auth/forgot-password', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body:JSON.stringify({email:email.trim().toLowerCase()}),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'Please try again later.');
      setMessage(data.message);
    } catch (e) {setError(e instanceof Error ? e.message : 'Unable to send request.');}
    finally {setBusy(false);}
  }

  return <main style={{maxWidth:500,margin:'4rem auto',padding:'1.5rem',fontFamily:'system-ui'}}>
    <Link href="/account">← Back to sign in</Link>
    <h1>Forgot your password?</h1>
    <p>If an account exists for your email address, we will send a password reset link.</p>
    {!message && <form onSubmit={submit} style={{display:'grid',gap:16}}>
      <label>Email<input type="email" required autoComplete="email" value={email} onChange={e=>setEmail(e.target.value)} style={{display:'block',width:'100%',padding:12}}/></label>
      <button type="submit" disabled={busy}>{busy?'Please wait…':'Email reset link'}</button>
    </form>}
    {message && <p role="status">{message}</p>}
    {error && <p role="alert" className="status-error">{error}</p>}
  </main>;
}
