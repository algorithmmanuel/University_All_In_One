'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

const API = (process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');
type Profile = {id:number;full_name:string;email:string;role:string;is_approved:boolean};

export default function Dashboard() {
  const router=useRouter();
  const [user,setUser]=useState<Profile|null>(null);
  const [error,setError]=useState('');
  useEffect(()=>{
    const token=sessionStorage.getItem('educyber_token');
    if(!token){router.replace('/account');return;}
    const controller=new AbortController();
    fetch(API+'/api/v1/dashboard',{headers:{Authorization:'Bearer '+token},signal:controller.signal})
      .then(async r=>{if(!r.ok)throw new Error('Session expired. Please sign in again.');return r.json();})
      .then(data=>setUser(data.user))
      .catch(e=>{if(!controller.signal.aborted)setError(e.message);});
    return ()=>controller.abort();
  },[router]);

  async function signOut(){
    const token=sessionStorage.getItem('educyber_token');
    if(token){try{await fetch(API+'/api/v1/auth/logout',{method:'POST',headers:{Authorization:'Bearer '+token}});}catch{}}
    sessionStorage.removeItem('educyber_token');router.replace('/account');
  }

  return <main style={{maxWidth:900,margin:'3rem auto',padding:'1.5rem',fontFamily:'system-ui'}}>
    <Link href="/">← EduCyber Nigeria</Link>
    {error?<><h1>Unable to load dashboard</h1><p role="alert">{error}</p><button onClick={signOut}>Sign in again</button></>:
      !user?<p role="status">Loading your dashboard…</p>:<>
        <h1>Welcome, {user.full_name}</h1>
        <p>{user.email} · {user.role}</p>
        <section style={{background:'#eef7f6',padding:24,borderRadius:12,marginTop:24}}>
          {user.role==='teacher'&&!user.is_approved?<><h2>Teacher approval pending</h2><p>Your account is registered. Teaching tools will be available after administrator approval.</p></>:
          user.role==='teacher'||user.role==='admin'?<><h2>Teacher workspace</h2><p>Course authoring, lesson management and learner reporting will be added next.</p></>:
          <><h2>Your learning dashboard</h2><p>Explore the academies and the cybersecurity practice mission. Enroll in courses, complete lessons and track your progress.</p><Link href="/learn" style={{display:'inline-block',padding:'12px 18px',background:'#0e766f',color:'white',borderRadius:8,textDecoration:'none'}}>Browse courses and start learning →</Link></>}
        </section>
        <button onClick={signOut} style={{marginTop:24,padding:12}}>Sign out</button>
      </>}
  </main>;
}
