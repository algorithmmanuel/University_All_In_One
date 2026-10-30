"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import JourneyLink from "../../components/journey/JourneyLink";
import { AccountNavigation } from "../../components/home/account-navigation";
import { focusActivity } from "../../lib/activity-focus";
import { useActivityFocus } from "../../lib/use-activity-focus";
import { STAGES, AUDIENCES, workshopBelongsTo, type Audience } from "../../lib/learning-journey";
import styles from "./workshops.module.css";
type Case = {
  id: string;
  title: string;
  stage: string;
  briefing: string;
  objective: string;
};
type RecordItem = {
  prompt: string;
  step: number;
  label: string;
  explanation: string;
  effort: number;
  fact: string | null;
};
type Summary = { effort: number; findings: string[]; unresolved: string[] };
type Run = Omit<Case, "id"> &
  Summary & {
    id: number;
    case_id: string;
    step_index: number;
    completed: boolean;
    recap: RecordItem[];
    baseline: Summary | null;
    notice: string;
    step: null | {
      prompt: string;
      context: string;
      choices: { id: "a" | "b"; label: string; effort: number }[];
    };
  };
type Preview = {
  id: number;
  title: string;
  case_id: string;
  stage: string;
  completed: boolean;
  step_index: number;
};
type Command = {
  command_id: string;
  expected_step: number;
  choice_id: "a" | "b";
};
class RequestError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
  }
}
const API = (process.env.NEXT_PUBLIC_API_BASE_URL || "").replace(/\/$/, "");
export default function Workshops() {
  const router = useRouter();
  const [audience, setAudience] = useState<Audience>("all");
  const [cases, setCases] = useState<Case[]>([]),
    [filter, setFilter] = useState("all"),
    [chosen, setChosen] = useState("");
  const [run, setRun] = useState<Run | null>(null),
    [history, setHistory] = useState<Preview[]>([]),
    [cursor, setCursor] = useState<number | null>(null);
  const [busy, setBusy] = useState(false),
    [loading, setLoading] = useState(true),
    [error, setError] = useState(""),
    [uncertain, setUncertain] = useState(false),
    [opened, setOpened] = useState(0);
  const pending = useRef<Command | null>(null),
    inFlight = useRef(false);
  const heading = useActivityFocus(opened);
  const decisionHeading = useRef<HTMLHeadingElement>(null);
  const previousStep = useRef<{ id: number; step: number } | null>(null);
  useEffect(() => {
    const previous = previousStep.current;
    previousStep.current = run ? { id: run.id, step: run.step_index } : null;
    if (!run || previous?.id !== run.id || run.step_index <= previous.step)
      return;
    const frame = window.requestAnimationFrame(() =>
      focusActivity(
        decisionHeading.current,
        window.matchMedia("(prefers-reduced-motion: reduce)").matches,
      ),
    );
    return () => window.cancelAnimationFrame(frame);
  }, [run?.id, run?.step_index]);

  const request = useCallback(
    async <T,>(path: string, data?: unknown): Promise<T> => {
      const token = sessionStorage.getItem("educyber_token");
      if (path != "/catalog" && !token) {
        router.replace("/account");
        throw new RequestError(
          "Sign in with a learner account to save this workshop.",
          401,
        );
      }
      const r = await fetch(API + "/api/v1/workshops" + path, {
        method: data === undefined ? "GET" : "POST",
        cache: "no-store",
        headers: {
          ...(token ? { Authorization: "Bearer " + token } : {}),
          ...(data === undefined ? {} : { "Content-Type": "application/json" }),
        },
        ...(data === undefined ? {} : { body: JSON.stringify(data) }),
      });
      const b = await r.json();
      if (!r.ok) {
        if (r.status === 401) {
          sessionStorage.removeItem("educyber_token");
          router.replace("/account");
        }
        throw new RequestError(
          typeof b.detail === "string"
            ? b.detail
            : "Workshop request could not be completed.",
          r.status,
        );
      }
      return b;
    },
    [router],
  );
  const loadHistory = useCallback(
    async (before?: number) => {
      if (!sessionStorage.getItem("educyber_token")) return;
      const p = await request<{
        runs: Preview[];
        next_before_id: number | null;
      }>("/runs" + (before ? "?before_id=" + before : ""));
      setHistory((old) => (before ? [...old, ...p.runs] : p.runs));
      setCursor(p.next_before_id);
    },
    [request],
  );
  const initialize = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const c = await request<{ cases: Case[] }>("/catalog");
      setCases(c.cases);
      const p = new URLSearchParams(window.location.search);
      const rawPath = p.get("journey_pathway") || p.get("pathway");
      const path: Audience = AUDIENCES.find(a => a.id === rawPath)?.id || "all";
      setAudience(path);
      const visible = c.cases.filter(c => workshopBelongsTo(c.id, path));
      const stage = p.get("stage");
      if (STAGES.some((s) => s.id === stage)) setFilter(stage!);
      const selected = visible.find((c) => c.id === p.get("case"));
      setFilter(
        selected?.stage ||
          (STAGES.some((s) => s.id === stage) ? stage! : "all"),
      );
      setChosen(
        selected?.id ||
          visible.find((c) => c.stage === stage)?.id ||
          visible[0]?.id || "",
      );
      await loadHistory();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  }, [request, loadHistory]);
  useEffect(() => {
    void initialize();
  }, [initialize]);
  async function work(job: () => Promise<void>) {
    if (inFlight.current) return;
    inFlight.current = true;
    setBusy(true);
    setError("");
    try {
      await job();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      inFlight.current = false;
      setBusy(false);
    }
  }
  function show(m: Run) {
    setRun(m);
    pending.current = null;
    setUncertain(false);
    setOpened((n) => n + 1);
  }
  async function start(replay = false) {
    await work(async () => {
      show(
        await request<Run>("/runs", {
          case_id: replay ? run!.case_id : chosen,
          ...(replay ? { replay_of: run!.id } : {}),
        }),
      );
      await loadHistory();
    });
  }
  async function resume(id: number) {
    await work(async () => {
      show(await request<Run>("/runs/" + id));
    });
  }
  async function refresh() {
    if (!run) return;
    await work(async () => {
      const m = await request<Run>("/runs/" + run.id);
      setRun(m);
      if (pending.current && m.step_index > pending.current.expected_step) {
        pending.current = null;
        setUncertain(false);
      }
      await loadHistory();
    });
  }
  async function decide(choice?: "a" | "b") {
    if (!run) return;
    await work(async () => {
      if (!pending.current && choice)
        pending.current = {
          command_id: crypto.randomUUID(),
          expected_step: run.step_index,
          choice_id: choice,
        };
      if (!pending.current) return;
      try {
        const m = await request<Run>(
          "/runs/" + run.id + "/decisions",
          pending.current,
        );
        setRun(m);
        pending.current = null;
        setUncertain(false);
      } catch (e) {
        if (e instanceof RequestError && e.status < 500) {
          pending.current = null;
          setUncertain(false);
          if (e.status === 409) setRun(await request<Run>("/runs/" + run.id));
        } else setUncertain(true);
        throw e;
      }
    });
  }
  useEffect(() => {
    if (run) void loadHistory().catch((e) => setError(e.message));
  }, [run?.id, run?.step_index, loadHistory]);
  const selected = cases.find((c) => c.id === chosen);
  return (
    <>
      <header className={`container ${styles.header}`}>
        <Link className="brand" href="/">
          EduCyber
        </Link>
        <JourneyLink />
        <AccountNavigation showJourney={false} />
      </header>
      <main className={`container ${styles.main}`}>
        <span className="tag">EVIDENCE · DECISIONS · CONSEQUENCES</span>
        <h1>Decision workshop library</h1>
        <p>
          Explore 24 authored cases across the eight journey stages. Each
          contains three decisions, explanations and saved replay comparison.
          Full strategy games remain available in Cyber Lab and Red / Blue.
        </p>
        {error && (
          <div className={styles.error} role="alert">
            {error}{" "}
            <button
              className="btn secondary"
              disabled={busy}
              onClick={() => void (run ? refresh() : initialize())}
            >
              Refresh saved activities
            </button>
          </div>
        )}
        {loading ? (
          <p role="status">Loading workshops…</p>
        ) : (
          <section className={styles.panel}>
            <h2>Choose a case</h2>
            {audience !== "all" && <p role="status">Showing the eight cases allocated to {AUDIENCES.find(a => a.id === audience)!.title}. <button type="button" className="btn secondary" onClick={() => setAudience("all")}>Browse all workshops</button></p>}
            <label>
              Journey stage
              <select
                aria-label="Workshop stage"
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
              >
                <option value="all">All stages</option>
                {STAGES.map((s, i) => (
                  <option key={s.id} value={s.id}>
                    {i + 1}. {s.title}
                  </option>
                ))}
              </select>
            </label>
            <div className={styles.caseGrid}>
              {cases
                .filter((c) => workshopBelongsTo(c.id, audience) && (filter === "all" || c.stage === filter))
                .map((c) => (
                  <button
                    key={c.id}
                    aria-pressed={chosen === c.id}
                    disabled={busy || uncertain}
                    onClick={() => setChosen(c.id)}
                  >
                    <span>{STAGES.find((s) => s.id === c.stage)?.title}</span>
                    <strong>{c.title}</strong>
                  </button>
                ))}
            </div>
            {selected && (
              <>
                <h3>{selected.title}</h3>
                <p>{selected.briefing}</p>
                <p>{selected.objective}</p>
                <button
                  className="btn"
                  disabled={busy || uncertain}
                  onClick={() => void start()}
                >
                  Start saved workshop
                </button>
              </>
            )}
          </section>
        )}
        {run && (
          <section
            className={styles.panel}
            aria-label="Workshop workspace"
            aria-busy={busy}
          >
            <div className={styles.row}>
              <div>
                <span className="tag">
                  WORKSHOP {run.id} · {run.step_index} / 3 DECISIONS
                </span>
                <h2 ref={heading} tabIndex={-1} className="activity-heading">
                  {run.title}
                </h2>
              </div>
              <button
                className="btn secondary"
                disabled={busy}
                onClick={() => void refresh()}
              >
                Refresh workshop
              </button>
            </div>
            <p>{run.briefing}</p>
            <dl className={styles.metrics}>
              <div>
                <dt>Supported findings</dt>
                <dd>{run.findings.length}</dd>
              </div>
              <div>
                <dt>Unresolved decisions</dt>
                <dd>{run.unresolved.length}</dd>
              </div>
              <div>
                <dt>Effort used</dt>
                <dd>{run.effort}</dd>
              </div>
            </dl>
            <p className="small">{run.notice}</p>
            {run.step ? (
              <section
                className={styles.decision}
                aria-labelledby="decision-heading"
              >
                <h3 id="decision-heading" ref={decisionHeading} tabIndex={-1}>
                  Decision {run.step_index + 1}: {run.step.prompt}
                </h3>
                <p>{run.step.context}</p>
                {run.recap.length > 0 && (
                  <p className={styles.lastEvidence}>
                    <strong>Latest case consequence:</strong>{" "}
                    {run.recap[run.recap.length - 1].explanation}
                  </p>
                )}
                <div className={styles.choices}>
                  {run.step.choices.map((c) => (
                    <button
                      disabled={busy || uncertain}
                      key={c.id}
                      onClick={() => void decide(c.id)}
                    >
                      {c.label}
                      <small>
                        {c.effort} effort unit{c.effort === 1 ? "" : "s"}
                      </small>
                    </button>
                  ))}
                </div>
              </section>
            ) : (
              <section aria-labelledby="review-heading">
                <h3 id="review-heading" ref={decisionHeading} tabIndex={-1}>
                  Your case review
                </h3>
                <p>
                  Review supported findings and unresolved decisions before
                  trying another approach. Finishing a case does not establish a
                  clean real-world system or professional competence.
                </p>
                {run.unresolved.length > 0 ? (
                  <ul>
                    {run.unresolved.map((text, i) => (
                      <li key={i}>{text}</li>
                    ))}
                  </ul>
                ) : (
                  <p>
                    Each decision collected a supported finding in this authored
                    case. Consider where the same reasoning would need more
                    evidence in a real environment.
                  </p>
                )}
                {run.baseline && (
                  <div className={styles.comparison}>
                    <h4>Compared with your previous approach</h4>
                    <table>
                      <thead>
                        <tr>
                          <th>Recorded measure</th>
                          <th>Previous</th>
                          <th>This run</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <th>Supported findings</th>
                          <td>{run.baseline.findings.length}</td>
                          <td>{run.findings.length}</td>
                        </tr>
                        <tr>
                          <th>Unresolved decisions</th>
                          <td>{run.baseline.unresolved.length}</td>
                          <td>{run.unresolved.length}</td>
                        </tr>
                        <tr>
                          <th>Effort units</th>
                          <td>{run.baseline.effort}</td>
                          <td>{run.effort}</td>
                        </tr>
                      </tbody>
                    </table>
                    <p>
                      Compare the reasoning and case effects as well as the
                      counts; fewer effort units alone is not a better outcome.
                    </p>
                  </div>
                )}
                <button
                  className="btn"
                  disabled={busy}
                  onClick={() => void start(true)}
                >
                  Replay and compare another approach
                </button>
              </section>
            )}
            {uncertain && (
              <div role="status">
                <p>
                  The response was interrupted. Refresh saved state or retry the
                  same request safely.
                </p>
                <button
                  className="btn"
                  disabled={busy}
                  onClick={() => void decide()}
                >
                  Retry same decision
                </button>
              </div>
            )}
            <h3>Decision ledger</h3>
            {run.recap.length ? (
              <ol className={styles.ledger}>
                {run.recap.map((r) => (
                  <li key={r.step}>
                    <h4>{r.prompt}</h4>
                    <p>
                      <strong>You chose:</strong> {r.label}
                    </p>
                    <p>{r.explanation}</p>
                    <p>
                      {r.fact
                        ? "Supported finding recorded."
                        : "Unresolved decision to revisit."}{" "}
                      Effort: {r.effort}.
                    </p>
                  </li>
                ))}
              </ol>
            ) : (
              <p>Your recorded choices and explanations will appear here.</p>
            )}
            <nav className={styles.row} aria-label="Continue learning">
              <JourneyLink />
              <Link href="/cyber-lab">Full defender simulations</Link>
              <Link href="/red-blue">Red / Blue simulator</Link>
              <Link
                href={
                  "/feedback?page=" +
                  encodeURIComponent(
                    "/workshops?case=" +
                      run.case_id +
                      "&run=" +
                      run.id +
                      "&step=" +
                      run.step_index,
                  )
                }
              >
                Report this workshop experience
              </Link>
            </nav>
          </section>
        )}
        <section className={styles.panel}>
          <h2>Your saved workshops</h2>
          <p>
            Refresh the list after an interrupted start before creating another
            attempt.
          </p>
          <button
            className="btn secondary"
            disabled={busy}
            onClick={() => void work(() => loadHistory())}
          >
            Refresh workshop history
          </button>
          <div className={styles.caseGrid}>
            {history.map((r) => (
              <button
                disabled={busy || uncertain}
                key={r.id}
                onClick={() => void resume(r.id)}
              >
                <strong>{r.title}</strong>
                <span>
                  {r.completed
                    ? "Review completed case"
                    : `Resume decision ${r.step_index + 1}`}{" "}
                  · workshop {r.id}
                </span>
              </button>
            ))}
          </div>
          {history.length === 0 && (
            <p>
              No saved workshops loaded. Sign in with an eligible student
              account to save your playthrough.
            </p>
          )}
          {cursor && (
            <button
              className="btn secondary"
              disabled={busy}
              onClick={() => void work(() => loadHistory(cursor))}
            >
              Load older workshops
            </button>
          )}
        </section>
      </main>
    </>
  );
}
