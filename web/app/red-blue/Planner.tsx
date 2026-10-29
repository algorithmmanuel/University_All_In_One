"use client";
import { useEffect, useState } from "react";
import type { Action, Match, Order } from "./types";
import styles from "./arena.module.css";
export default function Planner({
  match,
  actions,
  selected,
  busy,
  uncertain,
  onSeal,
}: {
  match: Match;
  actions: Action[];
  selected: string;
  busy: boolean;
  uncertain: boolean;
  onSeal: (o?: Order) => void;
}) {
  const [choice, setChoice] = useState("");
  const options = match.orders.filter(
    (o) => o.target === selected || o.target === null,
  );
  const chosen = options.find((o) => JSON.stringify(o) === choice);
  const action = actions.find((a) => a.id === chosen?.action);
  const asset = match.assets.find((a) => a.id === selected);
  useEffect(() => {
    setChoice("");
  }, [selected, match.id, match.turn]);
  return (
    <section className={styles.panel} aria-labelledby="planning-heading">
      <span className={styles.eyebrow}>ONE SEALED CHOICE</span>
      <h3 id="planning-heading">Plan this round</h3>
      {asset && (
        <div className={styles.inspector}>
          <h4>{asset.name}</h4>
          <p>
            {asset.exposed ? "Externally exposed" : "Internal trust boundary"} ·
            business value {asset.value}
          </p>
          {match.side === "blue" ? (
            <>
              <p>Controls: {asset.controls?.join(", ") || "None recorded"}</p>
              <p>
                Known weaknesses:{" "}
                {asset.vulnerabilities?.join(", ") || "None recorded"}
              </p>
            </>
          ) : (
            <>
              <p>
                Last assessment:{" "}
                {asset.assessed
                  ? "round " + asset.assessed.turn
                  : "not assessed"}
              </p>
              {asset.assessed && (
                <>
                  <p>
                    Assessed controls:{" "}
                    {asset.assessed.controls.join(", ") || "none"}
                  </p>
                  <p>
                    Assessed weaknesses:{" "}
                    {asset.assessed.vulnerabilities.join(", ") || "none"}
                  </p>
                </>
              )}
              <p>
                Fictional impact recorded:{" "}
                {[
                  asset.leaked && "data copied",
                  asset.fraud && "records altered",
                  asset.disrupted && "service disrupted",
                ]
                  .filter(Boolean)
                  .join(", ") || "none in your evidence"}
              </p>
            </>
          )}
        </div>
      )}
      {match.status === "waiting" ? (
        <p>Waiting for a second learner. Planning opens after they join.</p>
      ) : match.winner ? (
        <p>Match finished. Review the debrief below.</p>
      ) : match.committed ? (
        <div role="status">
          <strong>Choice sealed. Waiting for the other seat.</strong>
          <p>
            Your choice: {match.committed_order?.action.replaceAll("_", " ")}{" "}
            {match.committed_order?.target || ""}. It cannot be edited. You can
            leave and resume later.
          </p>
        </div>
      ) : (
        <>
          <p>
            Select an asset, then a conceptual action. Both choices resolve
            together: Blue first, then Red. Blocked actions still spend their
            cost.
          </p>
          <label htmlFor="planned-order">
            Action for {asset?.name || "this round"}
          </label>
          <select
            id="planned-order"
            value={choice}
            disabled={busy || uncertain}
            onChange={(e) => setChoice(e.target.value)}
          >
            <option value="">Choose an action</option>
            {options.map((o) => (
              <option key={JSON.stringify(o)} value={JSON.stringify(o)}>
                {o.action.replaceAll("_", " ")}
                {o.source
                  ? " from " +
                    (match.assets.find((a) => a.id === o.source)?.name ||
                      o.source)
                  : ""}{" "}
                · {actions.find((a) => a.id === o.action)?.cost} credits
              </option>
            ))}
          </select>
          {action && (
            <div className={styles.actionDetails}>
              <h4>{action.id.replaceAll("_", " ")}</h4>
              <p>{action.explanation}</p>
              <p>
                <strong>Cost:</strong> {action.cost} credits and {action.cost}{" "}
                of this round’s {match.action_points} AP cap. One action only;
                unused AP expire.
              </p>
              <p>
                <strong>Prerequisite:</strong> {action.prerequisites}
              </p>
              <p>{action.rule}</p>
              <a href={action.url} target="_blank" rel="noreferrer">
                {action.technique} · {action.relation} MITRE ATT&CK ↗
              </a>
            </div>
          )}
          <button
            className="btn"
            disabled={!chosen || busy || uncertain}
            onClick={() => chosen && onSeal(chosen)}
          >
            Seal choice
          </button>
        </>
      )}
      {uncertain && (
        <div role="status">
          <p>
            The response was interrupted. Retry the same sealed request safely,
            or refresh to check its saved state.
          </p>
          <button disabled={busy} onClick={() => onSeal()}>
            Retry same choice
          </button>
        </div>
      )}
    </section>
  );
}
