'use client';
import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

const API = (process.env.NEXT_PUBLIC_API_BASE_URL || '').replace(/\/$/, '');

export default function Account() {
  const router = useRouter();
  const [mode, setMode] = useState<'login'|'register'>('register');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('student');
  const [dateOfBirth, setDateOfBirth] = useState('');
  const [betaInvite, setBetaInvite] = useState('');
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [busy, setBusy] = useState(false);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError(''); setNotice(''); setBusy(true);
    try {
      const url = mode === 'register' ? '/api/v1/auth/register' : '/api/v1/auth/login';
      const payload = mode === 'register' ? {full_name:name,email,password,role,date_of_birth:dateOfBirth,beta_invite:betaInvite||undefined} : {email,password};
      const response = await fetch(API+url, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
      const data = await response.json();
      if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'Please check your details.');
      if (mode === 'register') {
        setNotice(data.message + '. Please sign in.');
        setMode('login'); setPassword('');
      } else {
        sessionStorage.setItem('educyber_token',data.access_token);
        router.push('/dashboard');
      }
    } catch (e) {setError(e instanceof Error ? e.message : 'Unable to connect to the API');}
    finally {setBusy(false);}
  }

  return <main style={{maxWidth:500,margin:'4rem auto',padding:'1.5rem',fontFamily:'system-ui'}}>
    <Link href="/">← EduCyber Nigeria</Link>
    <h1>{mode==='register'?'Create your account':'Welcome back'}</h1>
    <p>Learn and teach on EduCyber Nigeria.</p>
    <div style={{display:'flex',gap:12,marginBottom:24}}>
      <button onClick={()=>{setMode('register');setError('');}} aria-pressed={mode==='register'}>Register</button>
      <button onClick={()=>{setMode('login');setError('');}} aria-pressed={mode==='login'}>Sign in</button>
    </div>
    <form onSubmit={submit} style={{display:'grid',gap:16}}>
      {mode==='register'&&<label>Full name<input required minLength={2} maxLength={120} value={name} onChange={e=>setName(e.target.value)} style={{display:'block',width:'100%',padding:12}}/></label>}
      {mode==='register'&&<label>Date of birth<input required type="date" value={dateOfBirth} max={new Date().toISOString().slice(0,10)} onChange={e=>setDateOfBirth(e.target.value)} style={{display:'block',width:'100%',padding:12}}/></label>}
      {mode==='register'&&<p style={{fontSize:13,margin:0}}>Under-13 registration is not available. Ages 13–17 require guardian verification before account activation. Date of birth is self-declared and is not displayed publicly.</p>}
      {mode==='register'&&<label>Beta invitation code (if provided)<input autoComplete="off" value={betaInvite} onChange={e=>setBetaInvite(e.target.value)} style={{display:'block',width:'100%',padding:12}}/></label>}
      <label>Email<input required type="email" autoComplete="email" value={email} onChange={e=>setEmail(e.target.value)} style={{display:'block',width:'100%',padding:12}}/></label>
      <label>Password<input required type="password" minLength={mode==='register'?12:1} autoComplete={mode==='register'?'new-password':'current-password'} value={password} onChange={e=>setPassword(e.target.value)} style={{display:'block',width:'100%',padding:12}}/></label>
      {mode==='register'&&<label>Account type<select value={role} onChange={e=>setRole(e.target.value)} style={{display:'block',width:'100%',padding:12}}><option value="student">Student</option><option value="teacher">Teacher (approval required)</option></select></label>}
      <button disabled={busy} type="submit" style={{padding:14,background:'#0e766f',color:'white',border:0,borderRadius:8}}>{busy?'Please wait…':mode==='register'?'Create account':'Sign in'}</button>
    </form>
    {error&&<p role="alert" style={{color:'#b42318'}}>{error}</p>}
    {notice&&<p role="status" style={{color:'#087443'}}>{notice}</p>}
    <p style={{fontSize:13,marginTop:24}}>Development preview. Do not use a password from another account.</p>
  </main>;
}
