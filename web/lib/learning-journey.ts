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
function choicesFor(stage: Stage, audience: Audience): Resource[] {
  const path = audience === "all" ? "secondary" : audience;
  const missionTitle = {
    secondary: "Cyber Explorers investigations",
    university: "Cyber Academy investigations",
    professional: "Cyber Command investigations",
  }[path];
  const topic = (
    {
      secondary: "phishing",
      university: "network",
      professional: "governance",
    } as const
  )[path];
  const module = (
    {
      secondary: "protect",
      university: "defend",
      professional: "recover",
    } as const
  )[path];
  const scenario = {
    secondary: "microfinance",
    university: "software_cloud",
    professional: "payment_insider",
  }[path];
  switch (stage) {
    case "discover": {
      const introductions: Record<Audience, Resource> = {
        all: {title:"Browse every pathway",description:"Compare what each audience learns, then choose an area to explore.",href:"/help",kind:"Pathway overview"},
        secondary: {title:"Start with digital safety foundations",description:"Explore accounts, scams and safe everyday decisions before guided investigations.",href:"/learn?foundation=citizenship",kind:"Cyber Explorers starting point"},
        university: {title:"Begin technical foundations",description:"Build an understanding of security concepts, then investigate systems and network evidence.",href:"/cyber-lab?tab=learn&module=defend",kind:"Cyber Academy starting point"},
        professional: {title:"Explore organisational risk decisions",description:"Study governance, response and recovery decisions before more complex simulation.",href:"/cyber-lab?tab=learn&module=recover",kind:"Cyber Command starting point"},
      };
      return [introductions[audience],{
        title:"Six-question shared preview",
        description:"An optional diagnostic for every pathway. See explanations and receive a non-binding suggested next stage.",
        href:"/preview?pathway="+audience,
        kind:"Optional public introduction",
      }];
    }
    case "understand":
      return [
        {
          title: "Cyber Safety Foundations",
          description:
            "Phishing, account protection and safer browsing; three lessons with worked examples.",
          href: "/learn?foundation=cyber",
          kind: "Foundation course",
        },
        ...(audience === "all" || audience === "secondary"
          ? [
              {
                title: "Digital Citizenship Essentials",
                description:
                  "Digital footprints, privacy and respectful online conduct.",
                href: "/learn?foundation=citizenship",
                kind: "Foundation course",
              },
            ]
          : []),
        {
          title: {
            protect: "Protect the branch",
            defend: "Defend connected services",
            recover: "Respond, recover and assure",
          }[module],
          description:
            "Applied teaching with reflections, worked decisions and optional public reading.",
          href: "/cyber-lab?tab=learn&module=" + module,
          kind: "Cybersecurity module",
        },
        {
          title: "Introduction to Python · optional",
          description:
            "Variables, conditions and loops. Useful technical foundations; never a prerequisite for playing.",
          href: "/learn?foundation=python",
          kind: "Optional technical branch",
        },
      ];
    case "check":
      return [
        {
          title: "Choose a course assessment",
          description:
            "Quick, Standard, Extended or Custom. Review the explanations and the evidence from that attempt.",
          href: "/assessments",
          kind: "Knowledge check",
        },
        {
          title:
            "Practise " +
            {
              phishing: "phishing and verification",
              network: "networks and containment",
              governance: "governance and assurance",
            }[topic],
          description:
            "Start with a short topic session from the 500-question bank. You can change topic and difficulty.",
          href:
            "/cyber-lab?tab=practice&topic=" +
            topic +
            "&difficulty=foundational",
          kind: "Topic practice",
        },
        {
          title: "Review your practice mistakes",
          description:
            "Choose a topic and revisit previously missed questions. This needs earlier submitted practice.",
          href: "/cyber-lab?tab=practice&practice_mode=mistakes",
          kind: "Revision",
        },
      ];
    case "investigate":
      return [
        {
          title:
            audience === "all"
              ? "Explore the guided investigation library"
              : missionTitle,
          description:
            "Read the briefing, inspect evidence, make decisions and review the explanations. 2D and 3D are alternative views of the same mission.",
          href: "/missions?pathway=" + path,
          kind: "Guided investigation",
        },
      ];
    case "defend":
      return [
        {
          title: "Defend the branch",
          description:
            "Beginner strategy: prepare controls, investigate compromise and preserve service.",
          href: "/cyber-lab?scenario=branch",
          kind: "Beginner simulation",
        },
        {
          title: "Supplier Access Crisis",
          description:
            "Control recurring supplier access and deal with existing compromise.",
          href: "/cyber-lab?scenario=supplier",
          kind: "Intermediate simulation",
        },
        {
          title: "Recovery Under Pressure",
          description:
            "Contain disruption, verify a recovery source and restore services deliberately.",
          href: "/cyber-lab?scenario=ransomware",
          kind: "Intermediate simulation",
        },
      ];
    case "command":
      return [
        {
          title: "Branch Siege",
          description:
            "An advanced incident across eight assets, with uncertain signals, dependencies and delayed work. Finish, replay the same incident and compare decisions.",
          href: "/cyber-lab?scenario=siege",
          kind: "Advanced simulation",
        },
        {
          title: "Prepare with response and recovery teaching",
          description:
            "Review incident response, recovery and control assurance before or after your run.",
          href: "/cyber-lab?tab=learn&module=recover",
          kind: "Supporting study",
        },
      ];
    case "opponent":
      return [
        {
          title: "Start a Red / Blue computer match",
          description:
            "Begin with Blue and an easy computer in a suggested scenario. You can change seat, scenario and difficulty before starting.",
          href:
            "/red-blue?mode=computer&side=blue&difficulty=easy&scenario=" +
            scenario,
          kind: "Adversarial simulation",
        },
        {
          title: "Choose a harder computer challenge",
          description:
            "The hard policy changes decisions, not resources or access to hidden information. It is rule-based, with no external generative AI.",
          href: "/red-blue?mode=computer&difficulty=hard&scenario=" + scenario,
          kind: "Optional challenge",
        },
      ];
    case "compete":
      return [
        {
          title: "Solo role-reversal challenge",
          description:
            "Playing alone? Take Red against the computer, inspect the debrief, then create a new match as Blue. Compare what each seat could know before its decisions.",
          href:
            "/red-blue?mode=computer&side=red&difficulty=standard&scenario=" +
            scenario,
          kind: "Solo reflection and replay",
        },
        {
          title: "Create a two-learner Red / Blue match",
          description:
            "Use two different eligible student accounts in separate browser sessions. Invite privately, seal choices and read the participant debrief after the match.",
          href: "/red-blue?mode=human&scenario=" + scenario,
          kind: "Two-learner simulation",
        },
        {
          title: "Revisit saved matches and debriefs",
          description:
            "Resume a match or reopen a finished debrief. Exchange seats by creating a new match; existing seats remain bound to their players.",
          href: "/red-blue#saved-matches",
          kind: "Reflection and replay",
        },
      ];
  }
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
