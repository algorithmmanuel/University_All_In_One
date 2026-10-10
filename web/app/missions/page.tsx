'use client';
import {useCallback,useEffect,useState} from 'react';
import Link from 'next/link';
import {useRouter} from 'next/navigation';

const API=(process.env.NEXT_PUBLIC_API_BASE_URL||'http://127.0.0.1:8000').replace(/\/$/,'');
type Mission={id:string;title:string;track:string;difficulty:string;summary:string;step_count:number;latest_run:null|{run_id:number;completed:boolean;score:number;step_index:number}};
type Step={scene:string;story:string;evidence:string[];question:string;options:string[]};
type Run={run_id:number;mission_id:string;title:string;step_index:number;step_count:number;score:number;max_score:number;completed:boolean;step:Step|null;last_feedback:string|null};
type History={id:number;title:string;score:number;max_score:number;completed:boolean;created_at:string};

export default function Missions(){
  const router=useRouter();
  const [missions,setMissions]=useState<Mission[]>([]);
  const [history,setHistory]=useState<History[]>([]);
  const [run,setRun]=useState<Run|null>(null);
  const [selection,setSelection]=useState<number|null>(null);
  const [feedback,setFeedback]=useState('');
  const [busy,setBusy]=useState(false);
  const [error,setError]=useState('');
  const [loading,setLoading]=useState(true);
  const request=useCallback(async(path:string,method='GET',body?:object)=>{
    const token=sessionStorage.getItem('educyber_token');
    if(!token){router.replace('/account');throw new Error('Sign in to continue');}
    const res=await fetch(API+path,{method,headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},...(body?{body:JSON.stringify(body)}:{})});
    const data=await res.json();
    if(!res.ok){
      if(res.status===401){sessionStorage.removeItem('educyber_token');router.replace('/account');}
      throw new Error(typeof data.detail==='string'?data.detail:'Request failed');
    }
    return data;
  },[router]);
  const refresh=useCallback(async()=>{
    const [catalog,attempts]=await Promise.all([request('/api/v1/missions'),request('/api/v1/missions/history')]);
    setMissions(catalog.missions);setHistory(attempts.runs);
  },[request]);
  useEffect(()=>{refresh().catch(e=>setError(e.message)).finally(()=>setLoading(false));},[refresh]);

  async function start(id:string){
    setBusy(true);setError('');setFeedback('');
    try{setRun(await request('/api/v1/missions/'+id+'/start','POST'));setSelection(null);await refresh();}
    catch(e){setError(e instanceof Error?e.message:'Unable to start mission');}
    finally{setBusy(false);}
  }
  async function resume(id:number){
    setBusy(true);setError('');setFeedback('');
    try{setRun(await request('/api/v1/missions/runs/'+id));setSelection(null);}
    catch(e){setError(e instanceof Error?e.message:'Unable to resume mission');}
    finally{setBusy(false);}
  }
  async function decide(){
    if(!run||selection===null||run.completed)return;
    setBusy(true);setError('');
    try{
      const next=await request('/api/v1/missions/runs/'+run.run_id+'/decide','POST',
        {option_index:selection,expected_step:run.step_index});
      setRun(next);setFeedback(next.last_feedback||'');setSelection(null);await refresh();
    }catch(e){setError(e instanceof Error?e.message:'Unable to save decision');}
    finally{setBusy(false);}
  }

  return <main className="container section" style={{maxWidth:1050}}>
    <Link href="/dashboard">← Dashboard</Link>
    <p className="tag">EDUCYBER SIMULATION LAB</p>
    <h1>Cybersecurity missions</h1>
    <p className="muted">Explore fictional incidents, examine evidence and make defensive decisions. All activity is simulated.</p>
    {error&&<p role="alert" style={{color:'#b42318'}}>{error}</p>}
    {loading?<p>Loading missions…</p>:<>
      <div className="grid">
        {missions.map(m=><article className="card" key={m.id}>
          <p className="tag">{m.track} · {m.difficulty}</p>
          <h2 style={{fontSize:23}}>{m.title}</h2>
          <p className="muted">{m.summary}</p>
          <p className="small">{m.step_count} decisions · {m.step_count*10} possible points</p>
          {m.latest_run&&!m.latest_run.completed&&<button className="btn" disabled={busy}
            onClick={()=>resume(m.latest_run!.run_id)}>Resume mission</button>}
          <button className="btn secondary" style={{marginLeft:8,border:'1px solid #b5c7d3'}} disabled={busy}
            onClick={()=>start(m.id)}>{m.latest_run?'New attempt':'Start mission'}</button>
        </article>)}
      </div>
      {run&&<section className="section" id="mission-console">
        <div className="panel" style={{background:'#112944',color:'white'}}>
          <p className="tag" style={{color:'#82e4d0'}}>MISSION CONSOLE · {run.title}</p>
          <h2>{run.completed?'Mission complete':run.step?.scene}</h2>
          <p>Decision {Math.min(run.step_index+1,run.step_count)} of {run.step_count} · Score {run.score}/{run.max_score}</p>
          <progress value={run.step_index} max={run.step_count} style={{width:'100%'}} aria-label="Mission progress"/>
          {feedback&&<p role="status" style={{background:'#234763',padding:14,borderRadius:8}}>Analyst feedback: {feedback}</p>}
          {run.completed?<><h3>Final score: {run.score}/{run.max_score}</h3>
            <p>Your mission result has been saved. Review your decision feedback or try another run.</p>
            <button className="btn" onClick={()=>start(run.mission_id)} disabled={busy}>Replay mission</button></>:
          run.step&&<>
            <p style={{lineHeight:1.8}}>{run.step.story}</p>
            <h3>Evidence</h3>
            <ul>{run.step.evidence.map((item,i)=><li key={i}>{item}</li>)}</ul>
            <h3>{run.step.question}</h3>
            <div style={{display:'grid',gap:10}}>
              {run.step.options.map((option,i)=><label key={i} style={{display:'block',background:selection===i?'#215f75':'#24425c',padding:14,borderRadius:9,cursor:'pointer'}}>
                <input type="radio" name="decision" checked={selection===i} onChange={()=>setSelection(i)} disabled={busy}/> {option}
              </label>)}
            </div>
            <button className="btn" style={{marginTop:20}} disabled={busy||selection===null} onClick={decide}>Confirm decision →</button>
          </>}
        </div>
      </section>}
      <section className="section">
        <h2>Mission history</h2>
        {history.length===0?<p className="muted">Your first mission is waiting.</p>:<div className="card">
          {history.map(h=><p key={h.id}>{h.title} — {h.completed?'Completed':'In progress'} · {h.score}/{h.max_score} points · {new Date(h.created_at).toLocaleString()}</p>)}
        </div>}
      </section>
    </>}
  </main>;
}
