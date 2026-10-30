/** Reviewed navigation over existing materials. Never awards progress or access. */
export const AUDIENCES = [
  {
    id: "all",
    title: "Explore all pathways",
    description: "Choose materials by your interests and current confidence.",
  },
  {
    id: "secondary",
    title: "Cyber Explorers",
    description:
      "Personal safety, everyday decisions and supported introductions to investigation.",
  },
  {
    id: "university",
    title: "Cyber Academy",
    description:
      "Technical foundations, evidence analysis and connected systems.",
  },
  {
    id: "professional",
    title: "Cyber Command",
    description: "Organisational risk, incident decisions and assurance.",
  },
] as const;
export type Audience = (typeof AUDIENCES)[number]["id"];
export const STAGES = [
  {
    id: "discover",
    title: "Discover",
    question: "Try a small cybersecurity decision.",
    description:
      "Explore a short public activity and decide what you want to learn.",
  },
  {
    id: "understand",
    title: "Understand",
    question: "Build the concepts behind your decisions.",
    description:
      "Read explanations, work through examples and practise during the lesson.",
  },
  {
    id: "check",
    title: "Check understanding",
    question: "Find what needs another look.",
    description:
      "Use a short assessment or topic practice, then revisit the explanations.",
  },
  {
    id: "investigate",
    title: "Investigate with guidance",
    question: "Read the evidence before you decide.",
    description:
      "Work through a guided case with briefings, evidence, hints and review questions.",
  },
  {
    id: "defend",
    title: "Manage consequences",
    question: "See your choices change an incident.",
    description:
      "Protect connected assets while balancing limited resources and business availability.",
  },
  {
    id: "command",
    title: "Command an incident",
    question: "Coordinate a complex response.",
    description:
      "Investigate uncertainty, manage dependencies and compare another strategy.",
  },
  {
    id: "opponent",
    title: "Face an adaptive opponent",
    question: "Anticipate the other side.",
    description:
      "Choose Red or Blue against a rule-based computer with the same information constraints.",
  },
  {
    id: "compete",
    title: "Compete and reflect",
    question: "Test your judgement with another learner.",
    description:
      "Make hidden choices, review the outcome together and exchange seats in a new match.",
  },
] as const;
export type Stage = (typeof STAGES)[number]["id"];
export type Resource = {
  title: string;
  description: string;
  href: string;
  kind: string;
};
export const FOUNDATIONS = {
  cyber: "Cyber Safety Foundations",
  citizenship: "Digital Citizenship Essentials",
  python: "Introduction to Python",
} as const;
export function parseJourney(query: string): {
  audience: Audience;
  stage: Stage;
} {
  const p = new URLSearchParams(query);
  return {
    audience: AUDIENCES.find((a) => a.id === p.get("pathway"))?.id || "all",
    stage: STAGES.find((s) => s.id === p.get("stage"))?.id || "discover",
  };
}
export function journeyUrl(stage: Stage, audience: Audience = "all") {
  return "/journey?stage=" + stage + "&pathway=" + audience;
}
/** Exclusive core allocations. Existing engines, IDs and saved records stay unchanged.
 * General collection browsing remains available outside these campaign suggestions.
 */
export type Pathway = Exclude<Audience, "all">;
export const PATHWAY_CONTENT = {
  secondary: {
    theme: "Everyday accounts, personal information and a first response",
    module: "protect",
    topics: ["fundamentals", "phishing", "identity", "endpoint"],
    defender: "branch",
    computer: "microfinance",
    final: "hospital",
    workshops: ["scholarship-pressure", "cia-invoice", "session-boundary", "login-correlation", "patch-window", "reconnect-decision", "resolution-order", "two-seat-ready"],
  },
  university: {
    theme: "Systems, technical evidence and connected service defence",
    module: "defend",
    topics: ["network", "application", "cloud"],
    defender: "supplier",
    computer: "software_cloud",
    final: "ai_service",
    workshops: ["shared-device", "mover-access", "rule-order", "scheduled-export", "segment-service", "clinical-containment", "trust-route", "lost-acknowledgement"],
  },
  professional: {
    theme: "Organisational risk, business recovery and accountable decisions",
    module: "recover",
    topics: ["governance", "response", "recovery"],
    defender: "ransomware",
    computer: "trusted_vendor",
    final: "payment_insider",
    workshops: ["approval-surprise", "restore-dependency", "cloud-policy", "vendor-signal", "supplier-credential", "executive-change", "stale-foothold", "after-action"],
  },
} as const;

export function workshopFor(stage: Stage, audience: Audience): string | null {
  if (audience === "all") return null;
  return PATHWAY_CONTENT[audience].workshops[STAGES.findIndex(s => s.id === stage)];
}
export function workshopBelongsTo(caseId: string, audience: Audience): boolean {
  return audience === "all" || (PATHWAY_CONTENT[audience].workshops as readonly string[]).includes(caseId);
}
export function nextPathway(audience: Audience): Pathway | null {
  return audience === "secondary" ? "university" : audience === "university" ? "professional" : null;
}

function pathwayChoices(stage: Stage, audience: Pathway): Resource[] {
  const content = PATHWAY_CONTENT[audience];
  const workshop = workshopFor(stage, audience)!;
  const workshopLink = "/workshops?case=" + workshop;
  const practiceNames: Record<string, string> = {
    fundamentals: "security goals and risk", phishing: "phishing and verification",
    identity: "accounts and access", endpoint: "devices and patching", network: "networks and containment",
    application: "application security", cloud: "cloud access", governance: "governance and assurance",
    response: "incident response", recovery: "recovery assurance",
  };
  switch (stage) {
    case "discover": return [{
      title: AUDIENCES.find(a => a.id === audience)!.title + " introduction",
      description: "Six distinct questions for this pathway, with explanations and an optional next-step suggestion.",
      href: "/preview?pathway=" + audience, kind: "Pathway introduction",
    }];
    case "understand": return [
      ...(audience === "secondary" ? [
        {title: "Digital Citizenship Essentials", description: "Personal information, digital footprints and responsible online choices.", href: "/learn?foundation=citizenship", kind: "Foundation course"},
        {title: "Cyber Safety Foundations", description: "Everyday account protection, suspicious messages and safer browsing.", href: "/learn?foundation=cyber", kind: "Foundation course"},
      ] : []),
      {title: {protect: "Protect the branch", defend: "Defend connected services", recover: "Respond, recover and assure"}[content.module],
       description: content.theme + ". Worked examples and topic teaching for this pathway.",
       href: "/cyber-lab?tab=learn&module=" + content.module, kind: "Pathway teaching module"},
      ...(audience === "university" ? [{title: "Introduction to Python · optional", description: "Values, conditions and loops as a supporting technical skill.", href: "/learn?foundation=python", kind: "Optional technical branch"}] : []),
    ];
    case "check": return content.topics.map(topic => ({
      title: "Practise " + practiceNames[topic], description: "A separate topic pool allocated to this pathway. Select a session length, review explanations and revisit mistakes.",
      href: "/cyber-lab?tab=practice&topic=" + topic + "&difficulty=foundational", kind: "Pathway topic practice",
    }));
    case "investigate": return [{title: AUDIENCES.find(a => a.id === audience)!.title + " investigations",
      description: "Ten distinct guided missions belonging to this pathway, with evidence, hints and explained reviews.",
      href: "/missions?pathway=" + audience, kind: "Pathway investigation library"}];
    case "defend": return [{
      title: {branch: "Defend the branch", supplier: "Supplier Access Crisis", ransomware: "Recovery Under Pressure"}[content.defender],
      description: {branch: "Prepare controls and protect a small connected branch while preserving service.", supplier: "Investigate recurring supplier access and contain compromise along connected systems.", ransomware: "Prioritise business recovery, verify a copy and restore disrupted services deliberately."}[content.defender],
      href: "/cyber-lab?scenario=" + content.defender, kind: "Pathway defender scenario",
    }];
    case "command": return audience === "university" ? [{title: "Branch Siege", description: "Coordinate eight assets, uncertain evidence, service dependencies and delayed work.", href: "/cyber-lab?scenario=siege", kind: "Technical incident capstone"}] : [{
      title: audience === "secondary" ? "The reconnection decision" : "The urgent executive change",
      description: audience === "secondary" ? "Coordinate a bounded recovery decision: check trust and entry conditions before reconnecting. A saved three-decision workshop, not a full network game." : "Protect approval integrity during an incident while managing business continuity. A saved three-decision workshop, not a full network game.",
      href: workshopLink, kind: "Pathway incident command workshop",
    }];
    case "opponent": return [{title: "Start a Red / Blue computer match", description: audience === "secondary" ? "Ledger Under Pressure: defend a microfinance setting, then examine the attacker’s route." : audience === "university" ? "Open Bucket, Closed Doors: test a software/cloud environment with connected technical assets." : "The Maintenance Window: evaluate the organisational consequences of third-party access.",
      href: "/red-blue?mode=computer&side=blue&difficulty=easy&scenario=" + content.computer, kind: "Pathway adversarial scenario"}];
    case "compete": return [
      {title: "Solo role-reversal challenge", description: "A different scenario from stage seven: " + ({hospital: "Night Shift Outage", ai_service: "Instructions in the Evidence", payment_insider: "The Trusted Session"}[content.final]) + ". Play Red, inspect the debrief, then start a new match as Blue.", href: "/red-blue?mode=computer&side=red&difficulty=standard&scenario=" + content.final, kind: "Pathway final challenge"},
      {title: "Revisit saved matches and debriefs", description: "Your existing match history across all pathways. Opening history does not start or complete an activity.", href: "/red-blue#saved-matches", kind: "Saved history across pathways"},
      {title: "Create a two-learner Red / Blue match", description: "Play this pathway’s final scenario with a distinct eligible learner. Commit hidden choices and compare the completed debrief.", href: "/red-blue?mode=human&scenario=" + content.final, kind: "Optional two-learner challenge"},
    ];
  }
}

function choicesFor(stage: Stage, audience: Audience): Resource[] {
  if (audience !== "all") return pathwayChoices(stage, audience);
  // Browse mode is explicitly a combined catalogue, not a fourth campaign.
  return (["secondary", "university", "professional"] as const).flatMap(path =>
    pathwayChoices(stage, path).map(resource => ({...resource,
      title: AUDIENCES.find(a => a.id === path)!.title + " · " + resource.title})));
}

/** Carry advisory context through existing routes without storing learner data. */
export function resourcesFor(stage: Stage, audience: Audience): Resource[] {
  return choicesFor(stage, audience).map((resource) => {
    const url = new URL(resource.href, "https://educyber.invalid");
    url.searchParams.set("journey_stage", stage);
    url.searchParams.set("journey_pathway", audience);
    return { ...resource, href: url.pathname + url.search + url.hash };
  });
}
export function activityJourney(pathname: string, query: string): string {
  const p = new URLSearchParams(query);
  const implied: Stage =
    pathname === "/workshops"
      ? "understand"
      : pathname === "/missions"
        ? "investigate"
        : pathname === "/assessments"
          ? "check"
          : pathname === "/red-blue"
            ? p.get("mode") === "human"
              ? "compete"
              : "opponent"
            : pathname === "/cyber-lab"
              ? p.get("tab") === "learn"
                ? "understand"
                : p.get("tab") === "practice"
                  ? "check"
                  : p.get("scenario") === "siege"
                    ? "command"
                    : "defend"
              : "understand";
  const stage =
    STAGES.find((s) => s.id === p.get("journey_stage"))?.id || implied;
  const audience =
    AUDIENCES.find(
      (a) => a.id === (p.get("journey_pathway") || p.get("pathway")),
    )?.id || "all";
  return journeyUrl(stage, audience);
}
