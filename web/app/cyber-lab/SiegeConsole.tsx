"use client";
import type { Run } from "./types";
import styles from "./lab.module.css";

/** Show only reported signals and public work; never forecast hidden enemy state. */
export default function SiegeConsole({
  run,
  busy,
  onAction,
  onLocate,
}: {
  run: Run;
  busy: boolean;
  onAction: (action: string, target?: string) => void;
  onLocate: (asset: string) => void;
}) {
  const tactics = run.tactics;
  if (!tactics) return null;
  const active = run.status === "active";
  const pending = tactics.signals.filter((signal) => !signal.reviewed);
  const reviewed = tactics.signals.filter((signal) => signal.reviewed);
  const latest = reviewed
    .slice()
    .sort((a, b) => (b.review_order ?? 0) - (a.review_order ?? 0))[0];
  const label = (id: string) =>
    run.assets.find((asset) => asset.id === id)?.label ?? id;
  return (
    <section
      className={styles.commandConsole}
      aria-label="Incident command console"
    >
      <div className={styles.consoleHeading}>
        <div>
          <span className={styles.eyebrow}>BRANCH SIEGE / COMMAND DESK</span>
          <h3>Read the signals. Make the tradeoff.</h3>
        </div>
        <span className={styles.pressure}>
          Opponent pressure: {tactics.pressure}
        </span>
      </div>
      <ul className={styles.objectives}>
        {tactics.objectives.map((objective) => (
          <li key={objective.label}>
            <span aria-hidden="true">{objective.met ? "✓" : "○"}</span>
            <span>
              {objective.label}
              <small>
                {objective.met ? "Recorded milestone met" : "Still to address"}
              </small>
            </span>
          </li>
        ))}
      </ul>
      <p className={styles.muted}>
        Clear all compromise as well as these visible milestones. A recorded
        observation or validation can become stale; it does not reveal every
        hidden change.
      </p>
      <div className={styles.commandColumns}>
        <section aria-label="Investigation queue">
          <h4>Investigation queue · {pending.length} open</h4>
          {latest && (
            <div className={styles.latestFinding} role="status">
              <strong>
                Latest finding: {label(latest.asset)} · {latest.finding}
              </strong>
              <p>
                Observed turn {latest.reviewed_turn}. Later state may differ.
              </p>
              <button onClick={() => onLocate(latest.asset)}>
                Open {label(latest.asset)} controls
              </button>
            </div>
          )}
          <p>
            Reports are clues. Investigate before treating a report as confirmed
            compromise.
          </p>
          {pending.length === 0 && (
            <p>
              No unreviewed reports. Continue checking entry paths, service and
              recovery.
            </p>
          )}
          {pending.map((signal) => {
            const maintenance = run.assets.find(
              (asset) => asset.id === signal.asset,
            )?.pending;
            return (
              <article key={signal.id} className={styles.signal}>
                <span className={styles.eyebrow}>
                  {signal.id} · REPORTED TURN {signal.turn}
                </span>
                <h4>{label(signal.asset)}</h4>
                <p>{signal.message}</p>
                <button
                  disabled={busy || !active || run.staff < 1 || !!maintenance}
                  onClick={() => onAction("investigate_signal", signal.id)}
                >
                  Investigate {signal.id} · 1 staff
                </button>
                {maintenance && (
                  <p>
                    Asset work is in progress; investigate after it completes.
                  </p>
                )}
              </article>
            );
          })}
          {!!reviewed.length && (
            <details>
              <summary>{reviewed.length} reviewed reports</summary>
              {reviewed.map((signal) => (
                <p key={signal.id}>
                  <strong>
                    {label(signal.asset)} · {signal.finding}
                  </strong>
                  <br />
                  Observed turn {signal.reviewed_turn}. Report received turn{" "}
                  {signal.turn}.
                </p>
              ))}
            </details>
          )}
        </section>
        <section aria-label="Staff and work orders">
          <h4>Work orders</h4>
          {tactics.jobs.length === 0 ? (
            <p>No queued work.</p>
          ) : (
            <ul>
              {tactics.jobs.map((job) => (
                <li key={job.asset}>
                  <strong>{label(job.asset)}</strong>:{" "}
                  {job.action === "patch"
                    ? "patching"
                    : job.action === "restore"
                      ? "restoration"
                      : "recovery verification"}{" "}
                  completes on turn {job.due_turn}.
                </li>
              ))}
            </ul>
          )}
          <p>
            Two-turn work takes effect when you advance to its due turn.
            Maintenance and isolation may stop dependent services.
          </p>
          <div className={styles.supportCard}>
            <h4>Emergency staff</h4>
            <p>
              Trade 6 credits for 2 extra actions this turn. Available once per
              shift; unused extra actions expire on the next turn.
            </p>
            <button
              disabled={busy || !tactics.support_available}
              onClick={() => onAction("call_support", "support")}
            >
              {tactics.support_used
                ? "Emergency support already mobilised"
                : "Mobilise emergency support · 6 credits"}
            </button>
          </div>
          <p role="status">
            Turn {run.turn} · {run.staff} staff action
            {run.staff === 1 ? "" : "s"} available · {run.budget} credits
            remaining.
          </p>
        </section>
      </div>
    </section>
  );
}
