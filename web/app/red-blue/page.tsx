"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import JourneyLink from "../../components/journey/JourneyLink";
import { AccountNavigation } from "../../components/home/account-navigation";
import { focusActivity } from "../../lib/activity-focus";
import { useActivityFocus } from "../../lib/use-activity-focus";
import { useArena } from "./useArena";
import AssetBoard from "./AssetBoard";
import Planner from "./Planner";
import AfterAction from "./AfterAction";
import type { Side } from "./types";
import styles from "./arena.module.css";

export default function RedBlueArena() {
  const arena = useArena();
  const [scenario, setScenario] = useState("microfinance"),
    [side, setSide] = useState<Side>("blue");
  const [mode, setMode] = useState("computer"),
    [difficulty, setDifficulty] = useState("standard");
  const [token, setToken] = useState(""),
    [selected, setSelected] = useState("");
  useEffect(() => {
    if (!arena.catalog) return;
    const p = new URLSearchParams(window.location.search);
    const scenarioId = p.get("scenario");
    if (arena.catalog.scenarios.some((s) => s.id === scenarioId))
      setScenario(scenarioId!);
    if (p.get("mode") === "human" || p.get("mode") === "computer")
      setMode(p.get("mode")!);
    if (p.get("side") === "red" || p.get("side") === "blue")
      setSide(p.get("side") as Side);
    if (["easy", "standard", "hard"].includes(p.get("difficulty") || ""))
      setDifficulty(p.get("difficulty")!);
  }, [arena.catalog]);
  useEffect(() => {
    if (
      arena.loading ||
      !arena.catalog ||
      window.location.hash !== "#saved-matches"
    )
      return;
    const frame = window.requestAnimationFrame(() =>
      focusActivity(
        document.getElementById("saved-matches"),
        window.matchMedia("(prefers-reduced-motion: reduce)").matches,
      ),
    );
    return () => window.cancelAnimationFrame(frame);
  }, [arena.loading, arena.catalog]);
  const heading = useActivityFocus(arena.opened);
  const m = arena.match;
  const selectedId = m?.assets.some((a) => a.id === selected)
    ? selected
    : m?.assets[0]?.id || "";
  return (
    <>
      <header className={`container ${styles.header}`}>
        <Link className="brand" href="/">
          EduCyber
        </Link>
        <nav aria-label="Learning navigation">
          <JourneyLink />
          <Link href="/cyber-lab">Cyber Lab</Link>
          <Link href="/learn">Courses</Link>
        </nav>
        <AccountNavigation showJourney={false} />
      </header>
      <main className={`container ${styles.main}`}>
        <div className={styles.hero}>
          <span className={styles.eyebrow}>
            RED / BLUE · STRATEGY SIMULATOR
          </span>
          <h1>
            One organisation.
            <br />
            Two competing decisions.
          </h1>
          <p>
            Study the evidence. Commit your plan. See how access, protection and
            business tradeoffs change a fictional incident.
          </p>
          <p className={styles.muted}>
            Conceptual learning only · no real systems or payloads · no external
            AI
          </p>
        </div>
        {arena.error && (
          <div className={styles.error} role="alert">
            {arena.error}{" "}
            <button
              disabled={arena.busy || arena.loading}
              onClick={() =>
                void (arena.match ? arena.refresh() : arena.initialize())
              }
            >
              Try loading again
            </button>
          </div>
        )}
        {arena.loading ? (
          <p role="status">Loading simulator…</p>
        ) : (
          arena.catalog && (
            <>
              <div className={styles.setupGrid}>
                <section className={styles.panel} aria-labelledby="new-match">
                  <h2 id="new-match">Start a match</h2>
                  <div className={styles.formGrid}>
                    <label>
                      Scenario
                      <select
                        aria-label="Scenario"
                        value={scenario}
                        onChange={(e) => setScenario(e.target.value)}
                      >
                        {arena.catalog.scenarios.map((s) => (
                          <option key={s.id} value={s.id}>
                            {s.title} · {s.difficulty}
                          </option>
                        ))}
                      </select>
                    </label>
                    <label>
                      Your seat
                      <select
                        aria-label="Your seat"
                        value={side}
                        onChange={(e) => setSide(e.target.value as Side)}
                      >
                        <option value="blue">
                          Blue · protect the organisation
                        </option>
                        <option value="red">Red · test the organisation</option>
                      </select>
                    </label>
                    <label>
                      Opponent
                      <select
                        aria-label="Opponent"
                        value={mode}
                        onChange={(e) => setMode(e.target.value)}
                      >
                        <option value="computer">Rule-based computer</option>
                        <option value="human">Another learner</option>
                      </select>
                    </label>
                    {mode === "computer" && (
                      <label>
                        Computer difficulty
                        <select
                          aria-label="Computer difficulty"
                          value={difficulty}
                          onChange={(e) => setDifficulty(e.target.value)}
                        >
                          <option value="easy">
                            Easy · scouting / basic hygiene
                          </option>
                          <option value="standard">
                            Standard · objectives / alert-led response
                          </option>
                          <option value="hard">
                            Hard · weaknesses / trust boundaries
                          </option>
                        </select>
                      </label>
                    )}
                  </div>
                  <p className={styles.muted}>
                    Equal finite budgets. Difficulty changes decisions, never
                    resources or hidden information. No clock runs while you
                    plan.
                  </p>
                  <button
                    className="btn"
                    disabled={arena.busy || arena.uncertain}
                    onClick={() =>
                      void arena.start(scenario, side, mode, difficulty)
                    }
                  >
                    Start match
                  </button>
                </section>
                <section className={styles.panel} aria-labelledby="join-match">
                  <h2 id="join-match">Join another learner</h2>
                  <p>
                    Ask the creator for a private, single-use invitation. Sign
                    in with your own student account in a separate browser
                    session.
                  </p>
                  <form
                    onSubmit={(e) => {
                      e.preventDefault();
                      void arena.join(token);
                    }}
                  >
                    <label htmlFor="invite-token">Invitation code</label>
                    <input
                      id="invite-token"
                      value={token}
                      onChange={(e) => setToken(e.target.value)}
                      autoComplete="off"
                      maxLength={43}
                      spellCheck={false}
                    />
                    <button
                      className="btn secondary"
                      disabled={
                        arena.busy ||
                        arena.uncertain ||
                        token.trim().length !== 43
                      }
                    >
                      Join match
                    </button>
                  </form>
                  <p className={styles.muted}>
                    Invitations expire after 24 hours. No instructor or
                    spectator access is enabled.
                  </p>
                </section>
              </div>
              {m && (
                <section
                  className={styles.workspace} data-side={m.side}
                  aria-label="Match workspace"
                  aria-busy={arena.busy}
                >
                  <div className={styles.matchHeading}>
                    <div>
                      <span className={styles.eyebrow}>
                        MATCH {m.id} · {m.side.toUpperCase()} SEAT ·{" "}
                        {m.mode === "computer"
                          ? m.difficulty.toUpperCase() + " COMPUTER"
                          : "HUMAN OPPONENT"}
                      </span>
                      <h2
                        tabIndex={-1}
                        className="activity-heading"
                        ref={heading}
                      >
                        {m.title}
                      </h2>
                    </div>
                    <button
                      disabled={arena.busy}
                      onClick={() => void arena.refresh()}
                    >
                      Refresh saved match
                    </button>
                  </div>
                  <div className={styles.stats} aria-label="Match resources">
                    <div>
                      <span>ROUND</span>
                      <strong>
                        {m.turn} / {m.turn_limit}
                      </strong>
                    </div>
                    <div>
                      <span>YOUR BUDGET</span>
                      <strong>{m.budget} credits</strong>
                    </div>
                    <div>
                      <span>ROUND CAP</span>
                      <strong>{m.action_points} AP</strong>
                    </div>
                    <div>
                      <span>STATUS</span>
                      <strong role="status">
                        {m.winner
                          ? m.winner.toUpperCase() + " wins"
                          : m.status === "waiting"
                            ? "Waiting for learner"
                            : m.committed
                              ? "Choice sealed"
                              : "Planning open"}
                      </strong>
                    </div>
                  </div>
                  <section className={styles.briefing}>
                    <h3>Your briefing</h3>
                    <p>{m.briefing}</p>
                    <p>
                      <strong>Red objective:</strong>{" "}
                      {m.objective.kind === "fraud"
                        ? "Alter records"
                        : m.objective.kind === "leak"
                          ? "Copy fictional data"
                          : "Keep critical service unavailable"}{" "}
                      with at least {m.objective.threshold} value
                      {m.objective.hold_turns > 1
                        ? " for " +
                          m.objective.hold_turns +
                          " consecutive rounds"
                        : ""}
                      . Blue wins by preventing this through round{" "}
                      {m.turn_limit}.
                    </p>
                    <p>
                      Isolation also costs service availability. Recovery cannot
                      undo historical leakage or fraud.
                    </p>
                  </section>
                  {m.status === "waiting" && (
                    <section className={styles.panel}>
                      <h3>Invite the second seat</h3>
                      <button
                        disabled={arena.busy}
                        onClick={() => void arena.createInvite()}
                      >
                        {arena.invite
                          ? "Replace invitation code"
                          : "Create invitation code"}
                      </button>
                      {arena.invite && (
                        <div className={styles.invitation}>
                          <label htmlFor="share-code">
                            Share this code privately
                          </label>
                          <input
                            id="share-code"
                            value={arena.invite.token}
                            readOnly
                            onFocus={(e) => e.target.select()}
                          />
                          <p>
                            Expires{" "}
                            {new Date(arena.invite.expires_at).toLocaleString()}
                            . Replacing it invalidates the previous code.
                          </p>
                        </div>
                      )}
                      <p className={styles.muted}>
                        This page checks for a joined learner every three
                        seconds while visible. You can resume from saved
                        matches.
                      </p>
                    </section>
                  )}
                  <div className={styles.playGrid}>
                    <AssetBoard
                      match={m}
                      selected={selectedId}
                      onSelect={setSelected}
                    />
                    <Planner
                      match={m}
                      actions={arena.catalog.actions}
                      selected={selectedId}
                      busy={arena.busy}
                      uncertain={arena.uncertain}
                      onSeal={(o) => void arena.seal(o)}
                    />
                  </div>
                  <section className={styles.panel}>
                    <h3>Your evidence ledger</h3>
                    <p className={styles.muted}>
                      Only evidence available to your seat appears here. An
                      alert is not confirmation of attacker success.
                    </p>
                    {m.observations.length ? (
                      <ol className={styles.ledger}>
                        {m.observations
                          .slice()
                          .reverse()
                          .map((o, i) => (
                            <li key={i}>
                              <strong>
                                Round {o.turn} · {o.type.replaceAll("_", " ")}
                              </strong>
                              {o.target
                                ? " · " +
                                  (m.assets.find((a) => a.id === o.target)
                                    ?.name || o.target)
                                : ""}
                              {o.action
                                ? " · " + o.action.replaceAll("_", " ")
                                : ""}
                              <p>{o.message}</p>
                            </li>
                          ))}
                      </ol>
                    ) : (
                      <p>No action evidence recorded yet.</p>
                    )}
                  </section>
                  {arena.debrief && <AfterAction result={arena.debrief} />}
                </section>
              )}
              <section className={styles.panel} aria-labelledby="saved-matches">
                <h2 id="saved-matches" tabIndex={-1}>
                  Your saved matches
                </h2>
                <p>
                  Each seat is bound to your account. Reconnect or sign in again
                  to resume.
                </p>
                <div className={styles.history}>
                  {arena.history.matches.map((row) => (
                    <button
                      key={row.id}
                      disabled={arena.busy || arena.uncertain}
                      onClick={() => void arena.resume(row.id)}
                    >
                      <strong>
                        Match {row.id} · {row.title}
                      </strong>
                      <span>
                        {row.side.toUpperCase()} · {row.status}
                      </span>
                      <span>Resume match {row.id} →</span>
                    </button>
                  ))}
                </div>
                {!arena.history.matches.length && <p>No saved matches yet.</p>}
                {arena.history.next_before_id && (
                  <button
                    disabled={arena.busy}
                    onClick={() => void arena.more()}
                  >
                    Load older matches
                  </button>
                )}
              </section>
              <section className={styles.panel} aria-labelledby="action-wiki">
                <h2 id="action-wiki">Action field guide</h2>
                <p>
                  These are simplified educational rules, not measured attack
                  probabilities or working attack instructions. Public ATT&CK
                  mappings explain the concepts.
                </p>
                {arena.catalog.actions.map((a) => (
                  <details key={a.id}>
                    <summary>
                      {a.side.toUpperCase()} · {a.id.replaceAll("_", " ")} ·{" "}
                      {a.cost} credits
                    </summary>
                    <p>{a.explanation}</p>
                    <p>
                      <strong>Prerequisites:</strong> {a.prerequisites}
                    </p>
                    <p>{a.rule}</p>
                    <a href={a.url} target="_blank" rel="noreferrer">
                      {a.technique} · {a.relation} MITRE ATT&CK ↗
                    </a>
                  </details>
                ))}
              </section>
            </>
          )
        )}
      </main>
    </>
  );
}
