"use client";
import { useId, useState } from "react";
import type { Run } from "./types";
import styles from "./lab.module.css";

export default function GameBoard({
  run,
  busy,
  onAction,
  onReload,
}: {
  run: Run;
  busy: boolean;
  onAction: (action: string, target?: string) => void;
  onReload: () => void;
}) {
  const inspectorId = useId();
  const [view, setView] = useState<"map" | "list">("map");
  const [selected, setSelected] = useState("identity");
  const [help, setHelp] = useState(true);
  const asset = run.assets.find((a) => a.id === selected) ?? run.assets[0];
  const active = run.status === "active";
  return (
    <section aria-label="Branch Defender game" className={styles.game}>
      <div className={styles.gameTop}>
        <div>
          <span className={styles.eyebrow}>
            OPERATION FIREWALL / BRANCH DEFENDER
          </span>
          <h2>
            {run.scenario === undefined || run.scenario === "branch"
              ? "Protect the branch."
              : run.scenario_info?.title}
          </h2>
          <p>
            Run #{run.id} ·{" "}
            {run.status === "active"
              ? "Shift in progress"
              : run.status === "won"
                ? "Branch secured"
                : "Shift ended"}{" "}
            · Saved after every action
          </p>
        </div>
        <button onClick={onReload} disabled={busy}>
          Reload saved run
        </button>
      </div>
      <div className={styles.hud}>
        <div>
          <span>SHIFT</span>
          <strong>
            {run.turn}
            <small>/18 turns</small>
          </strong>
        </div>
        <div>
          <span>BUDGET</span>
          <strong>
            {run.budget}
            <small> credits</small>
          </strong>
        </div>
        <div>
          <span>STAFF</span>
          <strong>
            {run.staff}
            <small> actions</small>
          </strong>
        </div>
        <div>
          <span>SERVICE</span>
          <strong>{run.availability}%</strong>
          <progress
            aria-label="Service availability"
            max={100}
            value={run.availability}
          />
        </div>
        <div>
          <span>DATA EXPOSURE</span>
          <strong>{run.exposure}%</strong>
          <progress aria-label="Data exposure" max={100} value={run.exposure} />
        </div>
      </div>
      <div className={styles.controlStrip}>
        {run.scenario === "supplier" && (
          <span>
            {run.vendor_revoked
              ? "✓ Supplier access revoked"
              : "○ Supplier access enabled"}
          </span>
        )}
        <span>{run.mfa ? "✓ Sign-in protected" : "○ Sign-in exposed"}</span>
        <span>
          {run.segmented ? "✓ Database segmented" : "○ Database path open"}
        </span>
        <span>
          {run.copy_ready ? "✓ Recovery verified" : "○ Recovery unverified"}
        </span>
      </div>
      <button
        className={styles.helpButton}
        aria-expanded={help}
        onClick={() => setHelp((v) => !v)}
      >
        {help ? "Hide" : "Show"} shift briefing
      </button>
      {help && (
        <div className={styles.briefing}>
          <h3>Your objective</h3>
          <p>
            {run.scenario_info?.objective ??
              "By turn 18, clear all compromise, verify recovery and keep at least 80% service available. Victory can occur from turn 8."}{" "}
            Lose at 100% data exposure, or after two consecutive turn advances
            below 25% service.
          </p>
          {run.scenario_info && <p>{run.scenario_info.summary}</p>}
          <ol>
            <li>
              Select an asset on the map. Spend up to three staff actions, then
              advance the turn.
            </li>
            <li>
              Protect relevant entry paths, patch exposed services, deploy
              monitoring and investigate. Hidden compromise may exist even when
              no alert is visible.
            </li>
            <li>
              Isolation stops links but removes service. With a verified
              recovery copy, restore an isolated asset; reconnect after checking
              its condition.
            </li>
          </ol>
          <p>
            Patch, backup verification and restoration finish on the next turn.
            Patching and MFA do not clean existing compromise. An isolated but
            still compromised asset prevents victory.
          </p>
          <p className={styles.muted}>
            Fictional rules simplify real cybersecurity. No live systems are
            connected. No time limit while deciding; leave and resume this run
            later.
          </p>
        </div>
      )}
      <div
        className={styles.viewControls}
        role="group"
        aria-label="Network presentation"
      >
        <button aria-pressed={view === "map"} onClick={() => setView("map")}>
          Network map
        </button>
        <button aria-pressed={view === "list"} onClick={() => setView("list")}>
          Asset list
        </button>
        <a href={"#" + inspectorId}>Go to selected asset controls ↓</a>
      </div>
      <p className={styles.muted}>
        Use Tab to reach assets and Enter or Space to select one. The asset list
        provides the same actions without panning the map. Shape, text and
        status labels supplement colour.
      </p>
      <div className={styles.playLayout}>
        <div className={view === "map" ? styles.mapWrap : styles.listWrap}>
          <div
            className={view === "map" ? styles.map : styles.assetGrid}
            aria-label={
              view === "map"
                ? "Interactive branch network"
                : "Branch asset list"
            }
          >
            <div className={styles.mapLabel}>
              BRANCH NETWORK <span>SECURE CHANNEL / SIMULATION</span>
            </div>
            {view === "map" && (
              <svg
                viewBox="0 0 100 100"
                preserveAspectRatio="none"
                className={styles.connections}
                aria-hidden="true"
              >
                {run.links.map(([a, b]) => {
                  const left = run.assets.find((x) => x.id === a)!,
                    right = run.assets.find((x) => x.id === b)!;
                  return (
                    <line
                      key={a + b}
                      x1={left.x}
                      y1={left.y}
                      x2={right.x}
                      y2={right.y}
                      className={
                        left.isolated ||
                        right.isolated ||
                        (run.segmented && a === "app" && b === "database")
                          ? styles.blocked
                          : styles.link
                      }
                    />
                  );
                })}
              </svg>
            )}
            {run.assets.map((a) => (
              <button
                key={a.id}
                type="button"
                aria-pressed={asset.id === a.id}
                aria-label={
                  a.label +
                  ": " +
                  a.condition +
                  (a.isolated ? ", isolated" : "")
                }
                className={[
                  view === "map" ? styles.asset : styles.assetListItem,
                  asset.id === a.id ? styles.selected : "",
                  a.isolated
                    ? styles.isolated
                    : a.condition === "Compromise detected" || a.encrypted
                      ? styles.alert
                      : "",
                ].join(" ")}
                aria-controls={inspectorId}
                style={
                  view === "map"
                    ? { left: `${a.x}%`, top: `${a.y}%` }
                    : undefined
                }
                onClick={() => setSelected(a.id)}
              >
                <span className={styles.assetIcon} aria-hidden="true">
                  {a.id === "database"
                    ? "▤"
                    : a.id === "identity"
                      ? "◈"
                      : a.id === "backup"
                        ? "▣"
                        : a.id === "gateway"
                          ? "◇"
                          : "▰"}
                </span>
                <strong>{a.label}</strong>
                <small>
                  {a.pending
                    ? "Maintenance: " + a.pending
                    : a.isolated
                      ? "ISOLATED"
                      : a.encrypted
                        ? "SERVICE ENCRYPTED"
                        : a.condition === "Compromise detected"
                          ? "COMPROMISE DETECTED"
                          : a.monitored
                            ? "MONITORED"
                            : "SELECT TO INVESTIGATE"}
                </small>
              </button>
            ))}
            <div className={styles.mapLegend}>
              Teal: connected · Dashed amber: restricted · Amber: isolated ·
              Red: detected compromise
            </div>
          </div>
        </div>
        <aside
          id={inspectorId}
          tabIndex={-1}
          className={styles.inspector}
          aria-label="Selected asset controls"
        >
          <span className={styles.eyebrow}>ASSET CONTROL</span>
          <h3>{asset.label}</h3>
          <p>
            {asset.role} · {asset.weight}% service weight
          </p>
          <p role="status">
            <strong>{asset.condition}</strong>
            {asset.isolated ? " · isolated" : ""}
            {asset.pending ? " · " + asset.pending + " pending" : ""}
          </p>
          <p className={styles.muted}>
            {asset.patched ? "Patched" : "Patch not applied"} ·{" "}
            {asset.monitored ? "Monitoring deployed" : "No monitoring"}
          </p>
          <div className={styles.actionList}>
            {asset.actions.map((action) => (
              <button
                key={action.id}
                disabled={busy || run.staff === 0 || run.budget < action.cost}
                onClick={() => onAction(action.id, asset.id)}
              >
                <strong>
                  {action.label}
                  <span>{action.cost} cr · 1 staff</span>
                </strong>
                <small>{action.help}</small>
              </button>
            ))}
          </div>
          {active && (
            <button
              className={styles.endTurn}
              disabled={busy}
              onClick={() => onAction("end_turn")}
            >
              {busy ? "Saving action…" : "Advance turn →"}
            </button>
          )}
        </aside>
      </div>
      <div className={styles.afterBoard}>
        <section className={styles.timeline} aria-label="Saved shift timeline">
          <h3>Shift timeline</h3>
          <ol>
            {run.events
              .slice()
              .reverse()
              .map((e, i) => (
                <li key={run.events.length - i}>
                  <span>TURN {e.turn}</span>
                  {e.message}
                </li>
              ))}
          </ol>
        </section>
        <section className={styles.debrief}>
          <h3>
            {run.debrief ? "After-action review" : "Decide, observe, adapt"}
          </h3>
          {run.debrief ? (
            <>
              <p>
                {run.status === "won"
                  ? "You met this scenario’s containment, recovery and availability goals."
                  : "Review the timeline and compare another strategy."}
              </p>
              <p>
                Remaining compromise:{" "}
                {run.debrief.remaining_compromise.join(", ") || "none"}.
              </p>
              <ul>
                {run.debrief.lessons.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
              <a
                href={
                  "/cyber-lab?tab=learn&module=" +
                  (run.scenario_info?.lesson ?? "recover")
                }
              >
                Review response and recovery lessons →
              </a>
            </>
          ) : (
            <>
              <p>
                Monitoring buys visibility. Patching reduces this model’s
                exploit paths. Isolation limits spread at a service cost.
              </p>
              <p>
                Protecting one path leaves others to manage. Look at the whole
                network, then compare what changes after each turn.
              </p>
              <p>
                All game actions are recorded by the server. The browser does
                not award points or decide outcomes.
              </p>
            </>
          )}
        </section>
      </div>
    </section>
  );
}
