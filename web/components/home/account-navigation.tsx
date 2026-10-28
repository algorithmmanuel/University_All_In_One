'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {signOutLocally} from '../../lib/sign-out';

const API=(process.env.NEXT_PUBLIC_API_BASE_URL||'').replace(/\/$/,'');
export function AccountNavigation(){
  const router=useRouter();
  const [signedIn,setSignedIn]=useState(false);
  const [busy,setBusy]=useState(false);
  useEffect(()=>{
    const sync=()=>setSignedIn(Boolean(sessionStorage.getItem('educyber_token')));
    sync();
    window.addEventListener('focus',sync);
    return ()=>window.removeEventListener('focus',sync);
  },[]);
  async function logout(){
    if(busy)return;
    setBusy(true);
    await signOutLocally(API);
    setSignedIn(false);setBusy(false);router.replace('/account');
  }
  return <nav className="account-nav" aria-label="Account navigation">
    {signedIn?<><Link href="/dashboard">Dashboard</Link><Link href="/missions">Games</Link><button type="button" className="btn secondary" disabled={busy} onClick={logout} aria-label="Sign out of EduCyber Nigeria">{busy?'Signing out…':'Sign out ↗'}</button></>:
      <Link className="btn secondary" href="/account">Sign in / Register</Link>}
  </nav>;
}

