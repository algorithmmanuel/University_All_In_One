'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import DashboardGamePaths from './DashboardGamePaths';

const API = (process.env.NEXT_PUBLIC_API_BASE_URL || '').replace(/\/$/, '');
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

  return <main className="cyber-dashboard">
    <header className="cyber-topbar">
      <Link className="cyber-logo" href="/">⬡ EduCyber <span>Nigeria</span></Link>
      <nav aria-label="Dashboard navigation">
        <Link href="/learn">Courses</Link>
        <Link href="/missions">Missions</Link>
        <Link href="/assessments">Assessments</Link>
        <Link href="/feedback">Feedback</Link>
      </nav>
      <button className="cyber-signout" onClick={signOut}>Sign out</button>
    </header>
    {error?<section className="cyber-shell"><h1>Unable to load dashboard</h1><p role="alert">{error}</p><button className="btn" onClick={signOut}>Sign in again</button></section>:
      !user?<div className="cyber-shell" role="status">Loading your dashboard…</div>:<>
        <section className="cyber-hero">
          <div className="cyber-shell cyber-hero-inner">
            <div className="cyber-hero-copy">
              <span className="cyber-eyebrow">LEARN · INVESTIGATE · DEFEND · GROW</span>
              <p className="cyber-greeting">Welcome back, {user.full_name}</p>
              <h1>Build your skills.<br/><span>Defend the digital world.</span></h1>
              <p className="cyber-description">Explore practical cybersecurity courses, test your knowledge, and take on immersive security missions. Your next challenge starts here.</p>
              <div className="cyber-actions">
                <Link className="cyber-cta" href="/missions">Explore cyber missions →</Link>
                <Link className="cyber-cta cyber-cta-outline" href="/learn">Browse courses →</Link>
              </div>
              <div className="cyber-meta"><span>◈ Hands-on learning</span><span>◎ Real scenarios</span><span>✦ Track your progress</span></div>
            </div>
            <div className="cyber-hero-art" aria-hidden="true"><div className="cyber-orbit"><span>⌁</span></div><div className="cyber-console"><div>SECURITY OPERATIONS</div><strong>THREAT MONITOR</strong><span>● ANALYSE &nbsp; ● RESPOND &nbsp; ● LEARN</span><div className="cyber-bars"><i/><i/><i/><i/><i/><i/><i/></div></div></div>
          </div>
        </section>
        <section className="cyber-shell cyber-content">
          {user.role==='teacher'&&!user.is_approved?<div className="cyber-feature"><h2>Teacher approval pending</h2><p>Your account is registered. Teaching tools will be available after administrator approval.</p></div>:
           user.role==='teacher'||user.role==='admin'?<div className="cyber-feature"><h2>Teacher workspace</h2><p>Course authoring and learner reporting are being developed.</p></div>:
           <>
            <div className="cyber-section-heading"><div><span className="cyber-eyebrow">YOUR CYBER JOURNEY</span><h2>Choose your next challenge</h2></div><p>Start learning, put your skills to work, or measure your progress.</p></div>
            <div className="cyber-feature-grid">
              <Link className="cyber-feature cyber-feature-courses" href="/learn"><span className="cyber-feature-icon">▤</span><h3>Interactive courses</h3><p>Build your foundations through structured lessons and practical exercises.</p><span className="cyber-feature-link">Start learning ↗</span></Link>
              <Link className="cyber-feature cyber-feature-missions" href="/missions"><span className="cyber-feature-icon">⌘</span><h3>Cybersecurity missions</h3><p>Investigate simulated threats, analyse evidence and make security decisions.</p><span className="cyber-feature-link">Enter mission control ↗</span></Link>
              <Link className="cyber-feature cyber-feature-assessments" href="/assessments"><span className="cyber-feature-icon">◇</span><h3>Knowledge assessments</h3><p>Challenge yourself with expanded course quizzes and saved results.</p><span className="cyber-feature-link">Take an assessment ↗</span></Link>
            </div>
           </>}
          <div className="cyber-library"><DashboardGamePaths /></div>
          <div className="cyber-feedback-banner"><div><h2>Help shape EduCyber Nigeria</h2><p>Found a bug or have an idea? Send feedback directly from your beta account.</p></div><Link className="cyber-cta cyber-cta-outline" href="/feedback">Share feedback →</Link></div>
        </section>
      </>}
  </main>;
}
