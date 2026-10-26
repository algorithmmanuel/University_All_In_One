'use client';
import { useCallback, useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useActivityFocus } from '../../lib/use-activity-focus';

const API=(process.env.NEXT_PUBLIC_API_BASE_URL||'').replace(/\/$/,'');
type Course={id:number;title:string;academy_id:string};
type Question={id:number;prompt:string;options:string[]};
type Attempt={id:number;score:number;total:number;percentage:number;submitted_at:string};
type Feedback={question_id:number;correct_index:number;selected_index:number;correct:boolean;explanation:string};
type Result={score:number;total:number;percentage:number;feedback:Feedback[]};
type Preset='quick'|'standard'|'extended'|'custom';
const PRESETS=[{id:'quick',label:'Quick',count:5},{id:'standard',label:'Standard',count:10},
  {id:'extended',label:'Extended',count:20}] as const;

export default function Assessments(){
  const router=useRouter();
  const [courses,setCourses]=useState<Course[]>([]);
  const [courseId,setCourseId]=useState<number|null>(null);
  const [available,setAvailable]=useState(0);
  const [preset,setPreset]=useState<Preset>('standard');
  const [count,setCount]=useState('10');
  const [activeCount,setActiveCount]=useState(0);
  const [questions,setQuestions]=useState<Question[]>([]);
  const [answers,setAnswers]=useState<Record<number,number>>({});
  const [attempts,setAttempts]=useState<Attempt[]>([]);
  const [result,setResult]=useState<Result|null>(null);
  const [error,setError]=useState('');
  const [busy,setBusy]=useState(false);
  const [openSequence,setOpenSequence]=useState(0);
  const activityHeading=useActivityFocus(openSequence);
  const desiredCount=Number(count);
  const validCount=count.trim()!==''&&Number.isInteger(desiredCount)&&desiredCount>=1&&desiredCount<=available;

  const request=useCallback(async(path:string,method='GET',body?:object)=>{
    const token=sessionStorage.getItem('educyber_token');
    if(!token){router.replace('/account');throw new Error('Sign in first');}
    const response=await fetch(API+path,{method,headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},
      ...(body?{body:JSON.stringify(body)}:{})});
    const data=await response.json();
    if(!response.ok){
      if(response.status===401){sessionStorage.removeItem('educyber_token');router.replace('/account');}
      throw new Error(typeof data.detail==='string'?data.detail:'Request failed');
    }
    return data;
  },[router]);

  useEffect(()=>{
    request('/api/v1/learning/enrollments').then(d=>setCourses(d.enrollments)).catch(e=>setError(e.message));
  },[request]);

  async function choose(id:number){
    setBusy(true);setError('');setResult(null);setAnswers({});setQuestions([]);
    setAvailable(0);setAttempts([]);setCourseId(id);setActiveCount(0);
    try{
      const [options,history]=await Promise.all([
        request('/api/v1/quizzes/courses/'+id+'/options'),
        request('/api/v1/quizzes/courses/'+id+'/attempts')]);
      setAvailable(options.available_count);
      setCount(String(Math.min(10,options.available_count)));
      setPreset(options.available_count>=10?'standard':'custom');
      setAttempts(history.attempts);
      setOpenSequence(value=>value+1);
    }catch(e){setError(e instanceof Error?e.message:'Unable to load assessment options');}
    finally{setBusy(false);}
  }

  async function begin(){
    if(courseId===null||!validCount||busy)return;
    setBusy(true);setError('');
    try{
      const data=await request('/api/v1/quizzes/courses/'+courseId+'?question_count='+desiredCount);
      if(!Array.isArray(data.questions)||data.questions.length!==desiredCount)throw new Error('Assessment length changed. Please choose the course again.');
      setQuestions(data.questions);setActiveCount(desiredCount);setAnswers({});setResult(null);
      setOpenSequence(value=>value+1);
    }catch(e){setError(e instanceof Error?e.message:'Unable to start assessment');}
    finally{setBusy(false);}
  }

  async function submit(event:React.FormEvent){
    event.preventDefault();
    if(busy||courseId===null||questions.length===0||questions.some(q=>answers[q.id]===undefined))return;
    setBusy(true);setError('');
    try{
      const data=await request('/api/v1/quizzes/courses/'+courseId+'/submit','POST',
        {answers,question_count:activeCount});
      setResult(data);
      const history=await request('/api/v1/quizzes/courses/'+courseId+'/attempts');
      setAttempts(history.attempts);
    }catch(e){setError(e instanceof Error?e.message:'Unable to submit assessment');}
    finally{setBusy(false);}
  }

  return <main className="container section" style={{maxWidth:900}}>
    <Link href="/dashboard">← Dashboard</Link>
    <h1>Assessments & cyber missions</h1>
    <p className="muted">Choose a practice length that suits your time. The server grades your answers and saves the number of questions with your score.</p>
    {error&&<p role="alert" style={{color:'#b42318'}}>{error}</p>}
    <section className="card">
      <h2>Choose an enrolled course</h2>
      {courses.length===0?<p>Enroll in a course first at <Link href="/learn">My learning</Link>.</p>:
        <div style={{display:'flex',gap:10,flexWrap:'wrap'}}>
          {courses.map(c=><button className="btn" key={c.id} disabled={busy}
            onClick={()=>choose(c.id)} aria-pressed={courseId===c.id}>{c.title}</button>)}
        </div>}
    </section>
    {courseId!==null&&<section className="section" aria-labelledby="assessment-heading">
      <h2 id="assessment-heading" ref={activityHeading} tabIndex={-1} className="activity-heading">
        {questions.length>0?'Course assessment':'Choose your assessment length'}
      </h2>
      {questions.length===0?
        available===0?<p role="status" className="muted">{busy?'Loading assessment options…':'No questions available for this course yet.'}</p>:
        <div className="card">
          <p>{available} unique questions available. Choose between 1 and {available} questions.</p>
          <fieldset style={{border:0,padding:0}}>
            <legend>Test length</legend>
            <div style={{display:'flex',gap:16,flexWrap:'wrap',margin:'16px 0'}}>
              {PRESETS.map(option=><label key={option.id}>
                <input type="radio" name="test-length" value={option.id}
                  checked={preset===option.id} disabled={busy||available<option.count}
                  onChange={()=>{setPreset(option.id);setCount(String(option.count));}}/>
                {' '}{option.label} ({option.count} questions)
              </label>)}
              <label><input type="radio" name="test-length" value="custom" checked={preset==='custom'}
                disabled={busy} onChange={()=>setPreset('custom')}/> Custom</label>
            </div>
            {preset==='custom'&&<label>Number of questions
              <input type="number" min={1} max={available} step={1} value={count} disabled={busy}
                aria-describedby="assessment-length-help"
                onChange={event=>setCount(event.target.value)} style={{display:'block',padding:10,marginTop:8}}/>
            </label>}
          </fieldset>
          <p id="assessment-length-help" className="muted">
            {validCount?`Estimated time: about ${desiredCount} minute${desiredCount===1?'':'s'}. This is an estimate, not a timer.`:
              `Enter a whole number from 1 to ${available}.`}
          </p>
          <button type="button" className="btn" disabled={busy||!validCount} onClick={begin}>
            {busy?'Loading…':validCount?`Start ${desiredCount}-question assessment`:'Start assessment'}
          </button>
        </div>:
        <form onSubmit={submit}>
          <p>{activeCount} questions · {Object.keys(answers).length} answered</p>
          {questions.map((q,index)=><fieldset className="card" key={q.id} style={{marginBottom:18,border:'1px solid #dce4ec'}}>
            <legend style={{fontWeight:700}}>Question {index+1} of {activeCount}</legend>
            <p>{q.prompt}</p>
            {q.options.map((option,i)=><label key={i} style={{display:'block',padding:10}}>
              <input type="radio" name={'q'+q.id} checked={answers[q.id]===i} disabled={!!result||busy}
                onChange={()=>setAnswers(prev=>({...prev,[q.id]:i}))}/> {option}
            </label>)}
            {result&&(()=>{
              const feedback=result.feedback.find(f=>f.question_id===q.id);
              return feedback?<p role="status" style={{color:feedback.correct?'#087443':'#a52626'}}>
                {feedback.correct?'Correct':'Incorrect'} — Correct answer: {q.options[feedback.correct_index]}. {feedback.explanation}
              </p>:null;
            })()}
          </fieldset>)}
          {!result?<button className="btn" disabled={busy||questions.some(q=>answers[q.id]===undefined)}>
            {busy?'Submitting…':'Submit assessment'}
          </button>:<><div className="panel" role="status"><h2>Score: {result.score}/{result.total} ({result.percentage}%)</h2>
            <p>Saved as a {result.total}-question practice attempt.</p>
            <p className="muted">Shorter tests provide a smaller sample of your knowledge. Compare the question count as well as the percentage.</p></div>
            <button type="button" className="btn" onClick={()=>choose(courseId)} disabled={busy}>Choose another test length</button></>}
        </form>}
      <h2 style={{marginTop:32}}>Previous attempts</h2>
      {attempts.length===0?<p className="muted">No attempts yet.</p>:<ul>
        {attempts.map(a=><li key={a.id}>{new Date(a.submitted_at).toLocaleString()} — {a.total} questions · {a.score}/{a.total} ({a.percentage}%)</li>)}
      </ul>}
    </section>}
  </main>;
}

