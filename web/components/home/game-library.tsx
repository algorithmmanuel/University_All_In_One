'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';

type Game = { id:string; pathway:'secondary'|'university'|'professional'; title:string; mechanic:string; summary:string; status:'playable'|'planned'; mission_ids:string[] };
const PATHS = [['secondary','Cyber Explorers'],['university','Cyber Academy'],['professional','Cyber Command']] as const;
const BASE=(process.env.NEXT_PUBLIC_API_BASE_URL||'http://127.0.0.1:8000').replace(/\/$/,'');

function isGame(value:unknown):value is Game {
  if(!value||typeof value!=='object')return false;
  const g=value as Record<string,unknown>;
  return typeof g.id==='string'&&typeof g.title==='string'&&typeof g.mechanic==='string'&&typeof g.summary==='string'
    &&PATHS.some(([id])=>id===g.pathway)&&(g.status==='playable'||g.status==='planned')
    &&Array.isArray(g.mission_ids)&&g.mission_ids.every(x=>typeof x==='string')
    &&(g.status==='planned'?g.mission_ids.length===0:g.mission_ids.length>0);
}

export function GameLibrary(){
  const [games,setGames]=useState<Game[]>([]);
  const [selected,setSelected]=useState<Game['pathway']>('secondary');
  const [status,setStatus]=useState<'loading'|'ready'|'offline'>('loading');
  useEffect(()=>{
    const controller=new AbortController();
    fetch(BASE+'/api/v1/games',{signal:controller.signal}).then(async response=>{
      if(!response.ok)throw new Error('Catalogue unavailable');
      const payload:unknown=await response.json();
      if(!payload||typeof payload!=='object'||!Array.isArray((payload as {games?:unknown}).games))throw new Error('Invalid catalogue');
      const rows=(payload as {games:unknown[]}).games;
      if(!rows.every(isGame)||PATHS.some(([id])=>rows.filter(g=>(g as Game).pathway===id).length!==10))throw new Error('Invalid catalogue');
      setGames(rows as Game[]);setStatus('ready');
    }).catch(()=>{if(!controller.signal.aborted)setStatus('offline')});
    return ()=>controller.abort();
  },[]);
  const current=games.filter(g=>g.pathway===selected);
  return <section id="game-library" className="container section" aria-label="Cybersecurity game library">
    <p className="tag">CYBER GAME LIBRARY</p><h2>Explore 30 cyber game concepts</h2>
    <p className="muted">Ten titles per pathway. Playable games are clearly identified; new simulations are being developed.</p>
    <div className="actions" role="group" aria-label="Select game pathway">
      {PATHS.map(([id,label])=><button type="button" className={selected===id?'btn':'btn secondary'} aria-pressed={selected===id} key={id} onClick={()=>setSelected(id)}>{label}</button>)}
    </div>
    {status==='loading'?<p role="status">Loading game catalogue…</p>:status==='offline'?<div className="notice" role="status">Game catalogue unavailable. Start the FastAPI backend to load all 30 titles.</div>:<>
      <p className="small" role="status">{current.filter(g=>g.status==='playable').length} playable now · {current.filter(g=>g.status==='planned').length} in development</p>
      <div className="grid">{current.map(g=><article className="card" key={g.id}>
        <span className="tag">{g.status==='playable'?'PLAYABLE NOW':'COMING SOON'}</span>
        <h3>{g.title}</h3><p className="small">{g.mechanic}</p><p className="muted">{g.summary}</p>
        {g.status==='playable'?<Link className="btn" href="/missions">Open game →</Link>:<p className="small">Scenario development in progress</p>}
      </article>)}</div>
    </>}
  </section>;
}
