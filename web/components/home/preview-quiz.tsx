"use client";
import { useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { previewQuestions } from "../../lib/preview-quiz";
import { AUDIENCES, journeyUrl, type Audience } from "../../lib/learning-journey";

/** Optional, session-only diagnostic: never writes scores or awards mastery. */
export function PreviewQuiz() {
  const search = useSearchParams();
  const raw = search.get("pathway");
  const pathway: Audience = AUDIENCES.find(a => a.id === raw)?.id || "all";
  const [index, setIndex] = useState(0);
  const [selected, setSelected] = useState<number | null>(null);
  const [answers, setAnswers] = useState<number[]>([]);
  const done = answers.length === previewQuestions.length;
  const score = answers.filter((a, i) => a === previewQuestions[i].correct).length;
  const restart = () => { setIndex(0); setSelected(null); setAnswers([]); };
  const advance = () => {
    if (selected === null) return;
    setAnswers(previous => [...previous, selected]);
    setSelected(null);
    if (index < previewQuestions.length - 1) setIndex(i => i + 1);
  };
  const recommendedStage = score <= 3 ? "understand" : score <= 5 ? "check" : "investigate";
  return <section className="container section" aria-label="Optional cybersecurity preview" style={{maxWidth:850}}>
    <nav aria-label="Preview navigation"><Link href={journeyUrl("discover", pathway)}>← Back to my pathway</Link> · <Link href="/help">How EduCyber works</Link></nav>
    <div className="tag" style={{marginTop:24}}>SHARED OPTIONAL INTRODUCTION</div>
    <h1>Spot the risk: six-question preview</h1>
    <p className="muted">This is the same introductory activity for all pathways. No account is required and your answers are not sent to the server or saved as a learner score. You can choose any learning stage regardless of the result.</p>
    {!done ? <div className="card">
      <p className="pill">Question {index + 1} of {previewQuestions.length}</p>
      <progress aria-label="Questions answered" value={answers.length} max={previewQuestions.length} style={{width:"100%"}} />
      <h2>{previewQuestions[index].q}</h2>
      <div className="quiz-options">
        {previewQuestions[index].answers.map((option,i) => <button type="button" key={option}
          disabled={selected !== null} onClick={() => setSelected(i)}
          style={selected === i ? {borderColor:selected===previewQuestions[index].correct?"var(--success)":"var(--danger)"} : undefined}>{option}</button>)}
      </div>
      {selected !== null && <div aria-live="polite">
        <p className="result">{selected === previewQuestions[index].correct ? "Correct" : "Not quite"}</p>
        <p>{previewQuestions[index].explanation}</p>
        <button className="btn" type="button" onClick={advance}>{index === previewQuestions.length - 1 ? "See my results" : "Next question"} →</button>
      </div>}
    </div> : <div className="card" aria-live="polite">
      <span className="tag">PREVIEW COMPLETED</span>
      <h2>Your result: {score} of {previewQuestions.length}</h2>
      <p>{score <= 3 ? "Some foundational ideas deserve another look." : score <= 5 ? "You recognised many risks; practise and review the concepts you missed." : "Strong performance on this short introduction. Try a guided investigation if you wish."}</p>
      <p className="small">This suggestion is based on only six questions. It is not a placement decision, certification or prerequisite.</p>
      <h3>Review the explanations</h3>
      <ol>{previewQuestions.map((q,i) => <li key={q.q} style={{marginBottom:14}}><strong>{answers[i]===q.correct ? "Correct" : "Review"}:</strong> {q.q}<p className="muted">{q.explanation}</p></li>)}</ol>
      <div className="actions">
        <Link className="btn" href={journeyUrl(recommendedStage,pathway)}>Continue to my suggested stage →</Link>
        <Link className="btn secondary" href={journeyUrl("discover",pathway)}>Choose any stage</Link>
        <button className="btn secondary" type="button" onClick={restart}>Try again</button>
      </div>
    </div>}
  </section>;
}
