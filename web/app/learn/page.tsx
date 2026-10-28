'use client';
import { useCallback, useEffect, useRef, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import LessonGuide, {type LearningGuide} from '../../components/lesson-guide';
import { useActivityFocus } from '../../lib/use-activity-focus';

const API = (process.env.NEXT_PUBLIC_API_BASE_URL || '').replace(/\/$/, '');
type Course = {id:number;academy_id:string;title:string;description:string;lesson_count:number};
type Enrollment = {id:number;academy_id:string;title:string;description:string;total_lessons:number;completed_lessons:number;progress_percent:number};
type Lesson = {id:number;title:string;content:string;position:number;completed:boolean;learning_guide?:LearningGuide|null};
type CourseDetail = {course:Course;lessons:Lesson[]};
const academies: Record<string,string> = {cyber:'Cybersecurity Academy',university:'University',secondary:'Secondary School'};

export default function Learn() {
  const router = useRouter();
  const [catalog,setCatalog]=useState<Course[]>([]);
  const [enrollments,setEnrollments]=useState<Enrollment[]>([]);
  const [selected,setSelected]=useState<CourseDetail|null>(null);
  const [busy,setBusy]=useState(false);
  const [error,setError]=useState('');
  const [loading,setLoading]=useState(true);
  const [hasLoaded,setHasLoaded]=useState(false);
  const [openSequence,setOpenSequence]=useState(0);
  const linkedLessonFocused=useRef(false);
  const activityHeading=useActivityFocus(openSequence);

  const request = useCallback(async (path:string, method='GET', data?:Record<string,unknown>) => {
    const token=sessionStorage.getItem('educyber_token');
    if (!token) {router.replace('/account');throw new Error('Please sign in');}
    const response=await fetch(API+path,{method,headers:{Authorization:'Bearer '+token,...(data?{'Content-Type':'application/json'}:{})},...(data?{body:JSON.stringify(data)}:{})});
    const body=await response.json();
    if (!response.ok) {
      if(response.status===401) {sessionStorage.removeItem('educyber_token');router.replace('/account');}
      throw new Error(typeof body.detail==='string'?body.detail:'Request failed');
    }
    return body;
  },[router]);

  const refresh = useCallback(async()=>{
    const [courses, mine] = await Promise.all([
      request('/api/v1/learning/catalog'),
      request('/api/v1/learning/enrollments')
    ]);
    setCatalog(courses.courses);setEnrollments(mine.enrollments);setHasLoaded(true);
  },[request]);

  useEffect(()=>{
    let active=true;
    refresh().catch(e=>{if(active)setError(e.message);}).finally(()=>{if(active)setLoading(false);});
    return ()=>{active=false;};
  },[refresh]);

  useEffect(()=>{
    if(loading)return;
    const id=Number(new URLSearchParams(window.location.search).get('course'));
    if(Number.isSafeInteger(id)&&enrollments.some(course=>course.id===id)){
      openCourse(id,false);
    }
    // Resolve the initial URL after enrolments load; ordinary refreshes must not reopen a closed course.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[loading]);

  useEffect(()=>{
    if(!selected||linkedLessonFocused.current)return;
    const target=selected.lessons.find(lesson=>window.location.hash===`#lesson-${lesson.id}`);
    if(!target)return;
    const heading=document.getElementById(`lesson-${target.id}`);
    linkedLessonFocused.current=true;
    heading?.scrollIntoView({behavior:'instant',block:'start'});
    heading?.focus({preventScroll:true});
  },[selected]);

  async function enroll(id:number){
    setBusy(true);setError('');
    try{await request('/api/v1/learning/enrollments/'+id,'POST');await refresh();await openCourse(id);}
    catch(e){setError(e instanceof Error?e.message:'Unable to enroll');}
    finally{setBusy(false);}
  }
  async function openCourse(id:number, moveToActivity=true){
    setBusy(true);setError('');
    try{
      const detail=await request('/api/v1/learning/courses/'+id+'/lessons');
      setSelected(detail);
      if(moveToActivity)setOpenSequence(value=>value+1);
    }
    catch(e){setError(e instanceof Error?e.message:'Unable to load lessons');}
    finally{setBusy(false);}
  }
  async function complete(id:number){
    if(!selected)return;
    setBusy(true);setError('');
    try{
      await request('/api/v1/learning/lessons/'+id+'/complete','POST');
      await openCourse(selected.course.id,false);
      await refresh();
    }catch(e){setError(e instanceof Error?e.message:'Unable to save progress');}
    finally{setBusy(false);}
  }

  return <main className="container section" style={{maxWidth:1100}}>
    <Link href="/dashboard">← Dashboard</Link>
    <h1>My learning</h1>
    <p className="muted">Explore published courses, enroll and track completed lessons. Your progress is saved to your account.</p>
    {error&&<div><p role="alert" className="status-error">{error}</p><button className="btn secondary" disabled={busy||loading} onClick={()=>{setError('');setLoading(true);refresh().catch(e=>setError(e.message)).finally(()=>setLoading(false));}}>Retry learning data</button></div>}
    {loading?<p role="status">Loading courses…</p>:!hasLoaded?null:<>
      <section>
        <h2>Enrolled courses</h2>
        {enrollments.length===0?<p className="muted">You have not enrolled in a course yet.</p>:<div className="grid">
          {enrollments.map(c=><article className="card" key={c.id}>
            <span className="small">{academies[c.academy_id]||c.academy_id}</span>
            <h3>{c.title}</h3>
            <p>{c.completed_lessons} of {c.total_lessons} lessons complete</p>
            <progress value={c.completed_lessons} max={Math.max(c.total_lessons,1)} style={{width:'100%'}} aria-label={c.title+' progress'}/>
            <p className="small">{c.progress_percent}% completed</p>
            <button className="btn" disabled={busy} onClick={()=>openCourse(c.id)}>Continue learning →</button>
          </article>)}
        </div>}
      </section>
      <section className="section">
        <h2>Course catalogue</h2>
        {catalog.length===0?<p className="muted">No published courses yet. Run the demonstration course seed command.</p>:<div className="grid">
          {catalog.map(c=><article className="card" key={c.id}>
            <span className="small">{academies[c.academy_id]||c.academy_id}</span>
            <h3>{c.title}</h3>
            <p className="muted">{c.description}</p>
            <p className="small">{c.lesson_count} lessons</p>
            {enrollments.some(e=>e.id===c.id)
              ?<button className="btn" disabled={busy} onClick={()=>openCourse(c.id)}>Open course</button>
              :<button className="btn" disabled={busy} onClick={()=>enroll(c.id)}>Enroll for free</button>}
          </article>)}
        </div>}
      </section>
      {selected&&<section className="section" id="course-lessons">
        <div className="panel">
          <button onClick={()=>setSelected(null)}>← Close lessons</button>
          <h2 ref={activityHeading} tabIndex={-1} className="activity-heading">{selected.course.title}</h2>
          {selected.lessons.length===0?<p>No lessons have been published yet.</p>:selected.lessons.map(l=>
            <article className="card" key={l.id} style={{marginTop:16}}>
              <span className="small">Lesson {l.position} {l.completed?'· Completed ✓':''}</span>
              <h3 id={`lesson-${l.id}`} tabIndex={-1}>{l.title}</h3>
              {l.learning_guide?<LessonGuide key={l.id+':'+l.learning_guide.revision} guide={l.learning_guide}
                checkAnswer={(exercise,option)=>request('/api/v1/learning/lessons/'+l.id+'/practice','POST',
                  {exercise_id:exercise,option_index:option})}/>
                :<p style={{whiteSpace:'pre-wrap',lineHeight:1.7}}>{l.content}</p>}
              <button className="btn" disabled={busy||l.completed} onClick={()=>complete(l.id)}>
                {l.completed?'Completed ✓':'Mark lesson complete'}
              </button>
            </article>)}
        </div>
      </section>}
    </>}
  </main>;
}

