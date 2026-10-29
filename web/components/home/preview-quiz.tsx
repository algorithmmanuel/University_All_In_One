'use client';
import { useState } from 'react';
import { previewQuestions } from '../../lib/preview-quiz';

/** Session-only practice: no learner data leaves the browser. */
export function PreviewQuiz() {
  const [index, setIndex] = useState(0);
  const [answer, setAnswer] = useState<number | null>(null);
  const [completed, setCompleted] = useState(0);
  const current = previewQuestions[index];
  function next() {
    if (answer === current.correct) setCompleted(n => n + 1);
    setAnswer(null);
    setIndex(n => (n + 1) % previewQuestions.length);
  }
  return <section id="mission" className="container section"><div className="tag">INTERACTIVE CYBERSECURITY</div><h2>Mission 01: Spot the risk</h2><p className="muted">A short digital-safety challenge. No registration required; your answers remain in this browser session.</p><div className="card" style={{maxWidth:780}}><span className="pill">Question {index+1} of {previewQuestions.length}</span><h3>{current.q}</h3><div className="quiz-options">{current.answers.map((option,i)=><button key={option} onClick={()=>setAnswer(i)} disabled={answer!==null} style={answer===i?{borderColor:answer===current.correct?'var(--success)':'var(--danger)',background:answer===current.correct?'var(--success-surface)':'var(--danger-surface)',color:answer===current.correct?'var(--text)':'var(--danger)'}:{}}>{option}</button>)}</div>{answer!==null&&<><p className="result" role="status">{answer===current.correct?'✓ Correct':'Not quite — review the explanation'}</p><p className="muted">{current.explanation}</p><button className="btn" onClick={next}>Next question →</button></>}<p className="small">Correct answers completed this session: {completed}</p></div></section>;
}
