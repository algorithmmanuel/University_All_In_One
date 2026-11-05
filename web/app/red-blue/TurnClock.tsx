"use client";
import { useEffect, useState } from "react";
import type { Match, Side } from "./types";
import styles from "./arena.module.css";

/** Display-only timer. All turn permission and expiry belong to the server. */
export default function TurnClock({
  clock,
  activeSide,
  seat,
}: {
  clock: NonNullable<Match["clock"]>;
  activeSide?: Side | null;
  seat: Side;
}) {
  const [remaining, setRemaining] = useState(clock.seconds_remaining);
  useEffect(() => {
    const receivedAt = Date.now();
    const initial = clock.seconds_remaining;
    setRemaining(initial);
    const timer = window.setInterval(() => {
      // Local time is only an estimated display; never sent as authority.
      const elapsed = Math.floor((Date.now() - receivedAt) / 1000);
      setRemaining(Math.max(0, initial - elapsed));
    }, 500);
    return () => window.clearInterval(timer);
  }, [clock.deadline_at, clock.seconds_remaining]);
  return (
    <section className={styles.panel} aria-label="Timed turn status">
      <h3>Server-controlled turn clock</h3>
      <p role="timer" aria-live="off">
        <strong>{remaining} seconds remaining</strong>
        {" · "}{activeSide === seat ? "Your turn" : "Opponent's turn"}
      </p>
      {clock.grace_active && (
        <p>The server granted the active seat its one-time 30-second grace.</p>
      )}
      <p className={styles.muted}>
        This countdown is an estimate. Server time determines whether an action
        is accepted. Expired turns pass automatically.
      </p>
    </section>
  );
}
