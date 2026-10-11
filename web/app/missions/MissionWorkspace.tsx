'use client';
import {useEffect,useState} from 'react';
import dynamic from 'next/dynamic';
const SocScene=dynamic(()=>import('./SocScene'),{ssr:false});
import styles from './workspace.module.css';
import Investigation from './Investigation';
import CorrelationBoard from './CorrelationBoard';

type Step={scene:string;story:string;evidence:string[];question:string;options:string[]};
type Run={run_id:number;mission_id:string;title:string;step_index:number;step_count:number;score:number;max_score:number;completed:boolean;step:Step|null;last_feedback:string|null};
type Props={run:Run;busy:boolean;onDecision:(option:number,finding:number)=>Promise<void>;onReplay:()=>void;onExit:()=>void};

export default function MissionWorkspace({run,busy,onDecision,onReplay,onExit}:Props){
  const [tab,setTab]=useState<'briefing'|'evidence'|'decision'>('briefing');
  const [show3D,setShow3D]=useState(false);
  const [inspected,setInspected]=useState<number[]>([]);
  const [selected,setSelected]=useState<number|null>(null);
  const [finding,setFinding]=useState<number|null>(null);
  const [notes,setNotes]=useState('');
  const [sending,setSending]=useState(false);
  const [feedback,setFeedback]=useState('');
  const [lastStep,setLastStep]=useState(-1);
  useEffect(()=>{
    if(lastStep!==run.step_index){
      setLastStep(run.step_index);
      setTab('briefing');setInspected([]);setSelected(null);setFinding(null);
      if(run.step_index>0)setFeedback(run.last_feedback||'');
    }
  },[run.step_index,run.last_feedback,lastStep]);
  const evidence=run.step?.evidence||[];
  const allInspected=evidence.length>0&&inspected.length===evidence.length;
  async function submit(){
    if(selected===null||finding===null||!allInspected||busy||sending)return;
    setSending(true);
    try{await onDecision(selected,finding);}finally{setSending(false);}
  }
  return <section className={styles.shell} aria-label="Simulated analyst workstation">
    <header className={styles.topbar}>
      <div><span className={styles.liveDot}/> EDUCYBER / TRAINING ENVIRONMENT <small> · FICTIONAL CASE</small></div>
      <button className={styles.exit} onClick={onExit}>Exit workstation</button>
    </header>
    <div className={styles.toolbar}>
      <div><span className={styles.eyebrow}>CASE #{String(run.run_id).padStart(4,'0')}</span>
        <h2>{run.title}</h2><p>{run.completed?'Case resolved':'Active investigation · '+(run.step?.scene||'')}</p></div>
      <div className={styles.stats}>
        <div><span>STAGE</span><strong>{Math.min(run.step_index+1,run.step_count)}/{run.step_count}</strong></div>
        <div><span>POINTS</span><strong>{run.score}<small>/{run.max_score}</small></strong></div>
      </div>
    </div>
    <div className={styles.progress}><div style={{width:(100*run.step_index/run.step_count)+'%'}}/></div>
    {!run.completed&&<div style={{padding:'0 20px'}}><button type="button" className={styles.ghost} style={{margin:'12px 0'}} aria-expanded={show3D} onClick={()=>setShow3D(v=>!v)}>{show3D?'Switch to 2D workstation':'Enter 3D investigation room'}</button>{show3D&&<SocScene key={run.run_id+'-'+run.step_index} stage={run.step_index} missionId={run.mission_id} missionTitle={run.title} active={tab} onSelect={setTab} evidence={evidence} inspected={inspected} onInspect={i=>setInspected(old=>old.includes(i)?old:[...old,i])}/>}</div>}
    {run.completed?<div className={styles.complete}>
      <div className={styles.completeIcon}>✓</div>
      <span className={styles.eyebrow}>AFTER-ACTION REPORT</span>
      <h3>Mission complete</h3>
      <p>You scored <strong>{run.score} out of {run.max_score}</strong> points ({Math.round(run.score/run.max_score*100)}%). Your result has been saved to your account.</p>
      {feedback&&<div className={styles.feedback}>{feedback}</div>}
      <button className={styles.primary} onClick={onReplay} disabled={busy}>Replay this mission</button>
      <button className={styles.ghost} onClick={onExit}>Return to mission board</button>
    </div>:<div className={styles.body}>
      <aside className={styles.sidebar}>
        <span className={styles.eyebrow}>WORKSPACE</span>
        {(['briefing','evidence','decision'] as const).map((t,i)=><button key={t}
          className={tab===t?styles.activeTab:styles.tab} onClick={()=>setTab(t)}>
          <span>{['◈','▤','◎'][i]}</span> {['Case briefing','Evidence locker','Decision desk'][i]}
          {t==='evidence'&&<small>{inspected.length}/{evidence.length}</small>}
        </button>)}
        <div className={styles.sidebarNote}><strong>Training mode</strong><p>No live networks, accounts or devices are involved.</p></div>
      </aside>
      <div className={styles.main}>
        {feedback&&<div className={styles.feedback} role="status"><strong>Previous decision</strong><p>{feedback}</p></div>}
        {tab==='briefing'&&<div>
          <span className={styles.eyebrow}>INTELLIGENCE BRIEF · STAGE {run.step_index+1}</span>
          <h3>{run.step?.scene}</h3>
          <p className={styles.story}>{run.step?.story}</p>
          <div className={styles.callout}><strong>Your assignment</strong><p>Review all available evidence, then choose the safest response.</p></div>
          <button className={styles.primary} onClick={()=>setTab('evidence')}>Open evidence locker →</button>
        </div>}
        {tab==='evidence'&&<div>
          <span className={styles.eyebrow}>EVIDENCE LOCKER</span>
          <h3>Review the case artifacts</h3>
          <p className={styles.subtle}>Select each artifact to inspect it. These are fictional training records.</p>
          <Investigation key={run.mission_id+'-'+run.step_index} missionId={run.mission_id}
            stage={run.step_index} evidence={evidence} inspected={inspected}
            onInspect={i=>setInspected(old=>old.includes(i)?old:[...old,i])}/>
          <CorrelationBoard key={run.run_id+'-'+run.step_index} evidence={evidence} inspected={inspected} stage={run.step_index}/>
          <fieldset style={{border:'1px solid #35516b',borderRadius:9,padding:14,marginTop:18}}>
            <legend style={{color:'#65dfc6',fontWeight:700}}>Investigation finding · 5 bonus points</legend>
            <p className={styles.subtle}>Which finding is the most important indicator at this stage? Select one for server grading.</p>
            {evidence.map((item,i)=><label key={i} style={{display:'block',padding:'8px 0',color:'#e0eef7'}}>
              <input type="radio" name={'finding-'+run.run_id+'-'+run.step_index}
                checked={finding===i} onChange={()=>setFinding(i)} disabled={!allInspected}/> {item}
            </label>)}
          </fieldset>
          <button className={styles.primary} disabled={!allInspected||finding===null} onClick={()=>setTab('decision')}>Proceed to decision desk →</button>
        </div>}
        {tab==='decision'&&<div>
          <span className={styles.eyebrow}>DECISION DESK</span>
          <h3>{run.step?.question}</h3>
          <p className={styles.subtle}>Choose one action. Your score is determined by the server.</p>
          <div className={styles.choices}>{run.step?.options.map((option,i)=><label key={i} className={selected===i?styles.chosen:styles.choice}>
            <input type="radio" name={'mission-'+run.run_id+'-'+run.step_index} checked={selected===i}
              onChange={()=>setSelected(i)} disabled={busy||sending}/>
            <span className={styles.choiceLetter}>{String.fromCharCode(65+i)}</span>{option}
          </label>)}</div>
          {!allInspected&&<p className={styles.warning}>Inspect every artifact in the evidence locker before submitting.</p>}
          <button className={styles.primary} disabled={!allInspected||selected===null||finding===null||busy||sending} onClick={submit}>
            {busy||sending?'Recording decision…':'Commit decision →'}
          </button>
        </div>}
      </div>
      <aside className={styles.notebook}>
        <span className={styles.eyebrow}>ANALYST NOTEBOOK</span>
        <p>Use this scratchpad to reason through the scenario.</p>
        <textarea aria-label="Analyst notes" value={notes} onChange={e=>setNotes(e.target.value)}
          placeholder="What do the clues suggest? What would you investigate next?" rows={10}/>
        <small>Scratchpad only · not submitted or saved to the server</small>
      </aside>
    </div>}
  </section>;
}
