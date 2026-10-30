import Link from "next/link";
import { AUDIENCES, STAGES } from "../../lib/learning-journey";
export default function HelpPage(){return <main className="container section" style={{maxWidth:950}}>
<nav><Link href="/">Home</Link> · <Link href="/journey">Learning journey</Link></nav>
<span className="tag">START HERE</span><h1>How EduCyber works</h1>
<p>Choose a learning pathway for recommendations, then choose any of the eight stages. These are recommendations, not locked levels. You can move between pathways and stages at any time.</p>
<h2>Choose your pathway</h2><div className="grid">{AUDIENCES.map(a=><article className="card" key={a.id}><h3>{a.title}</h3><p>{a.description}</p><Link href={"/journey?stage=discover&pathway="+a.id}>Explore this pathway</Link></article>)}</div>
<h2>The eight learning stages</h2><ol>{STAGES.map(s=><li key={s.id}><strong>{s.title}:</strong> {s.description}</li>)}</ol>
<h2>What are the activities?</h2>
<p><strong>Six-question preview:</strong> optional public introduction, with explanations and a non-binding suggested next stage. No saved score.</p>
<p><strong>Foundation courses:</strong> lessons for understanding concepts; enrollment and saved progress require a learner account.</p>
<p><strong>Knowledge checks:</strong> assessments and practice questions to identify topics to revisit.</p>
<p><strong>Guided missions and games:</strong> fictional investigations, evidence and decisions; the 2D and 3D modes are alternate views of a mission.</p>
<p><strong>Decision Workshop:</strong> a guided, saved case within a stage. Consider a situation, choose an action, see the consequence and reflect. It is not the same as the Red/Blue simulator.</p>
<p><strong>Cyber Lab:</strong> applied teaching, topic practice and decision-based defender simulations.</p>
<p><strong>Red/Blue:</strong> a separate strategy simulator against a computer or another eligible learner. You choose a seat and scenario before starting.</p>
<h2>Sign-in and progress</h2><p>The introductory preview works without an account. Enrolled courses, saved workshops and gameplay generally require an eligible learner account. Opening navigation links never automatically enrolls you, creates a game or awards progress.</p>
<div className="actions"><Link className="btn" href="/journey">Choose my pathway →</Link><Link className="btn secondary" href="/preview">Try the public preview</Link></div>
</main>}
