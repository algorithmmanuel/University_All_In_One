/** Exact approved 24-course titles; never fabricate published courses. */
export const APPROVED_COURSES = ["Everyday Digital Risks & Safety Choices","Accounts, Privacy & Secure Online Habits","Spotting Scams, Misinformation & Manipulation","Investigating Suspicious Messages & Activity","Securing Devices, Data & Digital Communities","Digital Safety Response & Helping Others","Recognising Evolving Attacks & Defending Choices","Digital Citizenship, Ethics & Lifelong Security Habits","How Computers, Networks & Threats Interact","Network, Operating System & Identity Security Foundations","Evidence, Logs & Detection Fundamentals","Guided Incident Investigation & Threat Analysis","Defensive Engineering, Segmentation & Recovery","Incident Response, Forensics & Recovery Coordination","Adversary Behaviour, Detection & Defensive Strategy","Security Operations Capstone & Evidence-Based Debrief","Cyber Risk, Business Value & Decision-Making","Governance, Controls & Security Architecture","Risk Assessment, Metrics & Control Effectiveness","Incident Triage, Escalation & Stakeholder Decisions","Business Continuity, Third-Party & Operational Resilience","Crisis Leadership, Communication & Regulatory Response","Threat-Informed Defence, Control Trade-offs & Assurance","Enterprise Cyber Strategy, Exercising & Board Reporting"] as const;
export function isProductionCourse(title: string): boolean {
  return (APPROVED_COURSES as readonly string[]).includes(title);
}

/** Editorial stage order follows each consecutive block of eight courses. */
export const COURSE_STAGES = [
  "Discover", "Understand", "Check understanding", "Investigate with guidance",
  "Manage consequences", "Command an incident", "Face an adaptive opponent",
  "Compete and reflect"
] as const;

const ACADEMIES = ["secondary", "university", "cyber"] as const;
export function productionCourseMetadata(academyId: string, title: string) {
  const index = APPROVED_COURSES.indexOf(title as typeof APPROVED_COURSES[number]);
  if (index < 0 || ACADEMIES[Math.floor(index / COURSE_STAGES.length)] !== academyId) return null;
  return { stageIndex: index % COURSE_STAGES.length, stage: COURSE_STAGES[index % COURSE_STAGES.length] };
}
