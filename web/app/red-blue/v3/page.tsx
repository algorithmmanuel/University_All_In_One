"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import styles from "./v3.module.css";
import V3Topology from "./V3Topology";

type Side = "blue" | "red";
type Action = { action: string; target: string | null; source: string | null; cost: number };
type Asset = {
  id: string; name: string; kind: string; exposed: boolean;
  value?: number; business_value?: number | null;
  controls?: string[]; weaknesses?: string[]; isolated?: boolean; disrupted?: boolean;
  zone?: string; patch_age_days?: number;
  knowledge?: string; observed_at?: number | null; assessment?: {
    weaknesses: string[]; controls: string[];
    zone?: string; estimated_patch_age_days?: number;
  } | null; believed_access?: number;
};
type Evidence = { sequence: number; kind: string; target?: string | null; message: string };
type Clock = {
  state: string; active_side: Side; turn_sequence: number;
  match_deadline_at: number; turn_deadline_at: number;
  match_seconds_remaining: number; turn_seconds_remaining: number;
};
type Match = {
  id: number; side: Side; phase: "prepare" | "engage" | "finished";
  version: number; mode: "computer" | "human"; prepared: Record<Side, boolean>;
  match_minutes: number; turn_seconds: number; assets: Asset[];
  connections: {source:string;target:string}[];
  credits: number; evidence: Evidence[]; offers: Action[];
  policies?: string[];
  discovery_hint?: string; strategy?: string; clock?: Clock;
  winner?: Side | null; reason?: string | null;
  score?: {blue_score:number;red_score:number;service_value_unavailable:number;foothold_value_confirmed:number;note:string} | null;
};
type History = { matches: {id: number; status: string; side: Side; mode: string}[] };
const API = (process.env.NEXT_PUBLIC_API_BASE_URL || "").replace(/\/$/, "") +
  "/api/v1/red-blue-v3";
const fmt = (seconds: number) => {
  const remaining = Math.max(0, Math.floor(seconds));
  return String(Math.floor(remaining / 60)).padStart(2, "0") + ":" +
    String(remaining % 60).padStart(2, "0");
};

export default function AdvancedMicrofinance() {
  const router = useRouter();
  const [loaded, setLoaded] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [history, setHistory] = useState<History>({ matches: [] });
  const [match, setMatch] = useState<Match | null>(null);
  const [side, setSide] = useState<Side>("blue");
  const [mode, setMode] = useState<"computer" | "human">("computer");
  const [minutes, setMinutes] = useState(30);
  const [turnSeconds, setTurnSeconds] = useState(90);
  const [invite, setInvite] = useState("");
  const [joinCode, setJoinCode] = useState("");
  const [selected, setSelected] = useState("");
  const [inspect, setInspect] = useState(false);
  const [inspectionTab, setInspectionTab] = useState<"issues" | "controls" | "activity">("issues");
  const [presentation, setPresentation] = useState<"learning" | "realistic">("learning");
  const [clockStarted, setClockStarted] = useState(Date.now());
  const [tick, setTick] = useState(0);
  const [chosen, setChosen] = useState("");
  const inFlight = useRef(false);

  const request = useCallback(async <T,>(path: string, body?: unknown): Promise<T> => {
    const token = sessionStorage.getItem("educyber_token");
    if (!token) { router.replace("/account"); throw new Error("Sign in first."); }
    const response = await fetch(API + path, {
      method: body === undefined ? "GET" : "POST",
      cache: "no-store",
      headers: { Authorization: "Bearer " + token,
        ...(body === undefined ? {} : { "Content-Type": "application/json" }) },
      ...(body === undefined ? {} : {body: JSON.stringify(body)}),
    });
    const data = await response.json();
    if (!response.ok) {
      if (response.status === 401) router.replace("/account");
      throw new Error(typeof data.detail === "string" ? data.detail : "Request unavailable.");
    }
    return data as T;
  }, [router]);
  const refreshHistory = useCallback(async () => {
    setHistory(await request<History>("/matches"));
  }, [request]);
  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        await request("/catalog");
        if (cancelled) return;
        await refreshHistory();
        if (!cancelled) setLoaded(true);
      } catch (e) { if (!cancelled) {setError((e as Error).message);setLoaded(true);} }
    })();
    return () => {cancelled = true;};
  }, [request, refreshHistory]);
  useEffect(() => {
    if (!match || match.phase === "finished") return;
    let cancelled = false;
    const id = match.id;
    const interval = window.setInterval(async () => {
      if (document.visibilityState !== "visible" || inFlight.current) return;
      try {
        const updated = await request<Match>("/matches/" + id);
        if (!cancelled) {
          setMatch(old => !old || old.id !== id || updated.version < old.version ? old : updated);
          setClockStarted(Date.now());
        }
      } catch (e) { if (!cancelled) setError((e as Error).message); }
    }, 3000);
    return () => {cancelled = true;window.clearInterval(interval);};
  }, [match?.id, match?.phase, request]);
  useEffect(() => {
    const timer = window.setInterval(() => setTick(n => n + 1), 1000);
    return () => window.clearInterval(timer);
  }, []);
  useEffect(() => {
    if (!inspect) return;
    const handler = (event: KeyboardEvent) => {
      if (event.key === "Escape") setInspect(false);
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [inspect]);
  const setUpdated = (updated: Match) => {
    setMatch(updated);
    setClockStarted(Date.now());
    setChosen("");
    setSelected(old => updated.assets.some(a => a.id === old) ? old : updated.assets[0]?.id || "");
  };
  const execute = async (work: () => Promise<void>) => {
    if (inFlight.current) return;
    inFlight.current = true;setBusy(true);setError("");
    try { await work(); } catch (e) { setError((e as Error).message); }
    finally { setBusy(false);inFlight.current = false; }
  };
  const clock = match?.clock;
  const elapsed = Math.max(0, Math.floor((Date.now() - clockStarted) / 1000));
  // The client displays estimated time only; server commands/expiry ignore it.
  const timeLeft = clock ? fmt(clock.match_seconds_remaining - elapsed) : "--:--";
  const actionLeft = clock ? fmt(clock.turn_seconds_remaining - elapsed) : "--:--";
  void tick;
  const selectedAsset = match?.assets.find(a => a.id === selected) || match?.assets[0];
  const offers = match?.offers || [];
  const selection = offers.find(o => JSON.stringify(o) === chosen);
  const labelFor = (o: Action) => (
    o.action.replaceAll("_", " ") +
    (o.target ? " · " + (match?.assets.find(a => a.id === o.target)?.name || o.target) : "") +
    (o.source ? " from " + (match?.assets.find(a => a.id === o.source)?.name || o.source) : "") +
    " · " + o.cost + " credits"
  );
  const submit = async () => {
    if (!match || !selection || !clock) return;
    await execute(async () => {
      const updated = await request<Match>("/matches/" + match.id + "/commands", {
        command_id: crypto.randomUUID(), expected_sequence: clock.turn_sequence,
        action: selection.action, target: selection.target, source: selection.source,
      });
      setUpdated(updated);
      await refreshHistory();
    });
  };
  return (
    <>
      <header className={styles.header}>
        <Link href="/" className={styles.brand}>EduCyber</Link>
        <nav aria-label="Pilot navigation">
          <Link href="/red-blue">Classic Red / Blue</Link>
          <Link href="/help">Help</Link>
        </nav>
      </header>
      <main className={styles.main}>
        <div className={styles.hero}>
          <span className={styles.eyebrow}>V3 DEVELOPMENT PILOT · MICROFINANCE</span>
          <h1>Discover the threat. Defend the institution.</h1>
          <p>Build a defensive policy baseline, uncover connected assets through reconnaissance,
             and respond to evidence before the match clock expires.</p>
        </div>
        {error && <p role="alert" className={styles.error}>{error}</p>}
        {!loaded && <p role="status">Loading advanced simulator…</p>}
        {loaded && (
          <>
            <section className={styles.panel} aria-labelledby="setup-title">
              <h2 id="setup-title">Configure a new Microfinance match</h2>
              <div className={styles.forms}>
                <label>Your seat
                  <select aria-label="V3 seat" value={side} onChange={e => setSide(e.target.value as Side)}>
                    <option value="blue">Blue · protect assets</option>
                    <option value="red">Red · investigate and attack</option>
                  </select>
                </label>
                <label>Opponent
                  <select aria-label="V3 opponent" value={mode} onChange={e => setMode(e.target.value as "computer"|"human")}>
                    <option value="computer">Computer</option>
                    <option value="human">Another authenticated learner</option>
                  </select>
                </label>
                <label>Overall match duration
                  <select aria-label="V3 match duration" value={minutes} onChange={e => setMinutes(Number(e.target.value))}>
                    {[15,30,60,120].map(v => <option key={v} value={v}>{v} minutes</option>)}
                  </select>
                </label>
                <label>Maximum time per turn
                  <select aria-label="V3 turn limit" value={turnSeconds} onChange={e => setTurnSeconds(Number(e.target.value))}>
                    {[30,60,90,180,300].map(v => <option key={v} value={v}>{v} seconds</option>)}
                  </select>
                </label>
              </div>
              <button className={styles.primary} disabled={busy} onClick={() =>
                void execute(async () => {
                  const updated = await request<Match>("/matches", {
                    side, mode, match_minutes: minutes, turn_seconds: turnSeconds,
                  });
                  setUpdated(updated);await refreshHistory();
                })
              }>Create V3 match</button>
              <p className={styles.muted}>The engagement clock starts only after both seats have completed preparation. Timing and role settings cannot be renegotiated mid-match.</p>
            </section>
            <section className={styles.panel} aria-label="Saved V3 matches">
              <h2>Resume or join a match</h2>
              <div className={styles.saved}>
                {history.matches.map(row => (
                  <button key={row.id} disabled={busy} onClick={() => void execute(async () =>
                    setUpdated(await request<Match>("/matches/" + row.id)))}>
                    Match {row.id} · {row.side.toUpperCase()} · {row.status}
                  </button>
                ))}
              </div>
              <form onSubmit={e => {e.preventDefault();void execute(async () => {
                setUpdated(await request<Match>("/join", {token: joinCode.trim()}));
                setJoinCode("");await refreshHistory();
              });}}>
                <label htmlFor="v3-code">Private match invitation code</label>
                <input id="v3-code" value={joinCode} maxLength={43} autoComplete="off"
                  onChange={e => setJoinCode(e.target.value)} />
                <button disabled={busy || joinCode.trim().length !== 43}>Join another learner</button>
              </form>
            </section>
            {match && (
              <section aria-label="V3 match workspace" className={styles.workspace}>
                <div className={styles.heading}>
                  <div>
                    <span className={styles.eyebrow}>MATCH {match.id} · {match.side.toUpperCase()} · {match.phase.toUpperCase()}</span>
                    <h2>Ledger Under Pressure — Advanced Microfinance</h2>
                  </div>
                  <button disabled={busy} onClick={() => void execute(async () =>
                    setUpdated(await request<Match>("/matches/" + match.id)))}>
                    Refresh match
                  </button>
                </div>
                <p className={styles.muted}>Agreed match settings: {match.match_minutes} minutes overall, maximum {match.turn_seconds} seconds per turn. Each learner accepts these immutable limits when marking their seat ready.</p>
                <div className={styles.metrics}>
                  <div><small>MATCH CLOCK</small><strong>{timeLeft}</strong></div>
                  <div><small>TURN CLOCK</small><strong>{actionLeft}</strong></div>
                  <div><small>ACTIVE SEAT</small><strong>{clock?.active_side.toUpperCase() || "PREPARE"}</strong></div>
                  <div><small>AVAILABLE CREDITS</small><strong>{match.credits}</strong></div>
                </div>
                {match.phase === "prepare" && (
                  <section className={styles.panel} aria-labelledby="prepare-title">
                    <h3 id="prepare-title">Prepare your {match.side === "blue" ? "defensive baseline" : "reconnaissance strategy"}</h3>
                    {match.side === "blue" ? (
                      <>
                        <p>You own all five assets. Choose a policy deployment, confirm its real controls and cost, then mark your seat ready.</p>
                        <div className={styles.asset}>
                          <strong>Security policy library</strong>
                          <p className={styles.muted}>Declare governance requirements first. The policy does not deploy a technical control or automatically remove a weakness.</p>
                          <div className={styles.buttons}>
                            {(["patch_management","network_segmentation","security_monitoring","access_governance"] as const).map(policy=>(
                              <button key={policy} disabled={busy || match.prepared.blue || match.policies?.includes(policy)}
                                onClick={()=>void execute(async()=>setUpdated(await request<Match>(
                                  "/matches/" + match.id + "/prepare",{policy}
                                )))}>
                                {policy.replaceAll("_"," ")}
                              </button>
                            ))}
                          </div>
                          <p>Declared policies: {match.policies?.join(", ") || "None"}</p>
                        </div>
                        <div className={styles.policies}>
                          {match.assets.map(asset => (
                            <div key={asset.id} className={styles.asset}>
                              <strong>{asset.name}</strong>
                              <span>Value {asset.value}; vulnerabilities: {asset.weaknesses?.join(", ") || "None recorded"}</span>
                              <span>Current controls: {asset.controls?.join(", ") || "None"}</span>
                              <div className={styles.buttons}>
                                {(["monitoring","patched","segmented","hardened"] as const).map(policy => (
                                  <button key={policy} disabled={busy || match.prepared.blue || asset.controls?.includes(policy)}
                                    onClick={() => void execute(async () => setUpdated(await request<Match>(
                                      "/matches/" + match.id + "/prepare", {control:policy,target:asset.id})))}>
                                    {policy.replaceAll("_"," ")}
                                  </button>
                                ))}
                              </div>
                            </div>
                          ))}
                        </div>
                      </>
                    ) : (
                      <>
                        <p>You know only limited external entry points. Choose a reconnaissance approach without gaining access to Blue's internal inventory.</p>
                        <div className={styles.buttons}>
                          {(["surface_mapping", "quiet_investigation"] as const).map(strategy => (
                            <button key={strategy} disabled={busy || match.prepared.red}
                              onClick={() => void execute(async () => setUpdated(await request<Match>(
                                "/matches/" + match.id + "/prepare", {strategy})))}>
                              {strategy.replaceAll("_", " ")}
                            </button>
                          ))}
                        </div>
                      </>
                    )}
                    {match.mode === "human" && (
                      <div className={styles.invite}>
                        <button disabled={busy} onClick={() => void execute(async () => {
                          const info = await request<{token:string}>("/matches/" + match.id + "/invite", {});
                          setInvite(info.token);
                        })}>Create single-use invitation</button>
                        {invite && <label>Share privately with the other learner
                          <input readOnly value={invite} onFocus={e => e.target.select()}/></label>}
                      </div>
                    )}
                    <button className={styles.primary} disabled={busy || match.prepared[match.side]}
                      onClick={() => void execute(async () => setUpdated(await request<Match>(
                        "/matches/" + match.id + "/ready", {})))}>
                      {match.prepared[match.side] ? "Waiting for other seat" : "Finish preparation · ready to engage"}
                    </button>
                  </section>
                )}
                {(match.phase === "engage" || match.phase === "finished") && (
                  <>
                    <section className={styles.panel}>
                      <h3>Network intelligence</h3>
                      <p>{match.side === "blue"
                        ? "Your owned inventory and deployed protections are visible. Alerts reflect only configured monitoring."
                        : match.discovery_hint || "Additional assets may remain unknown."}</p>
                      <V3Topology assets={match.assets} connections={match.connections} side={match.side}/>
                      <div className={styles.grid}>
                        {match.assets.map(asset => (
                          <button className={styles.assetButton} key={asset.id}
                            aria-label={"Inspect " + asset.name}
                            onClick={() => {setSelected(asset.id);setInspectionTab("issues");setInspect(true);}}>
                            <span className={styles.icon}> {asset.kind === "database" ? "▣" : asset.kind === "workstation" ? "▤" : "◈"}</span>
                            <strong>{asset.name}</strong>
                            <small>{asset.kind.replaceAll("_", " ")} · {match.side === "blue"
                              ? "Value " + asset.value
                              : asset.business_value != null ? "Value " + asset.business_value : "Value unknown"}</small>
                            <small>{match.side === "blue"
                              ? asset.isolated ? "Isolated" : "Available"
                              : asset.knowledge || "Discovered"}</small>
                          </button>
                        ))}
                      </div>
                      <details>
                        <summary>Known directed trust paths ({match.connections.length})</summary>
                        <ul>{match.connections.map((edge,i) => <li key={i}>
                          {match.assets.find(a=>a.id===edge.source)?.name || edge.source} →{" "}
                          {match.assets.find(a=>a.id===edge.target)?.name || edge.target}
                        </li>)}</ul>
                      </details>
                    </section>
                    <div className={styles.layout}>
                      <section className={styles.panel} aria-labelledby="actions-title">
                        <h3 id="actions-title">All currently available actions</h3>
                        <p className={styles.muted}>
                          Actions appear for all authorised targets, not only the currently selected asset.
                          Unknown and prohibited actions remain unavailable.
                        </p>
                        <label htmlFor="v3-actions">Choose an action and target</label>
                        <select id="v3-actions" value={chosen} disabled={busy || match.phase !== "engage" ||
                          clock?.active_side !== match.side} onChange={e=>setChosen(e.target.value)}>
                          <option value="">Choose a permitted action</option>
                          {offers.map((o,i)=><option key={i} value={JSON.stringify(o)}>
                            {labelFor(o)}
                          </option>)}
                        </select>
                        {selection && presentation === "learning" && <p className={styles.hint}>
                          {selection.action === "recon"
                            ? "Reconnaissance may discover another connected service and can generate Blue telemetry."
                            : selection.action === "assess"
                            ? "Assessment can reveal known asset weaknesses; findings may become outdated after Blue intervention."
                            : selection.action.startsWith("wait_")
                            ? "Passing preserves credits but the overall match clock continues."
                            : "Actions are evaluated against private simulated conditions. An offered action is not a guaranteed success."}
                        </p>}
                        <button className={styles.primary} disabled={!selection || busy ||
                          match.phase !== "engage" || clock?.active_side !== match.side}
                          onClick={() => void submit()}>Commit action</button>
                        {clock && clock.active_side !== match.side && match.phase === "engage" &&
                          <p role="status">Waiting for {clock.active_side.toUpperCase()} to act.</p>}
                        {match.phase === "finished" && <p role="status">
                          <strong>{match.winner?.toUpperCase()} wins.</strong> {match.reason}
                          {match.score && <span className={styles.score}> Blue {match.score.blue_score} · Red {match.score.red_score} · Unavailable business value {match.score.service_value_unavailable} · Confirmed foothold value {match.score.foothold_value_confirmed}. {match.score.note}</span>}
                        </p>}
                      </section>
                      <section className={styles.panel} aria-label="Role-filtered evidence ledger">
                        <h3>Your evidence ledger</h3>
                        <p className={styles.muted}>Evidence is scoped to your seat. Absence of an alert does not establish safety.</p>
                        {match.evidence.length ? <ol className={styles.ledger}>
                          {[...match.evidence].reverse().map(ev => (
                            <li key={ev.sequence}>
                              <strong>{ev.kind.replaceAll("_", " ")} · Event {ev.sequence}</strong>
                              {ev.target && <small> · {match.assets.find(a=>a.id===ev.target)?.name || ev.target}</small>}
                              <p>{ev.message}</p>
                            </li>
                          ))}
                        </ol> : <p>No visible events have been recorded yet.</p>}
                      </section>
                    </div>
                    <section className={styles.panel}>
                      <h3>Gameplay presentation</h3>
                      <label>Assistance level
                        <select value={presentation} onChange={e=>setPresentation(e.target.value as "learning"|"realistic")}>
                          <option value="learning">Learning · contextual explanations</option>
                          <option value="realistic">Realistic · evidence-only</option>
                        </select>
                      </label>
                      <p className={styles.muted}>Switching assistance does not change your authorised evidence, resources or engine outcome.</p>
                    </section>
                  </>
                )}
                {inspect && selectedAsset && (
                  <div className={styles.overlay}>
                    <div role="dialog" aria-modal="true"
                      aria-label={"Asset details: " + selectedAsset.name}
                      className={styles.dialog}>
                      <div className={styles.heading}>
                        <div><span className={styles.eyebrow}>{selectedAsset.kind}</span>
                          <h3>{selectedAsset.name}</h3></div>
                        <button autoFocus onClick={() => setInspect(false)}>Close asset details</button>
                      </div>
                      <div className={styles.buttons} role="group" aria-label="Asset inspector tabs">
                        {(["issues","controls","activity"] as const).map(tab => (
                          <button key={tab} aria-pressed={inspectionTab===tab} onClick={()=>setInspectionTab(tab)}>
                            {tab}</button>))}
                      </div>
                      {inspectionTab === "issues" && (
                        match.side === "blue" ? (
                          <>
                            <p><strong>Business value:</strong> {selectedAsset.value}</p>
                            <p><strong>Security zone:</strong> {selectedAsset.zone || "Not classified"}</p>
                            <p><strong>Simulated days since patch:</strong> {selectedAsset.patch_age_days ?? "Not recorded"} {selectedAsset.patch_age_days && selectedAsset.patch_age_days > 60 ? "· Patch review recommended" : ""}</p>
                            <p><strong>Current weaknesses:</strong> {selectedAsset.weaknesses?.join(", ") || "None recorded"}</p>
                            <p><strong>Availability:</strong> {selectedAsset.isolated ? "Isolated" : "Available"}</p>
                          </>
                        ) : (
                          <>
                            <p><strong>Business value:</strong> {selectedAsset.business_value ?? "Not yet assessed"}</p>
                            <p><strong>Intelligence:</strong> {selectedAsset.knowledge || "Unknown"}</p>
                            <p><strong>Assessed weaknesses:</strong> {selectedAsset.assessment?.weaknesses.join(", ") || "Not assessed"}</p>
                            <p><strong>Observed zone:</strong> {selectedAsset.assessment?.zone || "Not confirmed"}</p>
                            <p><strong>Estimated patch age:</strong> {selectedAsset.assessment?.estimated_patch_age_days ?? "Unknown"} {selectedAsset.assessment ? "simulated days (can become stale)" : ""}</p>
                            <p><strong>Last observed turn:</strong> {selectedAsset.observed_at ?? "No assessment"}</p>
                            <p>Intelligence can become stale; hidden Blue interventions are not disclosed.</p>
                          </>
                        )
                      )}
                      {inspectionTab === "controls" && (
                        match.side === "blue" ?
                          <p>Installed controls: {selectedAsset.controls?.join(", ") || "None recorded"}</p> :
                          <p>Observed controls: {selectedAsset.assessment?.controls.join(", ") || "Not confirmed"}</p>
                      )}
                      {inspectionTab === "activity" && (
                        <ol>{match.evidence.filter(ev => ev.target === selectedAsset.id).map(ev => (
                          <li key={ev.sequence}>{ev.kind.replaceAll("_"," ")}: {ev.message}</li>
                        ))}</ol>
                      )}
                    </div>
                  </div>
                )}
              </section>
            )}
          </>
        )}
      </main>
    </>
  );
}
