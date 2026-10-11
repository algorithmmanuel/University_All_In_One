'use client';
import {useState} from 'react';
import styles from './investigation.module.css';

type Props={missionId:string;stage:number;evidence:string[];inspected:number[];onInspect:(index:number)=>void};
const CONFIG:Record<string,{name:string;role:string;columns:[string,string,string];context:string}>={
 'risk-command':{name:'Enterprise risk register',role:'Risk manager',columns:['RISK ID','EVIDENCE','ASSESS'],context:'Review risk ownership, impact and treatment evidence.'},
 'zero-trust-briefing':{name:'Architecture assurance desk',role:'Security architect',columns:['TRUST SIGNAL','EVIDENCE','REVIEW'],context:'Inspect identity, device and workload trust controls.'},
 'cloud-incident':{name:'Cloud incident command',role:'Incident commander',columns:['CLOUD SIGNAL','EVIDENCE','REVIEW'],context:'Review fictional cloud activity and response options.'},
 'supply-chain-watch':{name:'Supplier assurance register',role:'Third-party risk lead',columns:['SUPPLIER SIGNAL','EVIDENCE','REVIEW'],context:'Validate supplier provenance and contractual response.'},
 'ransomware-recovery':{name:'Recovery coordination centre',role:'BCDR lead',columns:['RECOVERY SIGNAL','EVIDENCE','REVIEW'],context:'Prioritize continuity and verified recovery.'},
 'identity-crisis':{name:'Privileged access command',role:'Identity response lead',columns:['ACCESS SIGNAL','EVIDENCE','REVIEW'],context:'Correlate privileged sessions and access controls.'},
 'boardroom-breach':{name:'Executive situation room',role:'CISO',columns:['BOARD BRIEF','EVIDENCE','REVIEW'],context:'Balance confirmed facts, risk decisions and communications.'},
 'ai-governance':{name:'AI model risk register',role:'AI governance lead',columns:['MODEL SIGNAL','EVIDENCE','REVIEW'],context:'Review model ownership, fairness and drift evidence.'},
 'audit-trail':{name:'IT audit workpaper',role:'IT auditor',columns:['CONTROL TEST','EVIDENCE','REVIEW'],context:'Test evidence, document exceptions and validate closure.'}
};
export default function CommandInvestigation({missionId,stage,evidence,inspected,onInspect}:Props){
 const [filter,setFilter]=useState('');
 const [active,setActive]=useState<number|null>(null);
 const config=CONFIG[missionId]??{name:'Professional case desk',role:'Analyst',columns:['ID','EVIDENCE','REVIEW'] as [string,string,string],context:'Review simulated evidence.'};
 const rows=evidence.map((value,index)=>({value,index})).filter(({value,index})=>value.toLowerCase().includes(filter.toLowerCase())||String(index+1)===filter.trim());
 return <section className={styles.lab} aria-label={config.name}>
  <div className={styles.labHeader}><span>CYBER COMMAND / {config.name.toUpperCase()}</span><span>FICTIONAL · READ-ONLY</span></div>
  <div style={{padding:18}}>
   <p className={styles.hint}>ROLE: {config.role.toUpperCase()} · STAGE {stage+1} OF 3</p>
   <h4 style={{margin:'6px 0 10px'}}>{config.name}</h4>
   <p className={styles.hint}>{config.context} These records do not connect to real systems.</p>
   <label style={{display:'block',margin:'12px 0'}}>Filter evidence <input value={filter} onChange={event=>setFilter(event.target.value)} aria-label="Filter professional evidence" placeholder="Search control or indicator" style={{display:'block',width:'100%',padding:10,marginTop:6,border:'1px solid #49677d',borderRadius:8,background:'#10283d',color:'#e6f4fa'}}/></label>
   <div style={{overflowX:'auto'}}><table style={{width:'100%',borderCollapse:'collapse',textAlign:'left'}}>
    <thead><tr>{config.columns.map(label=><th key={label} style={{padding:10,borderBottom:'1px solid #49677d'}}>{label}</th>)}</tr></thead>
    <tbody>{rows.map(({value,index})=><tr key={index}>
     <td style={{padding:10}}>CC-{String(index+1).padStart(3,'0')}</td>
     <td style={{padding:10}}>{active===index?value:'Evidence available for inspection'}</td>
     <td style={{padding:10}}><button type="button" onClick={()=>{setActive(index);onInspect(index);}} aria-label={'Inspect professional evidence '+(index+1)} style={{padding:'8px 12px',border:'1px solid #4baaa2',borderRadius:8,background:'#163f49',color:'#e6f4fa',cursor:'pointer'}}>{inspected.includes(index)?'✓ Reviewed':'Inspect'}</button></td>
    </tr>)}</tbody>
   </table></div>
   {rows.length===0&&<p role="status">No matching fictional records.</p>}
   {active!==null&&evidence[active]&&<p role="status" style={{padding:14,marginTop:14,borderRadius:10,background:'#112f42'}}><strong>Reviewed evidence CC-{String(active+1).padStart(3,'0')}:</strong> {evidence[active]}</p>}
   <p className={styles.hint} style={{marginTop:14}}>{inspected.length} of {evidence.length} records inspected. Use the mission decision panel to submit an authorized response.</p>
  </div>
 </section>;
}
