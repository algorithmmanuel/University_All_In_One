'use client';
import { useCallback, useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

const API=(process.env.NEXT_PUBLIC_API_BASE_URL||'').replace(/\/$/,'');
type Course={id:number;title:string;academy_id:string};
type Question={id:number;prompt:string;options:string[]};
type Attempt={id:number;score:number;total:number;percentage:number;submitted_at:string};
type Feedback={question_id:number;correct_index:number;selected_index:number;correct:boolean;explanation:string};
type Result={score:number;total:number;percentage:number;feedback:Feedback[]};

export default function Assessments(){
  const router=useRouter();
  const [courses,setCourses]=useState<Course[]>([]);
  const [courseId,setCourseId]=useState<number|null>(null);
  const [questions,setQuestions]=useState<Question[]>([]);
  const [answers,setAnswers]=useState<Record<number,number>>({});
  const [attempts,setAttempts]=useState<Attempt[]>([]);
  const [result,setResult]=useState<Result|null>(null);
  const [error,setError]=useState('');
  const [busy,setBusy]=useState(false);

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
    setBusy(true);setError('');setResult(null);setAnswers({});setCourseId(id);
    try{
      const [q,a]=await Promise.all([request('/api/v1/quizzes/courses/'+id),
        request('/api/v1/quizzes/courses/'+id+'/attempts')]);
      setQuestions(q.questions);setAttempts(a.attempts);
    }catch(e){setError(e instanceof Error?e.message:'Unable to load quiz');}
    finally{setBusy(false);}
  }

  async function submit(event:React.FormEvent){
    event.preventDefault();
    if(courseId===null||questions.some(q=>answers[q.id]===undefined))return;
    setBusy(true);setError('');
    try{
      const data=await request('/api/v1/quizzes/courses/'+courseId+'/submit','POST',{answers});
      setResult(data);
      const history=await request('/api/v1/quizzes/courses/'+courseId+'/attempts');
      setAttempts(history.attempts);
    }catch(e){setError(e instanceof Error?e.message:'Unable to submit quiz');}
    finally{setBusy(false);}
  }

  return <main className="container section" style={{maxWidth:900}}>
    <Link href="/dashboard">← Dashboard</Link>
    <h1>Assessments & cyber missions</h1>
    <p className="muted">Practise with demonstration quizzes. Answers are graded by the server and attempts are saved to your account.</p>
    {error&&<p role="alert" style={{color:'#b42318'}}>{error}</p>}
    <section className="card">
      <h2>Choose an enrolled course</h2>
      {courses.length===0?<p>Enroll in a course first at <Link href="/learn">My learning</Link>.</p>:
        <div style={{display:'flex',gap:10,flexWrap:'wrap'}}>
          {courses.map(c=><button className="btn" key={c.id} disabled={busy}
            onClick={()=>choose(c.id)} aria-pressed={courseId===c.id}>{c.title}</button>)}
        </div>}
    </section>
    {courseId!==null&&<section className="section">
      <h2>Course assessment</h2>
      {questions.length===0?<p className="muted">No questions available for this course yet.</p>:
        <form onSubmit={submit}>
          {questions.map((q,index)=><fieldset className="card" key={q.id} style={{marginBottom:18,border:'1px solid #dce4ec'}}>
            <legend style={{fontWeight:700}}>Question {index+1}</legend>
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
            <p>Your result has been saved.</p></div>
            <button type="button" className="btn" onClick={()=>choose(courseId)} disabled={busy}>Try again</button></>}
        </form>}
      <h2 style={{marginTop:32}}>Previous attempts</h2>
      {attempts.length===0?<p className="muted">No attempts yet.</p>:<ul>
        {attempts.map(a=><li key={a.id}>{new Date(a.submitted_at).toLocaleString()} — {a.score}/{a.total} ({a.percentage}%)</li>)}
      </ul>}
    </section>}
  </main>;
}
