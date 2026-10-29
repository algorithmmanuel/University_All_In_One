export type Side = "red" | "blue";
export type Order = {
  action: string;
  target: string | null;
  source: string | null;
};
export type Action = {
  id: string;
  side: Side;
  phase: string;
  cost: number;
  explanation: string;
  prerequisites: string;
  rule: string;
  technique: string;
  relation: string;
  url: string;
};
export type Catalog = {
  scenarios: {
    id: string;
    title: string;
    industry: string;
    difficulty: string;
    turn_limit: number;
  }[];
  actions: Action[];
};
export type Asset = {
  id: string;
  name: string;
  kind: string;
  value: number;
  exposed: boolean;
  controls?: string[];
  vulnerabilities?: string[];
  isolated?: boolean;
  disrupted: boolean;
  access?: number;
  assessed?: {
    controls: string[];
    vulnerabilities: string[];
    turn: number;
  } | null;
  leaked?: boolean;
  fraud?: boolean;
};
export type Match = {
  id: number;
  status: "waiting" | "active" | "finished";
  difficulty: string;
  mode: "computer" | "human";
  title: string;
  side: Side;
  turn: number;
  version: number;
  turn_limit: number;
  budget: number;
  action_points: number;
  committed: boolean;
  committed_order: Order | null;
  winner: Side | null;
  briefing: string;
  scenario: string;
  engine_version: string;
  objective: {
    kind: string;
    targets: string[];
    threshold: number;
    hold_turns: number;
  };
  assets: Asset[];
  connections: { source: string; target: string }[];
  orders: Order[];
  observations: {
    turn: number;
    type: string;
    target?: string;
    action?: string;
    message: string;
  }[];
};
export type History = {
  matches: {
    id: number;
    side: Side;
    title: string;
    status: string;
    created_at: string;
  }[];
  next_before_id: number | null;
};
export type Debrief = {
  winner: Side;
  explanation: string;
  timeline: (Order & {
    turn: number;
    side: Side;
    success: boolean;
    detected: boolean;
    framework: Action;
  })[];
  missed: {
    turn: number;
    target: string;
    action: string;
    reason: string;
    success: boolean;
  }[];
  alternatives: (Order & {
    turn: number;
    explanation: string;
    framework: Action;
  })[];
};
export type Command = Order & { command_id: string; expected_turn: number };
