import type { Debrief } from "./types";
import styles from "./arena.module.css";
export default function AfterAction({ result }: { result: Debrief }) {
  const turns = [...new Set(result.timeline.map((e) => e.turn))];
  return (
    <section className={styles.panel} aria-labelledby="debrief-heading">
      <span className={styles.eyebrow}>AFTER ACTION REVIEW</span>
      <h2 id="debrief-heading">
        {result.winner === "blue"
          ? "Blue protected the objective"
          : "Red achieved the objective"}
      </h2>
      <p>{result.explanation}</p>
      {turns.map((turn) => (
        <details key={turn}>
          <summary>Round {turn} · decisions and missed opportunities</summary>
          <ol>
            {result.timeline
              .filter((e) => e.turn === turn)
              .map((e) => (
                <li key={e.side}>
                  <strong>{e.side.toUpperCase()}</strong> ·{" "}
                  {e.action.replaceAll("_", " ")}
                  {e.target ? " → " + e.target : ""}
                  {e.source ? " from " + e.source : ""}:{" "}
                  {e.success ? "achieved its aim" : "did not achieve its aim"}
                  {e.side === "red"
                    ? e.detected
                      ? "; alert generated"
                      : "; no alert generated"
                    : ""}
                  .{" "}
                  <a href={e.framework.url} target="_blank" rel="noreferrer">
                    {e.framework.technique}
                  </a>
                </li>
              ))}
          </ol>
          {result.missed
            .filter((e) => e.turn === turn)
            .map((e, i) => (
              <p key={i}>
                <strong>Evidence gap:</strong> {e.target} · {e.reason}
              </p>
            ))}
          {result.alternatives
            .filter((e) => e.turn === turn)
            .map((e, i) => (
              <p key={i}>
                <strong>Alternative:</strong> {e.action.replaceAll("_", " ")} →{" "}
                {e.target}. {e.explanation}
              </p>
            ))}
          {!result.alternatives.some((e) => e.turn === turn) && (
            <p>
              No tested affordable Blue alternative improved the measured
              outcomes in this round. This does not establish that the original
              choice was optimal.
            </p>
          )}
        </details>
      ))}
    </section>
  );
}
