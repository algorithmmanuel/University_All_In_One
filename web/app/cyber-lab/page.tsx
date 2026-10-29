"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import GameBoard from "./GameBoard";
import LessonTopic from "./LessonTopic";
import CampaignPanel from "./CampaignPanel";
import type {
  Catalog,
  CampaignStep,
  Run,
  RunPreview,
  Practice,
  PracticePreview,
} from "./types";
import styles from "./lab.module.css";
const API = (process.env.NEXT_PUBLIC_API_BASE_URL || "").replace(/\/$/, "");
class RequestError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
  }
}
type Pending = {
  command_id: string;
  expected_version: number;
  action: string;
  target?: string;
};

export default function CyberLab() {
  const router = useRouter();
  const [tab, setTab] = useState("play");
  const [catalog, setCatalog] = useState<Catalog | null>(null);
  const [run, setRun] = useState<Run | null>(null),
    [runs, setRuns] = useState<RunPreview[]>([]);
  const [runCursor, setRunCursor] = useState<number | null>(null);
  const [practice, setPractice] = useState<Practice | null>(null),
    [sessions, setSessions] = useState<PracticePreview[]>([]);
  const [practiceCursor, setPracticeCursor] = useState<number | null>(null);
  const [module, setModule] = useState("protect");
  const [scenario, setScenario] = useState("branch");
  const [practiceMode, setPracticeMode] = useState("fresh");
  const [topic, setTopic] = useState("all"),
    [difficulty, setDifficulty] = useState("all"),
    [count, setCount] = useState(10);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [busy, setBusy] = useState(false),
    [loading, setLoading] = useState(true),
    [error, setError] = useState("");
  const [retry, setRetry] = useState(false);
  const inFlight = useRef(false),
    pending = useRef<Pending | null>(null);
  const heading = useRef<HTMLHeadingElement>(null);
  const request = useCallback(
    async (path: string, method = "GET", data?: unknown) => {
      const token = sessionStorage.getItem("educyber_token");
      if (!token) {
        router.replace("/account");
        throw new RequestError("Please sign in to continue.", 401);
      }
      const response = await fetch(API + "/api/v1/cyber-lab" + path, {
        method,
        headers: {
          Authorization: "Bearer " + token,
          ...(data ? { "Content-Type": "application/json" } : {}),
        },
        ...(data ? { body: JSON.stringify(data) } : {}),
      });
      const body = await response.json();
      if (!response.ok) {
        if (response.status === 401) {
          sessionStorage.removeItem("educyber_token");
          router.replace("/account");
        }
        throw new RequestError(
          typeof body.detail === "string"
            ? body.detail
            : "Unable to complete this request.",
          response.status,
        );
      }
      return body;
    },
    [router],
  );
  const refresh = useCallback(async () => {
    const [c, r, p] = await Promise.all([
      request("/catalog"),
      request("/runs"),
      request("/practice"),
    ]);
    setCatalog(c);
    setRuns(r.runs);
    setRunCursor(r.next_before_id);
    setSessions(p.sessions);
    setPracticeCursor(p.next_before_id);
  }, [request]);
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (["play", "learn", "practice"].includes(params.get("tab") || ""))
      setTab(params.get("tab")!);
    if (params.get("module")) setModule(params.get("module")!);
    if (
      ["branch", "supplier", "ransomware", "siege"].includes(
        params.get("scenario") || "",
      )
    )
      setScenario(params.get("scenario")!);
    refresh()
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [refresh]);
  async function work(job: () => Promise<void>) {
    if (inFlight.current) return;
    inFlight.current = true;
    setBusy(true);
    setError("");
    try {
      await job();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Request failed. Try again.");
    } finally {
      inFlight.current = false;
      setBusy(false);
    }
  }
  function focusActivity() {
    requestAnimationFrame(() => {
      heading.current?.focus();
      heading.current?.scrollIntoView({ block: "start", behavior: "instant" });
    });
  }
  async function command(action: string, target?: string) {
    if (!run) return;
    await work(async () => {
      const body = pending.current ?? {
        command_id: crypto.randomUUID(),
        expected_version: run.version,
        action,
        ...(target ? { target } : {}),
      };
      pending.current = body;
      try {
        const next = await request(`/runs/${run.id}/commands`, "POST", body);
        setRun(next);
        pending.current = null;
        setRetry(false);
        if (next.status !== "active") await refresh();
      } catch (e) {
        if (e instanceof RequestError) {
          pending.current = null;
          setRetry(false);
        } else setRetry(true);
        throw e;
      }
    });
  }
  function campaignNext(step: CampaignStep) {
    if (step.kind === "learn") {
      setModule(step.module ?? "protect");
      setTab("learn");
      focusActivity();
    } else if (step.kind === "practice") {
      const supporting = catalog?.modules.find(
        (item) => item.id === step.module,
      );
      setTopic(supporting?.topics[0] ?? "all");
      setDifficulty("all");
      setPracticeMode("fresh");
      setCount(5);
      setPractice(null);
      setTab("practice");
      focusActivity();
    } else {
      setScenario(step.scenario ?? "branch");
      if (step.run_id)
        void work(async () => {
          setRun(await request("/runs/" + step.run_id));
          pending.current = null;
          setRetry(false);
          focusActivity();
        });
      else {
        setRun(null);
        pending.current = null;
        setRetry(false);
        focusActivity();
      }
    }
  }
  const selectedScenario = catalog?.scenarios?.find(
    (item) => item.id === scenario,
  );
  const eligibleCount = (catalog?.topics ?? [])
    .filter((item) => topic === "all" || item.id === topic)
    .reduce(
      (sum, item) =>
        sum +
        (practiceMode === "mistakes"
          ? (item.mistakes?.[difficulty] ?? 0)
          : difficulty === "all"
            ? item.count
            : (item.counts?.[difficulty] ?? 0)),
      0,
    );
  const sessionCount = Math.min(count, eligibleCount, 20);
  const selectedModule =
    catalog?.modules.find((m) => m.id === module) ?? catalog?.modules[0];
  return (
    <main className={styles.page}>
      <header className={styles.header}>
        <Link href="/dashboard">← Dashboard</Link>
        <Link href="/missions">Case-study missions</Link>
        <span>EDUCYBER / CYBER LAB</span>
      </header>
      <section className={styles.hero}>
        <span className={styles.eyebrow}>
          LEARN THE CONTROLS. MAKE THE CALL.
        </span>
        <h1>Cybersecurity in motion.</h1>
        <p>
          Defend a fictional branch, build your knowledge and practise across{" "}
          {catalog?.question_count ?? 500} cybersecurity questions.
        </p>
        <div
          className={styles.tabs}
          role="group"
          aria-label="Cyber lab sections"
        >
          {["play", "learn", "practice"].map((t) => (
            <button
              key={t}
              aria-pressed={tab === t}
              onClick={() => {
                setTab(t);
                focusActivity();
              }}
            >
              {t === "play"
                ? "01 / Play"
                : t === "learn"
                  ? "02 / Learn"
                  : "03 / Practise"}
            </button>
          ))}
        </div>
      </section>
      {error && (
        <div className={styles.error} role="alert">
          <p>{error}</p>
          {retry ? (
            <button disabled={busy} onClick={() => void command("end_turn")}>
              Retry the same saved command
            </button>
          ) : (
            <button disabled={busy} onClick={() => void work(refresh)}>
              Reload activity lists
            </button>
          )}
        </div>
      )}
      {loading ? (
        <p role="status">Loading your cyber lab…</p>
      ) : !catalog ? (
        <button onClick={() => void work(refresh)} disabled={busy}>
          Retry cyber lab
        </button>
      ) : (
        <>
          <h2 ref={heading} tabIndex={-1} className={styles.sectionHeading}>
            {tab === "play"
              ? "Your shift"
              : tab === "learn"
                ? "Cybersecurity learning modules"
                : "Cybersecurity practice"}
          </h2>
          {tab === "play" && (
            <>
              {!run && catalog.campaign && (
                <CampaignPanel
                  campaign={catalog.campaign}
                  busy={busy}
                  onNext={campaignNext}
                />
              )}
              {!run && (
                <div className={styles.launch}>
                  <div>
                    <span className={styles.eyebrow}>
                      CHOOSE YOUR NEXT SHIFT
                    </span>
                    <h2>
                      Operation Firewall:
                      <br />
                      {selectedScenario?.title ?? "Defend the branch"}
                    </h2>
                    <p>
                      Six assets. A limited budget. An incident that changes
                      with your decisions.
                    </p>
                    <p>
                      Deploy controls, investigate alerts, contain spread and
                      recover services. The opponent uses fictional programmed
                      rules. Pause between turns and resume whenever you need.
                    </p>
                    <label className={styles.scenarioChoice}>
                      Scenario
                      <select
                        aria-label="Scenario"
                        value={scenario}
                        onChange={(e) => setScenario(e.target.value)}
                      >
                        {catalog.scenarios.map((item) => (
                          <option key={item.id} value={item.id}>
                            {item.title} · {item.difficulty}
                          </option>
                        ))}
                      </select>
                    </label>
                    <p>{selectedScenario?.summary}</p>
                    <button
                      className={styles.primary}
                      disabled={busy}
                      onClick={() =>
                        void work(async () => {
                          setRun(await request("/runs", "POST", { scenario }));
                          pending.current = null;
                          setRetry(false);
                          await refresh();
                          focusActivity();
                        })
                      }
                    >
                      Start a new shift →
                    </button>
                  </div>
                  <div className={styles.launchArt} aria-hidden="true">
                    <span>◈</span>
                    <strong>
                      BRANCH
                      <br />
                      {scenario === "siege" ? "SIEGE" : "DEFENDER"}
                    </strong>
                    <small>PROTECT / DETECT / RESPOND / RECOVER</small>
                  </div>
                </div>
              )}
              {run && (
                <>
                  <button
                    className={styles.back}
                    disabled={busy}
                    onClick={() => {
                      setRun(null);
                      pending.current = null;
                      setRetry(false);
                      void work(refresh);
                    }}
                  >
                    ← Saved shifts
                  </button>
                  <GameBoard
                    key={run.id}
                    run={run}
                    busy={busy || retry}
                    onAction={(a, t) => void command(a, t)}
                    onReplay={() =>
                      void work(async () => {
                        setRun(
                          await request("/runs", "POST", {
                            scenario: "siege",
                            replay_run_id: run.id,
                          }),
                        );
                        pending.current = null;
                        setRetry(false);
                        await refresh();
                        focusActivity();
                      })
                    }
                    onReload={() =>
                      void work(async () => {
                        setRun(await request("/runs/" + run.id));
                        pending.current = null;
                        setRetry(false);
                      })
                    }
                  />
                  {retry && (
                    <button
                      onClick={() =>
                        void work(async () => {
                          setRun(await request("/runs/" + run.id));
                          pending.current = null;
                          setRetry(false);
                        })
                      }
                    >
                      Reload run after connection failure
                    </button>
                  )}
                </>
              )}
              {!run && (
                <section className={styles.saved}>
                  <h3>Saved shifts</h3>
                  <p>
                    Your current and completed shifts remain available here.
                  </p>
                  {runs.length === 0 ? (
                    <p>No saved shifts yet.</p>
                  ) : (
                    <div className={styles.savedGrid}>
                      {runs.map((r) => (
                        <button
                          key={r.id}
                          disabled={busy}
                          onClick={() =>
                            void work(async () => {
                              setRun(await request("/runs/" + r.id));
                              focusActivity();
                            })
                          }
                        >
                          <strong>Shift #{r.id}</strong>
                          <span>{r.title ?? "Defend the branch"}</span>
                          <span>
                            Turn {r.turn} · {r.status}
                          </span>
                          <small>
                            {r.status === "active"
                              ? "Resume shift →"
                              : "Open debrief →"}
                          </small>
                        </button>
                      ))}
                    </div>
                  )}
                  {runCursor && (
                    <button
                      disabled={busy}
                      onClick={() =>
                        void work(async () => {
                          const p = await request(
                            "/runs?before_id=" + runCursor,
                          );
                          setRuns((old) => [...old, ...p.runs]);
                          setRunCursor(p.next_before_id);
                        })
                      }
                    >
                      Older shifts
                    </button>
                  )}
                </section>
              )}
            </>
          )}
          {tab === "learn" && (
            <div className={styles.studyLayout}>
              <nav aria-label="Learning modules">
                {catalog.modules.map((m) => (
                  <button
                    key={m.id}
                    aria-pressed={selectedModule?.id === m.id}
                    onClick={() => {
                      setModule(m.id);
                      focusActivity();
                    }}
                  >
                    {m.completed ? "✓ " : ""}
                    {m.title}
                  </button>
                ))}
              </nav>
              {selectedModule && (
                <article className={styles.lesson} key={selectedModule.id}>
                  <span className={styles.eyebrow}>
                    {selectedModule.revision}
                  </span>
                  <h2>{selectedModule.title}</h2>
                  {selectedModule.previously_completed &&
                    !selectedModule.completed && (
                      <p className={styles.callout}>
                        You completed an earlier edition. Your previous record
                        is preserved; review the new material before marking
                        this edition complete.
                      </p>
                    )}
                  <p className={styles.callout}>
                    <strong>Worked incident: </strong>
                    {selectedModule.example}
                  </p>
                  {selectedModule.sections.map((section) => (
                    <LessonTopic
                      key={selectedModule.revision + section.id}
                      section={section}
                      onPractice={() => {
                        setTopic(section.id);
                        setCount(5);
                        setDifficulty("all");
                        setPracticeMode("fresh");
                        setTab("practice");
                        setPractice(null);
                        focusActivity();
                      }}
                    />
                  ))}
                  <div className={styles.callout}>
                    <h3>Apply it in the game</h3>
                    <p>{selectedModule.game}</p>
                    <button onClick={() => setTab("play")}>
                      Go to Branch Defender →
                    </button>
                  </div>
                  <button
                    className={styles.primary}
                    disabled={busy || selectedModule.completed}
                    onClick={() =>
                      void work(async () => {
                        await request(
                          "/study/" + selectedModule.id + "/complete",
                          "POST",
                        );
                        await refresh();
                      })
                    }
                  >
                    {selectedModule.completed
                      ? "Module completed ✓"
                      : "Mark module complete"}
                  </button>
                  <p className={styles.muted}>
                    Completion records that you marked this module read; it does
                    not certify mastery.
                  </p>
                </article>
              )}
            </div>
          )}
          {tab === "practice" && (
            <section className={styles.practice}>
              {!practice ? (
                <>
                  <p>
                    Select a topic and difficulty, or use a mixed session. Fresh
                    selections prioritise questions you have not recently seen.
                    Questions repeat when the eligible pool is exhausted.
                  </p>
                  <form
                    onSubmit={(e) => {
                      e.preventDefault();
                      void work(async () => {
                        setPractice(
                          await request("/practice", "POST", {
                            topic,
                            difficulty,
                            mode: practiceMode,
                            count: sessionCount,
                          }),
                        );
                        setAnswers({});
                        await refresh();
                        focusActivity();
                      });
                    }}
                    className={styles.practiceControls}
                  >
                    <label>
                      Practice mode
                      <select
                        aria-label="Practice mode"
                        value={practiceMode}
                        onChange={(e) => setPracticeMode(e.target.value)}
                      >
                        <option value="fresh">Fresh practice</option>
                        <option value="mistakes">Review recent mistakes</option>
                      </select>
                    </label>
                    <label>
                      Topic
                      <select
                        aria-label="Topic"
                        value={topic}
                        onChange={(e) => setTopic(e.target.value)}
                      >
                        <option value="all">Mixed topics</option>
                        {catalog.topics.map((t) => (
                          <option key={t.id} value={t.id}>
                            {t.title} ({t.count})
                          </option>
                        ))}
                      </select>
                    </label>
                    <label>
                      Difficulty
                      <select
                        aria-label="Difficulty"
                        value={difficulty}
                        onChange={(e) => setDifficulty(e.target.value)}
                      >
                        <option value="all">All difficulties</option>
                        <option value="foundational">Foundational</option>
                        <option value="applied">Applied</option>
                        <option value="challenging">Challenging</option>
                      </select>
                    </label>
                    <label>
                      Questions
                      <input
                        type="number"
                        min={1}
                        max={Math.max(1, Math.min(20, eligibleCount))}
                        value={sessionCount || 1}
                        onChange={(e) => setCount(Number(e.target.value))}
                      />
                    </label>
                    <p role="status">
                      {eligibleCount} eligible questions
                      {practiceMode === "mistakes"
                        ? " from the latest graded verdicts within your last 50 submitted sessions"
                        : ""}
                      .{" "}
                      {eligibleCount === 0
                        ? "Choose another topic or complete practice first."
                        : ""}
                    </p>
                    <button
                      className={styles.primary}
                      disabled={busy || eligibleCount === 0}
                    >
                      Start practice →
                    </button>
                  </form>
                  <h3>Saved practice</h3>
                  {sessions.length === 0 ? (
                    <p>No saved sessions.</p>
                  ) : (
                    <div className={styles.savedGrid}>
                      {sessions.map((p) => (
                        <button
                          key={p.id}
                          disabled={busy}
                          onClick={() =>
                            void work(async () => {
                              setPractice(await request("/practice/" + p.id));
                              setAnswers({});
                              focusActivity();
                            })
                          }
                        >
                          <strong>Practice #{p.id}</strong>
                          <span>
                            {p.completed
                              ? `${p.score}/${p.count} · Open results`
                              : `${p.count} questions · Resume`}
                          </span>
                        </button>
                      ))}
                    </div>
                  )}
                  {practiceCursor && (
                    <button
                      disabled={busy}
                      onClick={() =>
                        void work(async () => {
                          const p = await request(
                            "/practice?before_id=" + practiceCursor,
                          );
                          setSessions((old) => [...old, ...p.sessions]);
                          setPracticeCursor(p.next_before_id);
                        })
                      }
                    >
                      Older practice
                    </button>
                  )}
                </>
              ) : (
                <>
                  <button
                    onClick={() => {
                      setPractice(null);
                      void work(refresh);
                    }}
                  >
                    ← Practice sessions
                  </button>
                  <h3>Practice #{practice.id}</h3>
                  {practice.result ? (
                    <>
                      <h2>
                        {practice.result.score} / {practice.result.total}
                      </h2>
                      <p>{practice.result.notice}</p>
                      {practice.result.feedback.map((f) => (
                        <article key={f.id} className={styles.feedback}>
                          <span>
                            {f.correct ? "✓ Correct" : "Review this decision"}
                          </span>
                          <h3>{f.prompt}</h3>
                          <p>Your answer: {f.selected}</p>
                          <p>
                            <strong>Expected: {f.expected}</strong>
                          </p>
                          <p>{f.explanation}</p>
                          <button
                            onClick={() => {
                              setModule(f.module);
                              setTab("learn");
                            }}
                          >
                            Review the supporting module
                          </button>
                          <p>
                            <a
                              href={f.source.url}
                              target="_blank"
                              rel="noopener noreferrer"
                            >
                              Further reading: {f.source.title} ↗
                            </a>
                          </p>
                        </article>
                      ))}
                    </>
                  ) : (
                    <form
                      onSubmit={(e) => {
                        e.preventDefault();
                        void work(async () => {
                          setPractice(
                            await request(
                              "/practice/" + practice.id + "/submit",
                              "POST",
                              { answers },
                            ),
                          );
                          await refresh();
                          focusActivity();
                        });
                      }}
                    >
                      <p role="status">
                        {Object.keys(answers).length} of{" "}
                        {practice.questions.length} answered
                      </p>
                      <progress
                        aria-label="Practice answers selected"
                        max={practice.questions.length}
                        value={Object.keys(answers).length}
                      />
                      <p>
                        Selected questions are saved. Unsubmitted answer choices
                        stay in this page only; reopening starts those choices
                        again.
                      </p>
                      {practice.questions.map((q, i) => (
                        <fieldset
                          key={q.id}
                          className={styles.question}
                          disabled={busy}
                        >
                          <legend>
                            {i + 1}. {q.prompt}
                          </legend>
                          {q.options.map((option, index) => (
                            <label key={index}>
                              <input
                                type="radio"
                                name={q.id}
                                checked={answers[q.id] === index}
                                onChange={() =>
                                  setAnswers((old) => ({
                                    ...old,
                                    [q.id]: index,
                                  }))
                                }
                              />
                              {option}
                            </label>
                          ))}
                        </fieldset>
                      ))}
                      <button
                        className={styles.primary}
                        disabled={
                          busy ||
                          Object.keys(answers).length !==
                            practice.questions.length
                        }
                      >
                        Submit practice answers
                      </button>
                    </form>
                  )}
                </>
              )}
            </section>
          )}
        </>
      )}
    </main>
  );
}
