'use client';
import {useState} from 'react';
import styles from './investigation.module.css';

type Props={missionId:string;stage:number;evidence:string[];inspected:number[];onInspect:(index:number)=>void};
type Config={title:string;columns:[string,string,string];note:string};
const CONFIG:Record<string,Config>={
 'network-watch':{title:'Network flow analyzer',columns:['SIGNAL','OBSERVATION','REVIEW'],note:'Simulated flow records; no real packet capture.'},
 'web-defense':{title:'Web security review console',columns:['REQUEST SIGNAL','OBSERVATION','REVIEW'],note:'Fictional web application; no payload execution.'},
 'cloud-perimeter':{title:'Cloud configuration inspector',columns:['CONTROL','OBSERVATION','REVIEW'],note:'Read-only fictional cloud configuration.'},
 'forensics-desk':{title:'Forensic evidence register',columns:['EVIDENCE ID','OBSERVATION','CHAIN'],note:'Synthetic artifacts; maintain a documented evidence trail.'},
 'malware-clues':{title:'Static analysis workbench',columns:['INDICATOR','OBSERVATION','REVIEW'],note:'No executable samples or live detonation.'},
 'identity-lab':{title:'Identity and access review',columns:['ACCESS SIGNAL','OBSERVATION','REVIEW'],note:'Synthetic sign-in and privilege data.'},
 'secure-code-review':{title:'CI security findings',columns:['CONTROL','OBSERVATION','REVIEW'],note:'Fictional pipeline records; no credentials are present.'},
 'threat-hunter':{title:'Threat hypothesis workspace',columns:['HUNT SIGNAL','OBSERVATION','REVIEW'],note:'Synthetic telemetry; defensive hypothesis validation only.'}
};
export default function AcademyInvestigation({missionId,stage,evidence,inspected,onInspect}:Props){
 const [selected,setSelected]=useState<number|null>(null);
 const [query,setQuery]=useState('');
 const config=CONFIG[missionId]??{title:'Evidence workspace',columns:['ID','OBSERVATION','REVIEW'] as [string,string,string],note:'Fictional training artifacts.'};
 const matches=evidence.map((value,index)=>({value,index})).filter(row=>row.value.toLowerCase().includes(query.trim().toLowerCase())||String(row.index+1)===query.trim());
 return <section className={styles.lab} aria-label={config.title}>
  <div className={styles.labHeader}><span>ACADEMY LAB / {config.title.toUpperCase()}</span><span>SIMULATED · READ-ONLY</span></div>
  <div style={{padding:18}}>
   <h4 style={{margin:'0 0 10px'}}>{config.title} · Stage {stage+1}</h4>
   <p className={styles.hint}>{config.note} Search the evidence register, select a record, and mark it inspected.</p>
   <label style={{display:'block',marginBottom:12}}>Filter evidence <input aria-label="Filter academy evidence" value={query} onChange={event=>setQuery(event.target.value)} placeholder="Search signals or record number" style={{display:'block',width:'100%',padding:10,marginTop:6,borderRadius:8,background:'#10283d',color:'#e6f4fa',border:'1px solid #49677d'}}/></label>
   <div style={{overflowX:'auto'}}>
    <table style={{width:'100%',borderCollapse:'collapse',textAlign:'left'}}>
     <thead><tr>{config.columns.map(column=><th key={column} style={{padding:10,borderBottom:'1px solid #49677d'}}>{column}</th>)}</tr></thead>
     <tbody>{matches.map(({value,index})=><tr key={index}>
      <td style={{padding:10}}>EV-{String(index+1).padStart(3,'0')}</td>
      <td style={{padding:10}}>{selected===index?value:'Select to inspect this record'}</td>
      <td style={{padding:10}}><button type="button" onClick={()=>{setSelected(index);onInspect(index);}} aria-label={'Inspect evidence '+(index+1)} style={{padding:'8px 12px',borderRadius:8,background:'#163f49',border:'1px solid #4baaa2',color:'#e6f4fa',cursor:'pointer'}}>{inspected.includes(index)?'✓ Reviewed':'Inspect'}</button></td>
     </tr>)}</tbody>
    </table>
   </div>
   {matches.length===0&&<p role="status">No matching simulated records.</p>}
   {selected!==null&&evidence[selected]&&<p role="status" style={{padding:14,background:'#112f42',borderRadius:10,marginTop:14}}><strong>Evidence EV-{String(selected+1).padStart(3,'0')}:</strong> {evidence[selected]}</p>}
   <p className={styles.hint} style={{marginTop:14}}>{inspected.length} of {evidence.length} findings inspected. Review evidence before deciding in the mission workspace.</p>
  </div>
 </section>;
}
