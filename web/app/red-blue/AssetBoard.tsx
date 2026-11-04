"use client";
import { useEffect, useState } from "react";
import type { Asset, Match } from "./types";
import styles from "./arena.module.css";

function summary(asset: Asset, side: string) {
  if (side === "blue")
    return asset.isolated
      ? "Isolated · service unavailable"
      : asset.disrupted
        ? "Service disrupted"
        : "Service available · access unconfirmed";
  return [
    "No believed foothold",
    "Believed user foothold",
    "Believed privileged foothold",
  ][asset.access || 0];
}

/** Draw only projected inventory/trust edges. Lines never represent secret traffic. */
export default function AssetBoard({
  match,
  selected,
  onSelect,
}: {
  match: Match;
  selected: string;
  onSelect: (id: string) => void;
}) {
  const [mode, setMode] = useState("list");
  useEffect(() => {
    setMode(
      window.matchMedia("(min-width: 760px)").matches ? "network" : "list",
    );
  }, []);
  const positions = Object.fromEntries(
    match.assets.map((a, i) => [
      a.id,
      { x: 30 + (i % 3) * 240, y: 25 + Math.floor(i / 3) * 145 },
    ]),
  );
  const height = Math.ceil(match.assets.length / 3) * 145 + 20;
  // The API already filters observations per authenticated seat. Never derive
  // this panel from private match truth or the terminal debrief.
  const perAsset = new Map<string, Match["observations"]>();
  const knownIds = new Set(match.assets.map((a) => a.id));
  for (const observation of match.observations) {
    if (!observation.target || !knownIds.has(observation.target)) continue;
    const entries = perAsset.get(observation.target) || [];
    entries.push(observation);
    perAsset.set(observation.target, entries);
  }
  const selectedAsset = match.assets.find((asset) => asset.id === selected);
  const selectedEvents = perAsset.get(selected) || [];
  const evidenceLabel = (assetId: string) => {
    const count = perAsset.get(assetId)?.length || 0;
    return count ? `${count} visible event${count === 1 ? "" : "s"}` : "No observed activity";
  };
  return (
    <section className={styles.panel} aria-label="Known assets">
      <div className={styles.sectionHead}>
        <div>
          <span className={styles.eyebrow}>YOUR INFORMATION</span>
          <h3>Organisation network</h3>
        </div>
        <div className={styles.controls} aria-label="Asset view">
          <button
            aria-pressed={mode === "network"}
            onClick={() => setMode("network")}
          >
            Network
          </button>
          <button
            aria-pressed={mode === "list"}
            onClick={() => setMode("list")}
          >
            Asset list
          </button>
        </div>
      </div>
      <p className={styles.muted}>
        {match.side === "red"
          ? "Your inventory is incomplete. Reconnaissance may reveal neighbours. Assessments and footholds can become stale."
          : "You know the inventory and service health. A quiet asset does not establish that it is free of attacker access."}{" "}
        Arrows show allowed trust paths.
      </p>
      {mode === "network" ? (
        <div className={styles.networkScroll}>
          <div className={styles.network} style={{ height }}>
            <svg width="740" height={height} aria-hidden="true">
              <defs>
                <marker
                  id="trust-arrow"
                  markerWidth="8"
                  markerHeight="8"
                  refX="7"
                  refY="4"
                  orient="auto"
                >
                  <path d="M0,0 L8,4 L0,8" fill="#57879a" />
                </marker>
              </defs>
              {match.connections.map((e) => {
                const a = positions[e.source],
                  b = positions[e.target];
                const dx = b.x - a.x,
                  dy = b.y - a.y;
                // Clip to the card boundary so the directed arrow is visible,
                // rather than drawing its head underneath the target card.
                const edge =
                  1 / Math.max(Math.abs(dx) / 106, Math.abs(dy) / 65);
                return (
                  <line
                    key={e.source + e.target}
                    x1={a.x + 100 + dx * edge}
                    y1={a.y + 59 + dy * edge}
                    x2={b.x + 100 - dx * edge}
                    y2={b.y + 59 - dy * edge}
                    stroke="#57879a"
                    strokeWidth="2"
                    markerEnd="url(#trust-arrow)"
                  />
                );
              })}
            </svg>
            {match.assets.map((a) => (
              <button
                key={a.id}
                className={`${styles.node} ${a.id === selected ? styles.selected : ""}`}
                aria-pressed={a.id === selected}
                onClick={() => onSelect(a.id)}
                style={{ left: positions[a.id].x, top: positions[a.id].y }}
              >
                <span>
                  {a.kind.replace("_", " ")} · value {a.value}
                </span>
                <strong>{a.name}</strong>
                <small>{summary(a, match.side)}</small>
                <small>{evidenceLabel(a.id)}</small>
              </button>
            ))}
          </div>
        </div>
      ) : (
        <div className={styles.assetGrid}>
          {match.assets.map((a) => (
            <button
              key={a.id}
              aria-pressed={a.id === selected}
              className={`${styles.asset} ${a.id === selected ? styles.selected : ""}`}
              onClick={() => onSelect(a.id)}
            >
              <span>
                {a.kind.replace("_", " ")} · value {a.value}
              </span>
              <strong>{a.name}</strong>
              <small>{summary(a, match.side)}</small>
              <small>{evidenceLabel(a.id)}</small>
            </button>
          ))}
        </div>
      )}
      {selectedAsset && (
        <section aria-label="Selected asset evidence">
          <h4>{selectedAsset.name} · observed evidence</h4>
          <p className={styles.muted}>
            {match.side === "blue"
              ? "Only your controls, investigations and detected telemetry are shown. An alert indicates suspicion, not proof of a successful attack."
              : "Only actions and intelligence available to your Red seat appear. Your assessments may be outdated."}
          </p>
          {selectedEvents.length ? (
            <ol>
              {selectedEvents.slice(-8).map((event, index) => (
                <li key={`${event.turn}-${event.type}-${index}`}>
                  <strong>Round {event.turn}</strong>{" "}
                  {event.type === "alert" ? "· Suspected activity" :
                    event.type === "finding" ? "· Investigation finding" :
                    event.type === "own_action" ? "· Your action" :
                    "· Observed event"}: {event.message}
                </li>
              ))}
            </ol>
          ) : (
            <p>No evidence has been recorded for this asset in your view. That does not establish that it is safe.</p>
          )}
        </section>
      )}
      <details>
        <summary>Read directed trust paths</summary>
        {match.connections.length ? (
          <ul>
            {match.connections.map((e) => (
              <li key={e.source + e.target}>
                {match.assets.find((a) => a.id === e.source)?.name} →{" "}
                {match.assets.find((a) => a.id === e.target)?.name}
              </li>
            ))}
          </ul>
        ) : (
          <p>No trust paths are currently known.</p>
        )}
      </details>
    </section>
  );
}
