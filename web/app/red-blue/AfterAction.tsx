"use client";
import type { Debrief, Side } from "./types";
import styles from "./arena.module.css";

export default function AfterAction({ result, seat }: { result: Debrief; seat: Side }) {
  const pivotal = result.pivotal?.length
    ? result.pivotal
    : result.timeline
        .filter((event) => !event.action.startsWith("wait_"))
        .slice(0, 5)
        .map((event) => ({
          ...event,
          reason: "Review this resolved action and its observable impact.",
          alternatives: result.alternatives.filter((a) => a.turn === event.turn && a.action !== event.action).slice(0, 2),
        }));
  return (
    <section className={styles.panel} aria-labelledby="debrief-heading">
      <span className={styles.eyebrow}>AFTER ACTION REVIEW · MATCH FINISHED</span>
      <h2 id="debrief-heading">
        {result.winner === "blue" ? "Blue protected the objective" : "Red achieved the objective"}
      </h2>
      <p>{result.explanation}</p>
      <h3>Most consequential decisions</h3>
      <p className={styles.muted}>
        Up to five ranked decisions, viewed from your {seat.toUpperCase()} seat.
        Post-match evidence is more complete than the information available during play.
      </p>
      {pivotal.length ? (
        <ol>
          {pivotal.map((event, index) => (
            <li key={`${event.turn}-${event.side}-${index}`}>
              <strong>Round {event.turn} · {event.side.toUpperCase()} · {event.action.replaceAll("_", " ")}</strong>
              {event.target ? ` · ${event.target}` : ""}
              <p>{event.success ? "Achieved its immediate aim." : "Did not achieve its immediate aim."} {event.reason}</p>
              {event.side === "red" && (
                <p>{event.detected ? "An alert was generated." : "No alert was generated."}</p>
              )}
              {event.alternatives.length ? (
                <ul>
                  {event.alternatives.slice(0, 2).map((alternative, i) => (
                    <li key={i}>
                      <strong>Seeded alternative:</strong>{" "}
                      {alternative.action.replaceAll("_", " ")}
                      {alternative.target ? ` on ${alternative.target}` : ""}.{" "}
                      {alternative.explanation}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className={styles.muted}>No measured alternative is available for this decision.</p>
              )}
            </li>
          ))}
        </ol>
      ) : <p>No consequential non-pass decisions were recorded.</p>}
      <details>
        <summary>Show complete action transcript ({result.timeline.length} actions)</summary>
        <ol>
          {result.timeline.map((event, index) => (
            <li key={index}>
              Round {event.turn} · {event.side.toUpperCase()} ·{" "}
              {event.action.replaceAll("_", " ")}
              {event.target ? ` → ${event.target}` : ""} ·{" "}
              {event.success ? "achieved aim" : "no confirmed success"}.
              {" "}<a href={event.framework.url} target="_blank" rel="noreferrer">
                {event.framework.technique}
              </a>
            </li>
          ))}
        </ol>
      </details>
    </section>
  );
}
