"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import StageWorkshops from "../../components/journey/StageWorkshops";
import { AccountNavigation } from "../../components/home/account-navigation";
import { useActivityFocus } from "../../lib/use-activity-focus";
import {
  AUDIENCES,
  STAGES,
  parseJourney,
  resourcesFor,
  journeyUrl,
  type Stage,
  type Audience,
} from "../../lib/learning-journey";
import styles from "../../components/journey/journey.module.css";
export default function Journey() {
  const [stage, setStage] = useState<Stage>("discover"),
    [audience, setAudience] = useState<Audience>("all");
  const [opened, setOpened] = useState(0);
  const heading = useActivityFocus(opened);
  useEffect(() => {
    const sync = () => {
      const p = parseJourney(window.location.search);
      setStage(p.stage);
      setAudience(p.audience);
    };
    sync();
    if (
      STAGES.some(
        (s) =>
          s.id === new URLSearchParams(window.location.search).get("stage"),
      )
    )
      setOpened(1);
    window.addEventListener("popstate", sync);
    return () => window.removeEventListener("popstate", sync);
  }, []);
  function select(next: Stage, path: Audience, move = true) {
    setStage(next);
    setAudience(path);
    window.history.pushState(null, "", journeyUrl(next, path));
    if (move) setOpened((n) => n + 1);
  }
  const index = STAGES.findIndex((s) => s.id === stage),
    current = STAGES[index];
  return (
    <>
      <header className={`container ${styles.header}`}>
        <Link className="brand" href="/">
          EduCyber
        </Link>
        <AccountNavigation />
      </header>
      <main className={`container ${styles.main}`}>
        <section className={styles.intro}>
          <span className="tag">LEARN · INVESTIGATE · DEFEND · COMPETE</span>
          <h1>Your cybersecurity learning journey</h1>
          <p>
            Move from understanding a concept to making decisions under
            uncertainty. Start at the beginning, return to an earlier topic, or
            jump directly to a later stage.
          </p>
          <p className="small">
            Stages are guidance, not locked levels or claims of mastery.
            Immersion and difficulty are different: an advanced investigation
            can be harder than a beginner strategy match.
          </p>
        </section>
        <section className={styles.pathways} aria-labelledby="pathway-heading">
          <h2 id="pathway-heading">Choose an audience pathway</h2>
          <p>
            This tailors the suggested materials to your interests. Every stage
            stays open.
          </p>
          <div className={styles.pathGrid}>
            {AUDIENCES.map((a) => (
              <button
                type="button"
                key={a.id}
                aria-pressed={a.id === audience}
                onClick={() => select(stage, a.id, false)}
              >
                <strong>{a.title}</strong>
                <span>{a.description}</span>
              </button>
            ))}
          </div>
        </section>
        <div className={styles.layout}>
          <nav aria-labelledby="choose-stage">
            <h2 id="choose-stage" tabIndex={-1}>
              Choose your starting stage
            </h2>
            <p className="small">
              New here? Start at 1. Already experienced? Choose any stage.
            </p>
            <ol className={styles.stages}>
              {STAGES.map((s, i) => (
                <li key={s.id}>
                  <button
                    type="button"
                    aria-current={s.id === stage ? "step" : undefined}
                    onClick={() => select(s.id, audience)}
                  >
                    <span>{i + 1}</span>
                    <strong>{s.title}</strong>
                  </button>
                </li>
              ))}
            </ol>
          </nav>
          <section className={styles.detail} aria-labelledby="stage-heading">
            <span className="tag">
              STAGE {index + 1} OF 8 ·{" "}
              {AUDIENCES.find((a) => a.id === audience)?.title}
            </span>
            <h2
              id="stage-heading"
              ref={heading}
              tabIndex={-1}
              className="activity-heading"
            >
              {current.title}
            </h2>
            <p className={styles.question}>{current.question}</p>
            <p>{current.description}</p>
            <div className={styles.resources}>
              {resourcesFor(stage, audience).map((r) => (
                <article key={r.href}>
                  <span className="tag">{r.kind}</span>
                  <h3>{r.title}</h3>
                  <p>{r.description}</p>
                  <Link className="btn" href={r.href}>
                    Open {r.title} →
                  </Link>
                </article>
              ))}
            </div>
            <StageWorkshops stage={stage} audience={audience} />
            <aside className={styles.reflect}>
              <strong>Before you move on</strong>
              <p>
                {stage === "discover" || stage === "understand"
                  ? "Explain the idea in your own words and try a short check. Return to the explanation when you are unsure."
                  : stage === "check"
                    ? "Use mistakes to choose what to revisit. A short score is evidence from that attempt, not a complete measure of your ability."
                    : "Review what you knew, what you chose and what happened. Use the debrief or explanations before trying a different decision."}
              </p>
              <p>
                Account-based activities require sign-in. Opening a link does
                not start a mission, create a match or mark anything complete.
              </p>
            </aside>
            <div className={styles.actions}>
              {index > 0 && (
                <button
                  type="button"
                  className="btn secondary"
                  onClick={() => select(STAGES[index - 1].id, audience)}
                >
                  ← Previous stage
                </button>
              )}
              {index < 7 && (
                <button
                  type="button"
                  className="btn"
                  onClick={() => select(STAGES[index + 1].id, audience)}
                >
                  Next stage →
                </button>
              )}
            </div>
          </section>
        </div>
        <section className={styles.browse}>
          <h2>Return to an activity or saved progress</h2>
          <p>
            Use the dashboard to continue saved work. You can also browse each
            collection directly.
          </p>
          <nav
            className={styles.actions}
            aria-label="Browse learning collections"
          >
            <Link href="/dashboard">Dashboard and saved progress</Link>
            <Link href="/learn">Courses</Link>
            <Link href="/assessments">Assessments</Link>
            <Link href="/missions">Guided missions</Link>
            <Link href="/cyber-lab">Cyber Lab</Link>
            <Link href="/red-blue">Red / Blue</Link>
          </nav>
        </section>
      </main>
    </>
  );
}
