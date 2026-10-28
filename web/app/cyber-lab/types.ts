export type Source = { title: string; url: string; reviewed: string };
export type Module = {
  id: string;
  title: string;
  revision: string;
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
    worked_cases: { situation: string; reasoning: string }[];
  }[];
};
export type Catalog = {
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
  actions: { id: string; label: string; help: string; cost: number }[];
};
export type Run = {
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
  debrief?: { remaining_compromise: string[]; lessons: string[] };
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
