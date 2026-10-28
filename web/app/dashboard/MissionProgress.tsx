'use client';
import {useEffect,useState} from 'react';
import Link from 'next/link';
const API=(process.env.NEXT_PUBLIC_API_BASE_URL||'').replace(/\/$/,'');
type Progress={completed_missions:number;active_missions:number;available_missions:number;recent_missions:{run_id:number;title:string;score:number;max_score:number;completed_stages:number;total_stages:number;completed:boolean}[]};
export default function MissionProgress(){
  const [data,setData]=useState<Progress|null>(null),[error,setError]=useState(false),[retry,setRetry]=useState(0);
  useEffect(()=>{
    const controller=new AbortController();setError(false);
    fetch(API+'/api/v1/missions/progress',{headers:{Authorization:'Bearer '+sessionStorage.getItem('educyber_token')},signal:controller.signal})
      .then(async response=>{if(!response.ok)throw new Error();const value=await response.json();if(!Array.isArray(value.recent_missions))throw new Error();return value;})
      .then(value=>{if(!controller.signal.aborted)setData(value);}).catch(()=>{if(!controller.signal.aborted)setError(true);});
    return ()=>controller.abort();
  },[retry]);
  return <section className="learning-overview" aria-labelledby="mission-progress-heading">
    <h2 id="mission-progress-heading">Your mission progress</h2>
    {error?<><p role="alert">Mission progress is unavailable.</p><button className="btn" onClick={()=>setRetry(value=>value+1)}>Retry mission progress</button></>:
      !data?<p role="status">Loading mission progress…</p>:<>
        <p>{data.completed_missions} of {data.available_missions} missions completed at least once · {data.active_missions} latest attempts in progress</p>
        <p className="small">Activity and simulation points are not proof of mastery. Replays do not count as new distinct completed missions.</p>
        {data.recent_missions.length===0?<p>No mission attempts yet. <Link href="/missions">Choose your first mission</Link>.</p>:
          <div className="grid">{data.recent_missions.map(run=><article className="card" key={run.run_id}>
            <h3>{run.title}</h3><p>{run.completed?'Completed':`${run.completed_stages} of ${run.total_stages} stages complete`} · {run.score}/{run.max_score} simulation points</p>
            <Link href={`/missions?run=${run.run_id}`}>{run.completed?'Review saved mission result':'Resume saved mission'}: {run.title}</Link>
          </article>)}</div>}
        <p><Link href="/missions">Open all missions and saved history →</Link></p>
      </>}
  </section>;
}
