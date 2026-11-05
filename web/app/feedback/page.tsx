'use client';
import {useEffect,useState} from 'react';
import Link from 'next/link';
import {useRouter} from 'next/navigation';

const API=(process.env.NEXT_PUBLIC_API_BASE_URL||'').replace(/\/$/,'');
export default function FeedbackPage(){
  const router=useRouter();
  const [category,setCategory]=useState('usability');
  const [rating,setRating]=useState('5');
  const [message,setMessage]=useState('');
  const [page,setPage]=useState('');
  const [status,setStatus]=useState('');
  const [busy,setBusy]=useState(false);
  useEffect(()=>{
    const context=new URLSearchParams(window.location.search).get('page');
    if(context?.startsWith('/')&&context.length<=160)setPage(context);
  },[]);
  async function submit(event:React.FormEvent<HTMLFormElement>){
    event.preventDefault();setBusy(true);setStatus('');
    const token=sessionStorage.getItem('educyber_token');
    if(!token){router.push('/account');return;}
    try{
      const res=await fetch(API+'/api/v1/beta/feedback',{method:'POST',
        headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},
        body:JSON.stringify({category,rating:Number(rating),message,page})});
      const data=await res.json();
      if(!res.ok)throw new Error(typeof data.detail==='string'?data.detail:'Submission failed');
      setStatus('Thank you. Your feedback was saved.');setMessage('');
    }catch(error){setStatus(error instanceof Error?error.message:'Unable to submit feedback');}
    finally{setBusy(false);}
  }
  return <main className="container section" style={{maxWidth:650}}>
    <Link href="/missions">← Back to missions</Link>
    <h1>Beta tester feedback</h1>
    <p>Tell us what worked, what was confusing, and what should improve. For a bug, include the journey stage, case or run identifier, steps taken, expected result and what happened. Please do not include passwords, private information, or real incident data.</p>
    <form onSubmit={submit} style={{display:'grid',gap:16}}>
      <label>Feedback type<select value={category} onChange={e=>setCategory(e.target.value)} style={{display:'block',width:'100%',padding:12}}>
        <option value="usability">Ease of use</option><option value="bug">Bug or error</option><option value="content">Learning content</option><option value="suggestion">Suggestion</option><option value="other">Other</option>
      </select></label>
      <label>Experience rating (1–5)<select value={rating} onChange={e=>setRating(e.target.value)} style={{display:'block',width:'100%',padding:12}}>
        {[1,2,3,4,5].map(n=><option key={n} value={n}>{n}</option>)}
      </select></label>
      <label>Page or mission (optional)<input maxLength={160} value={page} onChange={e=>setPage(e.target.value)} style={{display:'block',width:'100%',padding:12}}/></label>
      <label>What happened, and what should we improve?<textarea required minLength={10} maxLength={2000} rows={7} value={message} onChange={e=>setMessage(e.target.value)} style={{display:'block',width:'100%',padding:12}}/></label>
      <button className="btn" type="submit" disabled={busy}>{busy?'Submitting…':'Submit feedback'}</button>
    </form>
    {status&&<p role="status">{status}</p>}
  </main>;
}
