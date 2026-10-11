'use client';
import {useState} from 'react';
import styles from './investigation.module.css';
import ExplorerInvestigation from './ExplorerInvestigation';
import AcademyInvestigation from './AcademyInvestigation';
import CommandInvestigation from './CommandInvestigation';

type Props={missionId:string;stage:number;onInspect:(index:number)=>void;inspected:number[];evidence:string[]};
type Mail={from:string;subject:string;preview:string;body:string;link?:string};
const mails:Mail[]=[
 {from:'awards@scholarships-example.invalid',subject:'URGENT: Scholarship award confirmation',preview:'Confirm your student account before the deadline.',body:'Congratulations! Your scholarship has been approved. Confirm your student portal credentials within 20 minutes to claim the award.',link:'https://student-grants-example.invalid/verify'},
 {from:'registrar@university-example.invalid',subject:'Academic calendar update',preview:'The next semester calendar is available.',body:'The academic calendar has been updated. Check the official student portal for details.'},
 {from:'library@university-example.invalid',subject:'Library opening hours',preview:'New weekend opening hours.',body:'The university library will open on Saturdays this semester.'}
];
const logs=[
 {time:'00:39:02',account:'admin.ops',ip:'198.51.100.24',event:'LOGIN_FAILURE',severity:'Medium'},
 {time:'00:40:11',account:'admin.ops',ip:'198.51.100.24',event:'LOGIN_FAILURE',severity:'Medium'},
 {time:'00:42:07',account:'admin.ops',ip:'198.51.100.24',event:'LOGIN_SUCCESS',severity:'High'},
 {time:'00:43:19',account:'admin.ops',ip:'198.51.100.24',event:'PRIVILEGED_ACTION',severity:'Critical'},
 {time:'00:41:09',account:'staff.user',ip:'192.0.2.17',event:'LOGIN_SUCCESS',severity:'Low'}
];
const systems=[
 {name:'BR-WS-014',status:'Encrypted',role:'Branch workstation',time:'09:14'},
 {name:'BR-WS-019',status:'Suspicious',role:'Branch workstation',time:'09:21'},
 {name:'BR-FILE-01',status:'Investigating',role:'File server',time:'09:26'},
 {name:'BACKUP-OFFLINE',status:'Verified',role:'Offline recovery copy',time:'09:40'}
];
export default function Investigation({missionId,stage,onInspect,inspected,evidence}:Props){
 const [mail,setMail]=useState(0);
 const [search,setSearch]=useState('');
 const [severity,setSeverity]=useState('All');
 const [system,setSystem]=useState(0);
 const mark=(i:number)=>onInspect(i);
 if (['risk-command','zero-trust-briefing','cloud-incident','supply-chain-watch','ransomware-recovery','identity-crisis','boardroom-breach','ai-governance','audit-trail'].includes(missionId)) {
  return <CommandInvestigation key={missionId+'-'+stage} missionId={missionId} stage={stage} evidence={evidence} inspected={inspected} onInspect={onInspect}/>;
 }
 if (['network-watch','web-defense','cloud-perimeter','forensics-desk','malware-clues','identity-lab','secure-code-review','threat-hunter'].includes(missionId)) {
  return <AcademyInvestigation key={missionId+'-'+stage} missionId={missionId} stage={stage} evidence={evidence} inspected={inspected} onInspect={onInspect}/>;
 }
 if (['privacy-patrol','scam-spotter','safe-social','device-defender','wifi-wise','digital-footprints','mfa-guardian','backup-buddy'].includes(missionId)) {
  return <ExplorerInvestigation key={missionId+'-'+stage} missionId={missionId} stage={stage} evidence={evidence} inspected={inspected} onInspect={onInspect}/>;
 }
 return <div className={styles.lab}>
  <div className={styles.labHeader}><span>SIMULATED TOOL / {missionId==='phishing-investigation'?'MAIL CLIENT':missionId==='soc-alert-triage'?'SECURITY EVENT CONSOLE':'INCIDENT DASHBOARD'}</span><span>READ-ONLY TRAINING DATA</span></div>
  {missionId==='phishing-investigation'?<div className={styles.mailLayout}>
   <div className={styles.mailList}><strong>Inbox · 3 messages</strong>{mails.map((m,i)=><button key={i} className={mail===i?styles.selected:styles.mailRow} onClick={()=>setMail(i)}>
     <strong>{m.from}</strong><span>{m.subject}</span><small>{m.preview}</small></button>)}</div>
   <div className={styles.mailDetail}><span className={styles.label}>MESSAGE INSPECTOR</span><h4>{mails[mail].subject}</h4>
    <p><strong>From:</strong> {mails[mail].from}</p><p>{mails[mail].body}</p>
    {mails[mail].link&&<p className={styles.linkPreview}>Link preview (not clickable): {mails[mail].link}</p>}
    <p className={styles.hint}>Inspect sender, urgency and requested action. All domains are fictional.</p>
   </div>
  </div>:missionId==='soc-alert-triage'?<div className={styles.console}>
    <div className={styles.filters}><input aria-label="Search event logs" placeholder="Search account, IP or event…" value={search} onChange={e=>setSearch(e.target.value)}/>
    <select aria-label="Filter severity" value={severity} onChange={e=>setSeverity(e.target.value)}>
    {['All','Low','Medium','High','Critical'].map(s=><option key={s}>{s}</option>)}</select></div>
    <div className={styles.tableWrap}><table><thead><tr><th>TIME</th><th>ACCOUNT</th><th>SOURCE IP</th><th>EVENT</th><th>SEVERITY</th></tr></thead>
    <tbody>{logs.filter(l=>(severity==='All'||l.severity===severity)&&Object.values(l).join(' ').toLowerCase().includes(search.toLowerCase())).map((l,i)=>
      <tr key={i}><td>{l.time}</td><td>{l.account}</td><td>{l.ip}</td><td>{l.event}</td><td><span className={styles.severity}>{l.severity}</span></td></tr>)}</tbody></table></div>
    <p className={styles.hint}>Training IPs use reserved documentation ranges. Filtering does not affect mission scores.</p>
   </div>:<div className={styles.incident}>
     <div className={styles.systems}>{systems.map((s,i)=><button key={s.name} className={system===i?styles.selectedSystem:styles.system} onClick={()=>setSystem(i)}>
      <span className={styles.systemIcon}>▣</span><strong>{s.name}</strong><small>{s.status}</small></button>)}</div>
     <div className={styles.systemDetail}><span className={styles.label}>ASSET INSPECTOR</span><h4>{systems[system].name}</h4>
      <p>Role: {systems[system].role}</p><p>Status: <strong>{systems[system].status}</strong></p><p>Last observation: {systems[system].time}</p>
      <h4>Incident timeline</h4>{systems.map(s=><p key={s.name} className={styles.timeline}><strong>{s.time}</strong> · {s.name} — {s.status}</p>)}
     </div>
   </div>}
   <div className={styles.findings}><span className={styles.label}>CASE EVIDENCE · STAGE {stage+1}</span>
    <p className={styles.hint}>Use the tool above to investigate, then record each case finding below.</p>
    {evidence.map((item,i)=><button key={i} className={inspected.includes(i)?styles.findingDone:styles.finding} onClick={()=>mark(i)}>
      <span>{inspected.includes(i)?'✓':'○'}</span><span>{inspected.includes(i)?item:'Record finding '+(i+1)}</span></button>)}
    <p className={styles.hint}>{inspected.length}/{evidence.length} findings recorded</p>
   </div>
 </div>;
}
