'use client';
import {useEffect,useState} from 'react';
import Link from 'next/link';

type Game={pathway:'secondary'|'university'|'professional';status:'playable'|'planned'};
const PATHS=[['secondary','Cyber Explorers'],['university','Cyber Academy'],['professional','Cyber Command']] as const;
const API=(process.env.NEXT_PUBLIC_API_BASE_URL||'').replace(/\/$/,'');
export default function DashboardGamePaths(){
 const [games,setGames]=useState<Game[]|null>(null);
 const [error,setError]=useState(false);
 useEffect(()=>{
  const controller=new AbortController();
  fetch(API+'/api/v1/games',{signal:controller.signal}).then(async response=>{
   if(!response.ok)throw new Error('Catalogue unavailable');
   const data:unknown=await response.json();
   if(!data||typeof data!=='object'||!Array.isArray((data as {games?:unknown}).games))throw new Error('Invalid catalogue');
   const rows=(data as {games:unknown[]}).games;
   if(!rows.every(row=>typeof row==='object'&&row!==null&&['secondary','university','professional'].includes((row as Game).pathway)&&['playable','planned'].includes((row as Game).status)))throw new Error('Invalid games');
   setGames(rows as Game[]);
  }).catch(()=>{if(!controller.signal.aborted)setError(true)});
  return ()=>controller.abort();
 },[]);
 return <section style={{marginTop:26}} aria-label="Cybersecurity games">
  <h2>Cybersecurity game library</h2>
  <p>Choose a learning pathway to access simulated 2D and 3D cybersecurity missions.</p>
  {error?<p role="status">Game counts unavailable. <Link href="/missions">Open missions</Link></p>:
   !games?<p role="status">Loading game library…</p>:
   <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(190px,1fr))',gap:12}}>
    {PATHS.map(([id,title])=><article key={id} style={{padding:16,border:'1px solid #49677d',borderRadius:12,background:'#112f42',color:'#e6f4fa'}}>
     <h3 style={{margin:'0 0 8px'}}>{title}</h3>
     <p>{games.filter(g=>g.pathway===id&&g.status==='playable').length} playable games</p>
     <Link href={'/missions?pathway='+id} style={{color:'#8be8d9'}}>Open pathway →</Link>
    </article>)}
   </div>}
 </section>;
}
