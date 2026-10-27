'use client';
import {useRef,useState} from 'react';
import styles from './workspace.module.css';

export type Artifact={title:string;body:string};
export type ReviewQuestion={id:string;prompt:string;options:string[]};
export type ReviewResult={question_id:string;correct:boolean;explanation:string};
export type MissionLearning={revision:string;role:string;objectives:string[];workflow:string[];completion:string;
  stage:null|{task:string;hints:string[];artifacts:Artifact[]};review:ReviewQuestion[]};

export function MissionBriefing({learning}:{learning:MissionLearning}){
  return <section aria-label="Mission instructions" className={styles.callout}>
    <h4>Your role and goals</h4><p>{learning.role}</p>
    <ul>{learning.objectives.map(text=><li key={text}>{text}</li>)}</ul>
    <h4>How to play</h4><ol>{learning.workflow.map(text=><li key={text}>{text}</li>)}</ol>
    <p><strong>Completion:</strong> {learning.completion}</p>
    <p>2D is the default lightweight mode. The optional 3D room opens the same evidence and workstations; walking is never required.</p>
    {learning.stage&&<><h4>This stage’s task</h4><p>{learning.stage.task}</p>
      <details><summary>Need a hint?</summary>
        <p>{learning.stage.hints[0]}</p>
        <details><summary>Show another hint</summary><p>{learning.stage.hints[1]}</p></details>
      </details></>}
  </section>;
}

export function MissionArtifacts({artifacts,inspected,onInspect}:{artifacts:Artifact[];inspected:number[];onInspect:(index:number)=>void}){
  const [active,setActive]=useState<number|null>(null);
  return <section aria-label="Scholarship case artifacts">
    <p className={styles.subtle}>Open each fictional record and read what it shows. Then choose the finding that best answers this stage’s task.</p>
    <div className={styles.artifacts}>{artifacts.map((item,index)=><button key={item.title} type="button"
      className={styles.artifact} aria-pressed={active===index}
      onClick={()=>{setActive(index);onInspect(index);}}>
      <span>{index+1}. {item.title}</span><small>{inspected.includes(index)?'Reviewed':'Open record'}</small>
    </button>)}</div>
    {active!==null&&<div className={styles.callout} role="status"><h4>{artifacts[active].title}</h4><p>{artifacts[active].body}</p></div>}
  </section>;
}

export function MissionReview({questions,check}:{questions:ReviewQuestion[];check:(question:string,option:number)=>Promise<ReviewResult>}){
  const [answers,setAnswers]=useState<Record<string,number>>({});
  const [results,setResults]=useState<Record<string,ReviewResult>>({});
  const [busy,setBusy]=useState<string|null>(null);
  const [error,setError]=useState('');
  const pending=useRef(false);
  async function submit(id:string){
    if(pending.current||answers[id]===undefined)return;
    pending.current=true;setBusy(id);setError('');
    try{const result=await check(id,answers[id]);setResults(old=>({...old,[id]:result}));}
    catch(error){setError(error instanceof Error?error.message:'Unable to check this answer. Try again.');}
    finally{pending.current=false;setBusy(null);}
  }
  return <section aria-label="Mission review" className={styles.review}>
    <h3>Check your understanding</h3>
    <p>Five optional review questions. Try an answer, read the explanation and try again. These checks do not save a grade or change your mission result. Responses reset when you leave this workspace.</p>
    <p role="status">{Object.values(results).filter(result=>result.correct).length} of {questions.length} currently answered correctly in this review.</p>
    {error&&<p role="alert">{error}</p>}
    {questions.map((question,index)=><form key={question.id} onSubmit={event=>{event.preventDefault();void submit(question.id);}}>
      <fieldset aria-busy={busy===question.id}>
        <legend>{index+1}. {question.prompt}</legend>
        {question.options.map((option,i)=><label key={i} className={styles.reviewOption}>
          <input type="radio" name={'review-'+question.id} checked={answers[question.id]===i} aria-disabled={Boolean(busy)}
            onChange={()=>{if(pending.current)return;setAnswers(old=>({...old,[question.id]:i}));setResults(old=>{const next={...old};delete next[question.id];return next;});}}/> {option}
        </label>)}
        <button className={styles.primary} disabled={answers[question.id]===undefined} aria-disabled={Boolean(busy)} type="submit">{busy===question.id?'Checking…':'Check review answer'}</button>
      </fieldset>
      <div role="status">{results[question.id]&&<p>{results[question.id].correct?'Correct. ':'Try again. '}{results[question.id].explanation}</p>}</div>
    </form>)}
  </section>;
}
