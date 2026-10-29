"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { STAGES, type Stage, type Audience } from "../../lib/learning-journey";
import styles from "./journey.module.css";
type Case = { id: string; stage: string; title: string; briefing: string };
const API = (process.env.NEXT_PUBLIC_API_BASE_URL || "").replace(/\/$/, "");
export default function StageWorkshops({
  stage,
  audience,
}: {
  stage: Stage;
  audience: Audience;
}) {
  const [cases, setCases] = useState<Case[] | null>(null),
    [error, setError] = useState(false);
  useEffect(() => {
    const controller = new AbortController();
    fetch(API + "/api/v1/workshops/catalog", { signal: controller.signal })
      .then(async (r) => {
        if (!r.ok) throw Error();
        const b = await r.json();
        if (
          !Array.isArray(b.cases) ||
          !b.cases.length ||
          !b.cases.every(
            (c: Case) =>
              c &&
              typeof c.id === "string" &&
              /^[a-z][a-z0-9-]{0,47}$/.test(c.id) &&
              typeof c.title === "string" &&
              typeof c.briefing === "string" &&
              STAGES.some((s) => s.id === c.stage),
          )
        )
          throw Error();
        setCases(b.cases);
      })
      .catch(() => {
        if (!controller.signal.aborted) setError(true);
      });
    return () => controller.abort();
  }, []);
  return (
    <section className={styles.workshops} aria-labelledby="stage-workshops">
      <h3 id="stage-workshops">
        Decision workshops · explore another approach
      </h3>
      <p>
        Three saved, multi-decision cases for this stage. Read the evidence, see
        the authored consequences and replay to compare another approach. These
        complement the full missions and simulations.
      </p>
      {error ? (
        <p>
          Workshop catalogue is temporarily unavailable.{" "}
          <Link href="/workshops">Try the workshop library</Link>.
        </p>
      ) : cases === null ? (
        <p role="status">Loading decision workshops…</p>
      ) : (
        <div className={styles.resources}>
          {cases
            .filter((c) => c.stage === stage)
            .map((c) => (
              <article key={c.id}>
                <span className="tag">3 DECISIONS · SAVED REPLAY</span>
                <h4>{c.title}</h4>
                <p>{c.briefing}</p>
                <Link
                  className="btn secondary"
                  href={`/workshops?case=${c.id}&journey_stage=${stage}&journey_pathway=${audience}`}
                >
                  Explore {c.title} →
                </Link>
              </article>
            ))}
        </div>
      )}
    </section>
  );
}
