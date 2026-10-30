import Link from 'next/link';

export type Analysis={version:number;curriculum_revision:string|null;evidence_note:string;unmapped_count:number;
  topics:{objective_id:string;objective:string;lesson_id:number;lesson_title:string;correct:number;total:number;
    percentage:number|null;status:string;recommendation:string}[];
  feedback:{question_id:number;prompt:string;options:string[];correct_index:number;selected_index:number;
    correct:boolean;explanation:string;objective_id:string|null}[]};
const labels:Record<string,string>={not_assessed:'Not assessed',limited_evidence:'Limited evidence',
  strength_in_this_attempt:'Strength in this attempt',revisit:'Revisit this objective'};

export default function AssessmentEvidence({analysis,courseId}:{analysis:Analysis|null;courseId:number}){
  if(!analysis)return <p>Topic evidence is unavailable for this historical attempt. Your saved score is unchanged. Take a new assessment for topic feedback.</p>;
  return <section aria-label="Topic results and next steps">
    <h2>Topic results and next steps</h2>
    <p className="muted">{analysis.evidence_note}</p>
    <p className="small">Practice guide: at least two questions and 80% correct indicates a strength in this attempt; fewer than two gives limited evidence. These labels are not a mastery assessment.</p>
    {analysis.unmapped_count>0&&<p>{analysis.unmapped_count} question(s) have no distinct reviewed objective mapping. They count towards your score, but provide no topic evidence.</p>}
    {analysis.topics.length===0&&<p>No reviewed topic mapping is available for this attempt.</p>}
    <div className="grid">{analysis.topics.map(topic=><article className="card" key={topic.objective_id}>
      <h3>{topic.objective}</h3><p><strong>{labels[topic.status]||'Evidence unavailable'}</strong></p>
      <p>{topic.total?`${topic.correct}/${topic.total} correct (${topic.percentage}%)`:'No questions sampled'}</p>
      <p>{topic.recommendation}</p>
      <Link href={`/learn?course=${courseId}#lesson-${topic.lesson_id}`}>Review: {topic.lesson_title}</Link>
    </article>)}</div>
    <details style={{marginTop:20}}><summary>Review answers and explanations</summary>
      {analysis.feedback.map(item=><article className="card" key={item.question_id} style={{marginTop:12}}>
        <h3>{item.prompt}</h3><p>{item.correct?'Correct':'Revisit this answer'}</p>
        <p>Your answer: {item.options[item.selected_index]}</p><p>Correct answer: {item.options[item.correct_index]}</p>
        <p>{item.explanation}</p>
      </article>)}
    </details>
  </section>;
}
