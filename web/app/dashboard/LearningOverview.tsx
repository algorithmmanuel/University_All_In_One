'use client';
import {useEffect,useState} from 'react';
import Link from 'next/link';

const API=(process.env.NEXT_PUBLIC_API_BASE_URL||'').replace(/\/$/,'');
type Overview={enrolled_count:number;completed_courses:number;
  courses:{id:number;title:string;total_lessons:number;completed_lessons:number;progress_percent:number;completed:boolean;next_lesson:{id:number;title:string}|null}[];
  recent_attempts:{id:number;course_id:number;course_title:string;score:number;total:number;percentage:number;submitted_at:string}[]};

export default function LearningOverview(){
  const [data,setData]=useState<Overview|null>(null);
  const [error,setError]=useState('');
  const [retry,setRetry]=useState(0);
  useEffect(()=>{
    const controller=new AbortController();
    setError('');
    fetch(API+'/api/v1/learning/overview',{headers:{Authorization:'Bearer '+sessionStorage.getItem('educyber_token')},signal:controller.signal})
      .then(async response=>{if(!response.ok)throw new Error('Unable to load saved progress. Please try again.');return response.json();})
      .then(value=>{if(!controller.signal.aborted)setData(value);})
      .catch(error=>{if(!controller.signal.aborted)setError(error.message);});
    return ()=>controller.abort();
  },[retry]);
  return <section className="learning-overview" aria-labelledby="saved-progress-heading">
    <h2 id="saved-progress-heading">Your saved progress</h2>
    {error?<><p role="alert">{error}</p><button type="button" className="btn" onClick={()=>setRetry(value=>value+1)}>Retry saved progress</button></>:
      !data?<p role="status">Loading saved progress…</p>:<>
        <p>{data.enrolled_count} enrolled course(s) · {data.completed_courses} completed</p>
        <p className="small">Lesson completion records activity, not proof of mastery. Recent assessment scores describe individual attempts.</p>
        {data.courses.length===0?<p>No enrolled courses yet. <Link href="/learn">Choose your first course</Link>.</p>:
          <div className="grid">{data.courses.map(course=><article className="card" key={course.id}>
            <h3>{course.title}</h3><p>{course.completed_lessons} of {course.total_lessons} lessons complete</p>
            <progress aria-label={course.title+' lesson completion'} value={course.completed_lessons} max={Math.max(1,course.total_lessons)} style={{width:'100%'}}/>
            <p>{course.progress_percent}% completed</p>
            {course.next_lesson?<><p>Next lesson: {course.next_lesson.title}</p><Link href={`/learn?course=${course.id}#lesson-${course.next_lesson.id}`}>Continue {course.title}</Link></>:
              course.completed?<><p>All current lessons complete.</p><Link href={`/assessments?course=${course.id}`}>Practise {course.title}</Link></>:
              <p>Lessons have not been published yet.</p>}
          </article>)}</div>}
        <p><Link href="/learn">View all learning progress →</Link></p>
        <h3>Recent assessment attempts</h3>
        {data.recent_attempts.length===0?<p>No saved assessment attempts yet. <Link href="/assessments">Choose an assessment</Link>.</p>:
          <ul>{data.recent_attempts.map(attempt=><li key={attempt.id}>
            <Link href={`/assessments?course=${attempt.course_id}&attempt=${attempt.id}`}>{attempt.course_title}: {attempt.score}/{attempt.total} ({attempt.percentage}%)</Link>
            {' · '}{new Date(attempt.submitted_at).toLocaleString()}
          </li>)}</ul>}
        <p className="small">Showing up to three courses and three recent attempts. Compare question counts as well as percentages.</p>
      </>}
  </section>;
}
