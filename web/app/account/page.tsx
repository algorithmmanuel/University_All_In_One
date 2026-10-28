'use client';
import { useEffect, useRef, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

const API = (process.env.NEXT_PUBLIC_API_BASE_URL || '').replace(/\/$/, '');

export default function Account() {
  const router = useRouter();
  const [mode, setMode] = useState<'login'|'register'>('register');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [role, setRole] = useState('student');
  const [dateOfBirth, setDateOfBirth] = useState('');
  const [betaInvite, setBetaInvite] = useState('');
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [busy, setBusy] = useState(false);
  const errorHeading=useRef<HTMLParagraphElement>(null);
  const noticeHeading=useRef<HTMLParagraphElement>(null);
  useEffect(()=>{if(error)errorHeading.current?.focus();},[error]);
  useEffect(()=>{if(notice)noticeHeading.current?.focus();},[notice]);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (busy) return;
    setError(''); setNotice('');
    if (mode === 'register' && password !== confirmPassword) {
      setError('Passwords do not match. Check both password fields and try again.');
      return;
    }
    setBusy(true);
    try {
      const url = mode === 'register' ? '/api/v1/auth/register' : '/api/v1/auth/login';
      const normalizedEmail = email.trim().toLowerCase();
      // Do not trim or transform passwords: the exact bytes entered are authenticated.
      const payload = mode === 'register' ? {full_name:name,email:normalizedEmail,password,role,date_of_birth:dateOfBirth,beta_invite:betaInvite.trim()||undefined} : {email:normalizedEmail,password};
      const response = await fetch(API+url, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
      const data = await response.json();
      if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'Please check your details.');
      if (mode === 'register') {
        setNotice(data.message + '. Please sign in using the exact password you just created.');
        setMode('login'); setPassword(''); setConfirmPassword(''); setShowPassword(false);
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
      {mode==='register'&&<label>Full name<input autoComplete="name" required minLength={2} maxLength={120} value={name} onChange={e=>setName(e.target.value)} style={{display:'block',width:'100%',padding:12}}/></label>}
      {mode==='register'&&<label>Date of birth<input required autoComplete="bday" type="date" value={dateOfBirth} max={new Date().toISOString().slice(0,10)} onChange={e=>setDateOfBirth(e.target.value)} style={{display:'block',width:'100%',padding:12}}/></label>}
      {mode==='register'&&<p style={{fontSize:13,margin:0}}>Under-13 registration is not available. Ages 13–17 require guardian verification before account activation. Date of birth is self-declared and is not displayed publicly.</p>}
      {mode==='register'&&<label>Beta invitation code (if provided)<input autoComplete="off" value={betaInvite} onChange={e=>setBetaInvite(e.target.value)} style={{display:'block',width:'100%',padding:12}}/></label>}
      <label>Email<input required type="email" autoComplete="email" value={email} onChange={e=>setEmail(e.target.value)} style={{display:'block',width:'100%',padding:12}}/></label>
      <label>Password<input required type={showPassword?'text':'password'} minLength={mode==='register'?12:1} maxLength={mode==='register'?128:1024} autoComplete={mode==='register'?'new-password':'current-password'} value={password} onChange={e=>setPassword(e.target.value)} style={{display:'block',width:'100%',padding:12}}/></label>
      {mode==='register'&&<label>Confirm password<input required type={showPassword?'text':'password'} minLength={12} maxLength={128} autoComplete="new-password" value={confirmPassword} onChange={e=>setConfirmPassword(e.target.value)} style={{display:'block',width:'100%',padding:12}}/></label>}
      <label style={{display:'flex',alignItems:'center',gap:8}}><input type="checkbox" checked={showPassword} onChange={e=>setShowPassword(e.target.checked)}/>Show password{mode==='register'?'s':''}</label>
      {mode==='register'&&<p style={{fontSize:13,margin:0}}>Use at least 12 characters. Keep a secure record of your password: you will need to enter it again after registration.</p>}
      {mode==='register'&&<label>Account type<select value={role} onChange={e=>setRole(e.target.value)} style={{display:'block',width:'100%',padding:12}}><option value="student">Student</option><option value="teacher">Teacher (approval required)</option></select></label>}
      {mode==='login'&&<Link href="/forgot-password">Forgot password?</Link>}
      <button disabled={busy} type="submit" style={{padding:14,background:'#0e766f',color:'white',border:0,borderRadius:8}}>{busy?'Please wait…':mode==='register'?'Create account':'Sign in'}</button>
    </form>
    {error&&<p ref={errorHeading} tabIndex={-1} role="alert" className="status-error">{error}</p>}
    {notice&&<p ref={noticeHeading} tabIndex={-1} role="status" className="status-success">{notice}</p>}
    <p style={{fontSize:13,marginTop:24}}>Development preview. Do not use a password from another account.</p>
  </main>;
}
