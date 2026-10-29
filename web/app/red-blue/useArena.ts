"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import type {
  Catalog,
  Command,
  Debrief,
  History,
  Match,
  Order,
  Side,
} from "./types";
const API = (process.env.NEXT_PUBLIC_API_BASE_URL || "").replace(/\/$/, "");
class RequestError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
  }
}

/** Session-based client only: the API owns seats, offers, resources and outcomes. */
export function useArena() {
  const router = useRouter();
  const [catalog, setCatalog] = useState<Catalog | null>(null);
  const [history, setHistory] = useState<History>({
    matches: [],
    next_before_id: null,
  });
  const [match, setMatch] = useState<Match | null>(null);
  const [debrief, setDebrief] = useState<Debrief | null>(null);
  const [error, setError] = useState(""),
    [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true),
    [opened, setOpened] = useState(0);
  const [invite, setInvite] = useState<{
    token: string;
    expires_at: string;
  } | null>(null);
  const [uncertain, setUncertain] = useState(false);
  const pending = useRef<Command | null>(null),
    inFlight = useRef(false);
  const generation = useRef(0);
  const request = useCallback(
    async <T>(path: string, data?: unknown): Promise<T> => {
      const token = sessionStorage.getItem("educyber_token");
      if (!token) {
        router.replace("/account");
        throw new RequestError("Sign in to continue.", 401);
      }
      const response = await fetch(API + "/api/v1/red-blue" + path, {
        method: data === undefined ? "GET" : "POST",
        cache: "no-store",
        headers: {
          Authorization: "Bearer " + token,
          ...(data === undefined ? {} : { "Content-Type": "application/json" }),
        },
        ...(data === undefined ? {} : { body: JSON.stringify(data) }),
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
  const loadHistory = useCallback(
    async (cursor?: number) => {
      const page = await request<History>(
        "/matches" + (cursor ? "?before_id=" + cursor : ""),
      );
      setHistory((old) =>
        cursor ? { ...page, matches: [...old.matches, ...page.matches] } : page,
      );
    },
    [request],
  );
  const initialize = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const c = await request<Catalog>("/catalog");
      setCatalog(c);
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

  // GET polling never changes focus or applies a response to another opened match.
  useEffect(() => {
    if (
      !match ||
      !(match.status === "waiting" || match.committed) ||
      match.winner
    )
      return;
    let cancelled = false;
    const id = match.id;
    const timer = window.setInterval(async () => {
      if (document.visibilityState !== "visible" || inFlight.current) return;
      const ticket = generation.current;
      try {
        const current = await request<Match>("/matches/" + id);
        if (!cancelled && ticket === generation.current) {
          setMatch((old) =>
            !old || old.id !== id || current.version < old.version
              ? old
              : current.version === old.version &&
                  old.status !== "waiting" &&
                  current.status === "waiting"
                ? old
                : current,
          );
          if (current.status !== "waiting") setInvite(null);
        }
      } catch (e) {
        if (!cancelled) setError((e as Error).message);
      }
    }, 3000);
    return () => {
      cancelled = true;
      window.clearInterval(timer);
    };
  }, [match?.id, match?.status, match?.committed, match?.winner, request]);
  useEffect(() => {
    if (!match?.winner) return;
    let cancelled = false;
    request<Debrief>("/matches/" + match.id + "/debrief")
      .then((d) => {
        if (!cancelled) setDebrief(d);
      })
      .catch((e) => {
        if (!cancelled) setError(e.message);
      });
    return () => {
      cancelled = true;
    };
  }, [match?.id, match?.winner, opened, request]);

  useEffect(() => {
    if (match?.status === "finished") {
      void loadHistory().catch((e) => setError(e.message));
    }
  }, [match?.id, match?.status, loadHistory]);

  async function perform(task: () => Promise<void>) {
    if (inFlight.current) return;
    inFlight.current = true;
    generation.current++;
    setBusy(true);
    setError("");
    try {
      await task();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      inFlight.current = false;
      setBusy(false);
    }
  }
  function show(m: Match) {
    setMatch(m);
    setDebrief(null);
    setInvite(null);
    pending.current = null;
    setUncertain(false);
    setOpened((n) => n + 1);
  }
  async function start(
    scenario: string,
    side: Side,
    mode: string,
    difficulty: string,
  ) {
    await perform(async () => {
      show(
        await request<Match>("/matches", { scenario, side, mode, difficulty }),
      );
      await loadHistory();
    });
  }
  async function resume(id: number) {
    await perform(async () => {
      show(await request<Match>("/matches/" + id));
    });
  }
  async function join(token: string) {
    await perform(async () => {
      show(await request<Match>("/join", { token: token.trim() }));
      await loadHistory();
    });
  }
  async function createInvite() {
    if (!match) return;
    await perform(async () => {
      setInvite(await request("/matches/" + match.id + "/invite", {}));
    });
  }
  async function refresh() {
    if (!match) return;
    await perform(async () => {
      const current = await request<Match>("/matches/" + match.id);
      setMatch(current);
      // If the uncertain request is visibly committed/resolved it no longer needs retry.
      if (
        pending.current &&
        (current.committed ||
          current.turn !== pending.current.expected_turn ||
          current.winner)
      ) {
        pending.current = null;
        setUncertain(false);
      }
      if (current.status !== "waiting") setInvite(null);
      if (current.winner)
        setDebrief(await request("/matches/" + current.id + "/debrief"));
    });
  }
  async function seal(order?: Order) {
    if (!match) return;
    await perform(async () => {
      if (!pending.current && order)
        pending.current = {
          ...order,
          command_id: crypto.randomUUID(),
          expected_turn: match.turn,
        };
      if (!pending.current) return;
      try {
        const result = await request<Match>(
          "/matches/" + match.id + "/commands",
          pending.current,
        );
        setMatch(result);
        pending.current = null;
        setUncertain(false);
      } catch (e) {
        if (e instanceof RequestError && e.status < 500) {
          pending.current = null;
          setUncertain(false);
          if (e.status === 409)
            setMatch(await request<Match>("/matches/" + match.id));
        } else setUncertain(true); // Keep the exact UUID/payload for a safe retry.
        throw e;
      }
    });
  }
  async function more() {
    if (history.next_before_id)
      await perform(() => loadHistory(history.next_before_id!));
  }
  return {
    catalog,
    history,
    match,
    debrief,
    error,
    busy,
    loading,
    opened,
    invite,
    uncertain,
    start,
    resume,
    join,
    createInvite,
    refresh,
    seal,
    more,
    initialize,
  };
}
