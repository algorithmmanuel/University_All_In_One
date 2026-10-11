import type { AcademyCard, AcademyId } from '../../lib/pathways';

/** Both pathway sections share the same selected academy. */
export function AcademySections({ academies, selectedId, onSelect }: { academies: AcademyCard[]; selectedId: AcademyId; onSelect: (id: AcademyId) => void }) {
  const selected = academies.find(a => a.id === selectedId) ?? academies[0];
  if (!selected) return null;
  return <><section id="academies" className="container section"><div className="tag">THREE LEARNING PATHWAYS</div><h2>Choose your cyber pathway</h2><p className="muted">Different learning journeys, one connected platform.</p><div className="grid">{academies.map(a=><article className="card" key={a.id}><div className="icon" aria-hidden="true">{a.icon}</div><h3>{a.title}</h3><p className="muted">{a.description}</p><ul>{a.topics.map(t=><li key={t}>{t}</li>)}</ul><button className="btn" aria-pressed={selectedId===a.id} onClick={()=>{onSelect(a.id);document.getElementById('preview')?.scrollIntoView({behavior:'smooth'})}}>Preview pathway</button></article>)}</div></section><section id="preview" className="container section"><div className="panel"><div className="tag">CYBER PATHWAY PREVIEW</div><h2>{selected.icon} {selected.title}</h2><p className="muted">{selected.description}</p><div className="grid">{selected.topics.map((t,i)=><div className="card course" key={t}><span className="small">Module {i+1}</span><strong>{t}</strong><span className="small">Learning module preview · Mission experiences in development</span></div>)}</div></div></section></>;
}
