'use client';
import {useRef,useState} from 'react';

export type LearningGuide = {
  revision: string;
  objectives: {id:string;text:string}[];
  sections: {title:string;body:string;code?:string;output?:string}[];
  exercises: {id:string;objective:string;prompt:string;code?:string;options:string[]}[];
};
type PracticeResult = {exercise_id:string;correct:boolean;explanation:string};

function CodeExample({code,label}:{code:string;label:string}) {
  return <pre aria-label={label} style={{overflowX:'auto',padding:16,border:'1px solid #64748b',borderRadius:8,maxWidth:'100%'}}>
    <code>{code}</code>
  </pre>;
}

/** Render text only. Practice feedback never becomes a persisted assessment grade. */
export default function LessonGuide({guide,checkAnswer}:{guide:LearningGuide;
  checkAnswer:(exercise:string,option:number)=>Promise<PracticeResult>}) {
  const [answers,setAnswers]=useState<Record<string,number>>({});
  const [results,setResults]=useState<Record<string,PracticeResult>>({});
  const [busy,setBusy]=useState<string|null>(null);
  const checking=useRef(false);
  const [error,setError]=useState('');

  async function check(exercise:string) {
    const option=answers[exercise];
    if(option===undefined || checking.current)return;
    checking.current=true;setBusy(exercise);setError('');
    try {
      const result=await checkAnswer(exercise,option);
      setResults(previous=>({...previous,[exercise]:result}));
    } catch(error) {
      setError(error instanceof Error?error.message:'Unable to check your answer. Try again.');
    } finally {checking.current=false;setBusy(null);}
  }

  return <div>
    <h4>What you will learn</h4>
    <ul>{guide.objectives.map(objective=><li key={objective.id}>{objective.text}</li>)}</ul>
    {guide.sections.map(section=><section key={section.title} style={{marginTop:24}}>
      <h4>{section.title}</h4>
      <p style={{lineHeight:1.8}}>{section.body}</p>
      {section.code&&<CodeExample code={section.code} label={section.title+' example'}/>}
      {section.output!==undefined&&<><p className="small">Expected output</p>
        <CodeExample code={section.output} label={section.title+' expected output'}/></>}
    </section>)}
    <section style={{marginTop:24}} aria-label="Guided practice">
      <h4>Try it before checking</h4>
      <p>Choose the safest next step or predict the result, then check your reasoning. These practice checks do not save a grade or mark the lesson complete.</p>
      {(guide.sections.some(section=>section.code)||guide.exercises.some(exercise=>exercise.code))&&<p className="small">Python examples are for reading and prediction; this lesson does not run code.</p>}
      {error&&<p role="alert">{error}</p>}
      {guide.exercises.map((exercise,index)=><form key={exercise.id}
        onSubmit={event=>{event.preventDefault();void check(exercise.id);}}
        style={{marginTop:20,padding:16,border:'1px solid #64748b',borderRadius:8}}>
        {/* Keep the active control focusable while awaiting feedback. The ref
            blocks repeat submissions and answer changes without dropping focus. */}
        <fieldset aria-busy={busy===exercise.id} style={{border:0,padding:0,minWidth:0}}>
          <legend>Practice {index+1}: {exercise.prompt}</legend>
          {exercise.code&&<CodeExample code={exercise.code} label={'Practice '+(index+1)+' code'}/>}
          {exercise.options.map((option,optionIndex)=><label key={optionIndex} style={{display:'block',padding:'10px 0'}}>
            <input type="radio" name={guide.revision+'-'+exercise.id} aria-disabled={Boolean(busy)} checked={answers[exercise.id]===optionIndex}
              onChange={()=>{
                if(checking.current)return;
                setAnswers(previous=>({...previous,[exercise.id]:optionIndex}));
                setResults(previous=>{const next={...previous};delete next[exercise.id];return next;});
              }}/>{' '}{option}
          </label>)}
          <button className="btn" type="submit" disabled={answers[exercise.id]===undefined} aria-disabled={Boolean(busy)}>
            {busy===exercise.id?'Checking…':'Check answer'}
          </button>
        </fieldset>
        <div role="status" aria-live="polite" style={{marginTop:12}}>
          {results[exercise.id]&&<p><strong>{results[exercise.id].correct?'Well reasoned.':'Try tracing it again.'}</strong>{' '}
            {results[exercise.id].explanation}</p>}
        </div>
      </form>)}
    </section>
  </div>;
}
