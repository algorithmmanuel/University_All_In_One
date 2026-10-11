'use client';
import {useState} from 'react';
import styles from './investigation.module.css';

type Props={missionId:string;stage:number;evidence:string[];inspected:number[];onInspect:(index:number)=>void};
const THEMES:Record<string,{tool:string;context:string;artifact:string}> = {
  'privacy-patrol':{tool:'Privacy settings simulator',context:'Review what a fictional profile reveals before making a privacy decision.',artifact:'Profile disclosure'},
  'scam-spotter':{tool:'Fraud signals desk',context:'Compare suspicious claims with the available fictional warning signs.',artifact:'Fraud signal'},
  'safe-social':{tool:'Social safety centre',context:'Review a fictional online interaction and choose a supportive response.',artifact:'Safety indicator'},
  'device-defender':{tool:'Device health console',context:'Assess fictional device warnings and security settings.',artifact:'Device finding'},
  'wifi-wise':{tool:'Connection inspector',context:'Check a simulated connection before trusting a website or network.',artifact:'Network indicator'},
  'digital-footprints':{tool:'Digital footprint explorer',context:'Inspect what a fictional public post could reveal.',artifact:'Public trace'},
  'mfa-guardian':{tool:'Sign-in protection desk',context:'Examine fictional authentication prompts and recovery choices.',artifact:'Account indicator'},
  'backup-buddy':{tool:'Recovery readiness lab',context:'Review fictional backup and recovery evidence.',artifact:'Recovery indicator'},
};
export default function ExplorerInvestigation({missionId,stage,evidence,inspected,onInspect}:Props){
  const [active,setActive]=useState<number|null>(null);
  const theme=THEMES[missionId] ?? {tool:'Case inspector',context:'Review simulated case evidence.',artifact:'Artifact'};
  return <section className={styles.lab} aria-label={theme.tool}>
    <div className={styles.labHeader}><span>SIMULATED TOOL / {theme.tool.toUpperCase()}</span><span>READ-ONLY · FICTIONAL</span></div>
    <div style={{padding:18}}>
      <h4 style={{margin:'0 0 8px'}}>{theme.tool} · Stage {stage+1}</h4>
      <p className={styles.hint}>{theme.context} Select an artifact to reveal its contents and record it as inspected.</p>
      <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(190px,1fr))',gap:12,marginTop:18}}>
        {evidence.map((item,i)=><button key={i} type="button" onClick={()=>{setActive(i);onInspect(i);}}
          aria-pressed={active===i} style={{textAlign:'left',padding:16,borderRadius:12,border:'1px solid '+(active===i?'#37d4b3':'#49677d'),background:active===i?'#173f47':'#10283d',color:'#e6f4fa',cursor:'pointer'}}>
          <span style={{fontSize:12,display:'block',color:'#a6cbd7'}}>{theme.artifact} {i+1}</span>
          <strong>{inspected.includes(i)?'✓ Reviewed':'◈ Inspect artifact'}</strong>
        </button>)}
      </div>
      {active!==null&&evidence[active]&&<div role="status" style={{padding:18,marginTop:14,borderRadius:12,border:'1px solid #386d77',background:'#112f42',color:'#e6f4fa'}}>
        <strong>{theme.artifact} {active+1}</strong><p>{evidence[active]}</p>
        <small>This training artifact is fictional. No live accounts or systems are connected.</small>
      </div>}
      <p className={styles.hint} style={{marginTop:16}}>{inspected.length} of {evidence.length} artifacts inspected. Review all artifacts before choosing your finding.</p>
    </div>
  </section>;
}
