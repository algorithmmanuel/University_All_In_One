"use client";
import { useState } from "react";
import styles from "./arena.module.css";

const lessons = [
  {
    heading: "Two seats, two objectives",
    text: "Blue protects critical services and business integrity. Red attempts the fictional scenario objective before the round limit. Both seats receive different, incomplete information.",
    example: "Blue chooses a monitoring or protective action before Red's first attempted compromise in alternating matches.",
  },
  {
    heading: "Assets, trust paths and resources",
    text: "Each asset has business value and authorised connections. Your budget is finite, and a turn accepts only one permitted action. Isolation prevents further use but may interrupt normal service.",
    example: "A teller workstation may connect to an identity service, but an unknown connection stays hidden until your seat discovers it.",
  },
  {
    heading: "Evidence is not omniscience",
    text: "Blue sees owned controls, service availability, and only the alerts its monitoring or investigations support. Red sees confirmed own actions and scoped reconnaissance, not Blue's private decisions.",
    example: "A suspicious-activity alert does not prove that an attempted phishing action succeeded; silence does not prove safety.",
  },
  {
    heading: "A worked Blue → Red → Blue exchange",
    text: "First, Blue monitors the teller workstation. Next, Red attempts phishing. Blue's following turn is based on any genuine alerts and known availability; Red may have no idea which tools Blue installed.",
    example: "Blue may investigate an alert or contain an asset, while Red may discover that a previously believed foothold is no longer usable.",
  },
  {
    heading: "Deadlines, reconnects and final review",
    text: "Development timed matches have 90 seconds per active seat. The server decides expiry and may grant a one-time 30-second grace for qualifying inactivity; closing a tab is not a guaranteed pause. Saved matches can be resumed.",
    example: "After the result, compare pivotal decisions and optional complete history. Hypothetical alternatives replay only one decision and are not guaranteed to reverse the winner.",
  },
];

export default function GameGuide({
  completed,
  busy,
  onComplete,
  onClose,
}: {
  completed: boolean;
  busy: boolean;
  onComplete: () => void;
  onClose: () => void;
}) {
  const [step, setStep] = useState(0);
  const entry = lessons[step];
  return (
    <section className={styles.panel} aria-label="Red Blue first-launch guide">
      <span className={styles.eyebrow}>FIRST-LAUNCH WALKTHROUGH</span>
      <h2>How to play Red / Blue</h2>
      <p className={styles.muted}>
        Step {step + 1} of {lessons.length}. This guide is separate from the match and cannot change outcomes.
      </p>
      <div role="group" aria-label="Guide step">
        <h3>{entry.heading}</h3>
        <p>{entry.text}</p>
        <p><strong>Example:</strong> {entry.example}</p>
      </div>
      <div className={styles.guideControls}>
        <button type="button" disabled={step === 0} onClick={() => setStep((n) => n - 1)}>
          Previous
        </button>
        {step + 1 < lessons.length ? (
          <button type="button" onClick={() => setStep((n) => n + 1)}>Next step</button>
        ) : (
          <button type="button" disabled={busy} onClick={onComplete}>
            {completed ? "Finish review" : "Finish and remember for this account"}
          </button>
        )}
        <button type="button" onClick={onClose}>Close guide</button>
      </div>
    </section>
  );
}
