"use client";
import type { Run, SiegeMetrics } from "./types";
import styles from "./lab.module.css";

const METRICS: { key: keyof SiegeMetrics; title: string; suffix?: string }[] = [
  { key: "turns", title: "Turns used" },
  { key: "credits_spent", title: "Credits spent" },
  { key: "lowest_service", title: "Lowest observed service", suffix: "%" },
  { key: "exposure", title: "Final exposure indicator", suffix: "%" },
  { key: "actions_used", title: "Decisions made" },
  { key: "signals_reviewed", title: "Signals investigated" },
];

export default function SiegeDebrief({
  run,
  busy,
  onReplay,
}: {
  run: Run;
  busy: boolean;
  onReplay: () => void;
}) {
  const review = run.debrief;
  if (!review?.metrics || !review.history) return null;
  const history = review.history;
  const points = (key: "availability" | "exposure") =>
    history
      .map(
        (item, index) =>
          `${10 + (index * 480) / Math.max(1, history.length - 1)},${110 - item[key]}`,
      )
      .join(" ");
  const assetName = (id: string) =>
    run.assets.find((asset) => asset.id === id)?.label ?? id;
  return (
    <section
      className={styles.siegeReview}
      aria-label="Incident outcome comparison"
    >
      <h3>Your decisions changed the incident.</h3>
      <div className={styles.outcomeGrid}>
        {METRICS.map((metric) => (
          <div key={metric.key}>
            <span>{metric.title}</span>
            <strong>
              {review.metrics![metric.key]}
              {metric.suffix ?? ""}
            </strong>
          </div>
        ))}
      </div>
      <figure className={styles.serviceChart}>
        <svg
          viewBox="0 0 500 125"
          role="img"
          aria-label="Service availability and exposure indicator at each turn; exact values follow in the table"
        >
          {[10, 60, 110].map((y) => (
            <line key={y} x1="10" x2="490" y1={y} y2={y} stroke="#355269" />
          ))}
          <polyline
            points={points("availability")}
            fill="none"
            stroke="#6ff4d5"
            strokeWidth="3"
          />
          <polyline
            points={points("exposure")}
            fill="none"
            stroke="#ffad86"
            strokeWidth="3"
            strokeDasharray="6 4"
          />
        </svg>
        <figcaption>
          Solid teal: service · Dashed amber: exposure indicator · Turn
          boundaries only; the decision ledger also records within-turn service
          changes.
        </figcaption>
      </figure>
      <details>
        <summary>Exact turn history</summary>
        <div className={styles.reviewTable}>
          <table>
            <caption>Recorded turn-boundary outcomes</caption>
            <thead>
              <tr>
                <th>Turn</th>
                <th>Service</th>
                <th>Exposure indicator</th>
              </tr>
            </thead>
            <tbody>
              {history.map((item) => (
                <tr key={item.turn}>
                  <td>{item.turn}</td>
                  <td>{item.availability}%</td>
                  <td>{item.exposure}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </details>
      {review.comparison && (
        <div className={styles.reviewTable}>
          <table>
            <caption>
              Same opening: previous attempt versus this attempt
            </caption>
            <thead>
              <tr>
                <th>Measure</th>
                <th>Previous</th>
                <th>This attempt</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <th>Outcome</th>
                <td>{review.comparison.status}</td>
                <td>{review.metrics.status}</td>
              </tr>
              {METRICS.map((metric) => (
                <tr key={metric.key}>
                  <th>{metric.title}</th>
                  <td>
                    {review.comparison![metric.key]}
                    {metric.suffix ?? ""}
                  </td>
                  <td>
                    {review.metrics![metric.key]}
                    {metric.suffix ?? ""}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <details>
        <summary>Review the decision ledger</summary>
        <div className={styles.reviewTable}>
          <table>
            <caption>Resource and service consequences of your actions</caption>
            <thead>
              <tr>
                <th>Turn</th>
                <th>Decision</th>
                <th>Target</th>
                <th>Cost</th>
                <th>Service before → after</th>
              </tr>
            </thead>
            <tbody>
              {review.decisions?.map((decision, index) => (
                <tr key={index}>
                  <td>{decision.turn}</td>
                  <td>{decision.label}</td>
                  <td>{assetName(decision.target)}</td>
                  <td>{decision.cost}</td>
                  <td>
                    {decision.service_before}% → {decision.service_after}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </details>
      <p>
        Replay keeps the same opening and opponent rules. Your choices change
        the available paths and subsequent outcomes. Compare tradeoffs rather
        than treating one metric as a skill rating.
      </p>
      <button className={styles.primary} disabled={busy} onClick={onReplay}>
        Replay the same incident →
      </button>
    </section>
  );
}
