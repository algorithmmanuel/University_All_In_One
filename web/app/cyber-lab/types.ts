export type Source = { title: string; url: string; reviewed: string };
export type Module = {
  id: string;
  title: string;
  revision: string;
  topics: string[];
  completed: boolean;
  previously_completed?: boolean;
  example: string;
  game: string;
  sections: {
    id: string;
    title: string;
    objective: string;
    body: string;
    source: Source;
    steps?: { title: string; body: string }[];
    check?: {
      id: string;
      prompt: string;
      options: string[];
      answer: number;
      explanation: string;
    };
    extra_readings?: Source[];
    worked_cases: { situation: string; reasoning: string }[];
  }[];
};
export type CampaignStep = {
  kind: "learn" | "practice" | "play";
  module?: string;
  scenario?: string;
  run_id?: number | null;
  label: string;
};
export type Catalog = {
  campaign?: {
    completed: number;
    total: number;
    notice: string;
    chapters: {
      scenario: string;
      title: string;
      scenario_title: string;
      module_read: boolean;
      practice_distinct: number;
      practice_target: number;
      wins: number;
      next: CampaignStep;
    }[];
  };
  question_count: number;
  modules: Module[];
  scenarios: {
    id: string;
    title: string;
    summary: string;
    difficulty: string;
    objective: string;
    lesson: string;
  }[];
  topics: {
    id: string;
    title: string;
    count: number;
    counts: Record<string, number>;
    mistakes: Record<string, number>;
  }[];
};
export type Asset = {
  id: string;
  label: string;
  role: string;
  weight: number;
  x: number;
  y: number;
  encrypted?: boolean;
  isolated: boolean;
  patched: boolean;
  monitored: boolean;
  pending: string | null;
  condition: string;
  due_turn?: number | null;
  validated_at?: number | null;
  observed_at?: number | null;
  actions: {
    id: string;
    label: string;
    help: string;
    cost: number;
    available?: boolean;
    reason?: string | null;
    duration?: number;
    staff_cost?: number;
  }[];
};
export type SiegeMetrics = {
  status: string;
  turns: number;
  exposure: number;
  lowest_service: number;
  credits_spent: number;
  actions_used: number;
  signals_reviewed: number;
};
export type TurnRecord = {
  turn: number;
  availability: number;
  exposure: number;
};
export type Run = {
  replay_of?: number;
  tactics?: {
    pressure: string;
    support_used: boolean;
    support_available: boolean;
    rules: string[];
    history: TurnRecord[];
    signals: {
      id: string;
      asset: string;
      turn: number;
      message: string;
      reviewed: boolean;
      finding: string | null;
      reviewed_turn?: number;
      review_order?: number;
    }[];
    jobs: { asset: string; action: string; due_turn: number }[];
    objectives: { label: string; met: boolean }[];
  };
  id: number;
  revision: string;
  scenario?: string;
  scenario_info?: {
    title: string;
    summary: string;
    objective: string;
    lesson: string;
  };
  vendor_revoked?: boolean;
  version: number;
  turn: number;
  budget: number;
  staff: number;
  status: string;
  exposure: number;
  availability: number;
  copy_ready: boolean;
  mfa: boolean;
  segmented: boolean;
  links: [string, string][];
  assets: Asset[];
  events: { turn: number; message: string }[];
  debrief?: {
    remaining_compromise: string[];
    lessons: string[];
    metrics?: SiegeMetrics;
    comparison?: SiegeMetrics | null;
    history?: TurnRecord[];
    decisions?: {
      turn: number;
      action: string;
      label: string;
      target: string;
      cost: number;
      service_before: number;
      service_after: number;
    }[];
  };
};
export type RunPreview = {
  id: number;
  turn: number;
  status: string;
  title?: string;
};
export type Question = {
  id: string;
  prompt: string;
  topic: string;
  options: string[];
  module: string;
};
export type Practice = {
  id: number;
  questions: Question[];
  result: null | {
    score: number;
    total: number;
    notice: string;
    feedback: {
      id: string;
      prompt: string;
      topic: string;
      correct: boolean;
      selected: string;
      expected: string;
      explanation: string;
      module: string;
      source: Source;
    }[];
  };
};
export type PracticePreview = {
  id: number;
  count: number;
  completed: boolean;
  score: number | null;
};
