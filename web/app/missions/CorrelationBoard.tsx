'use client';
import {useState} from 'react';
type Props={evidence:string[];inspected:number[];stage:number};
type Link={from:number;to:number};
export default function CorrelationBoard({evidence,inspected,stage}:Props){
 const [links,setLinks]=useState<Link[]>([]);
 const [from,setFrom]=useState<number|null>(null);
 const [to,setTo]=useState<number|null>(null);
 const [hypothesis,setHypothesis]=useState('');
 const available=evidence.map((_,i)=>i).filter(i=>inspected.includes(i));
 const canLink=from!==null&&to!==null&&from!==to;
 function addLink(){if(!canLink)return;const a=Math.min(from!,to!),b=Math.max(from!,to!);setLinks(old=>old.some(l=>l.from===a&&l.to===b)?old:[...old,{from:a,to:b}]);setFrom(null);setTo(null);}
 return <section aria-label="Evidence correlation board" style={{marginTop:20,padding:16,border:'1px solid #35516b',borderRadius:10,background:'#0b2032',color:'#e0eef7'}}>
  <h3>Investigation board · Stage {stage+1}</h3>
  <p style={{fontSize:13,color:'#b5d0e1'}}>Connect inspected clues and write a working hypothesis. This reasoning workspace does not reveal answers or change your score.</p>
  <div style={{display:'flex',flexWrap:'wrap',gap:8,margin:'12px 0'}}>
   {evidence.map((item,i)=><div key={i} style={{flex:'1 1 170px',padding:10,border:'1px solid #35516b',borderRadius:8,opacity:inspected.includes(i)?1:.55}}>
    <strong>Artifact {i+1} {inspected.includes(i)?'✓':'· Locked'}</strong>
    <p style={{fontSize:12}}>{inspected.includes(i)?item:'Inspect this artifact in the locker first.'}</p>
   </div>)}
  </div>
  <div style={{display:'flex',gap:8,flexWrap:'wrap',alignItems:'center'}}>
   <label>From <select aria-label="First clue" value={from??''} onChange={e=>setFrom(e.target.value===''?null:Number(e.target.value))}><option value="">Select</option>{available.map(i=><option key={i} value={i}>Artifact {i+1}</option>)}</select></label>
   <label>To <select aria-label="Related clue" value={to??''} onChange={e=>setTo(e.target.value===''?null:Number(e.target.value))}><option value="">Select</option>{available.map(i=><option key={i} value={i}>Artifact {i+1}</option>)}</select></label>
   <button type="button" disabled={!canLink} onClick={addLink}>Connect clues</button>
  </div>
  <p aria-live="polite" style={{fontSize:13}}>Connections: {links.length}{links.length?': '+links.map(l=>`#${l.from+1} ↔ #${l.to+1}`).join(', '):' · none yet'}</p>
  {links.map(l=><button key={l.from+'-'+l.to} type="button" onClick={()=>setLinks(old=>old.filter(x=>x!==l))} style={{marginRight:8,marginBottom:8}}>Remove #{l.from+1} ↔ #{l.to+1}</button>)}
  <label style={{display:'block',fontWeight:600}}>Working hypothesis
   <textarea value={hypothesis} onChange={e=>setHypothesis(e.target.value)} rows={3} maxLength={1500} placeholder="What happened? Which artifacts support your interpretation?" style={{display:'block',width:'100%',boxSizing:'border-box',marginTop:6,padding:10,background:'#102d44',color:'#e0eef7',border:'1px solid #45627a',borderRadius:6}}/>
  </label>
  <small style={{color:'#a8bfd1'}}>Local scratchpad only · reset on stage change · not sent to the server.</small>
 </section>;
}
