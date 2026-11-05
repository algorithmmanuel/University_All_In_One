# Production Learning Library — 24-course expansion specification

**Owner request:** 30 October 2026. **Status:** New content phase proposed; not yet authored, published, tested or promoted. Continue beta independently. Actual games remain unchanged.

## Product contract

Replace the learner-facing impression of three short demonstration courses with a substantial, production-quality reading-first catalogue of **24 distinct courses**, mapped to three audience pathways × eight learning stages. These are courses, not a claim that there are 24 different locked progression levels. Keep the shared eight-stage navigation model and allow direct access at all stages. Each pathway has different concepts, case studies and learning outcomes, not merely a rewritten difficulty tier. Reading-only learners must be able to complete a meaningful full learning journey without playing games; games and workshops remain optional complementary routes.

Each published course requires 8–12 **substantial, authored** lessons as an initial editorial target (192–288 lessons total), with learning objectives, structured explanatory text, concrete safe examples, worked case studies, exercises and explanations, a glossary, section review, course recap and **curated links to further reading at the end of the course**. Do not count placeholder lessons, a few sentences, generated filler or a list of links as complete course material. Make long material navigable with a lesson table of contents, reading progress, resume position, accessible headings, device-friendly typography and optional text-only/low-bandwidth presentation. Never auto-enrol or award completion for opening a route.

## Proposed 24-course curriculum matrix

| Stage | Cyber Explorers — everyday skills | Cyber Academy — technical and investigative | Cyber Command — operations, governance and assurance |
| --- | --- | --- | --- |
| 1. Discover | Everyday Digital Risks & Safety Choices | How Computers, Networks & Threats Interact | Cyber Risk, Business Value & Decision-Making |
| 2. Understand | Accounts, Privacy & Secure Online Habits | Network, Operating System & Identity Security Foundations | Governance, Controls & Security Architecture |
| 3. Check understanding | Spotting Scams, Misinformation & Manipulation | Evidence, Logs & Detection Fundamentals | Risk Assessment, Metrics & Control Effectiveness |
| 4. Investigate with guidance | Investigating Suspicious Messages & Activity | Guided Incident Investigation & Threat Analysis | Incident Triage, Escalation & Stakeholder Decisions |
| 5. Manage consequences | Securing Devices, Data & Digital Communities | Defensive Engineering, Segmentation & Recovery | Business Continuity, Third-Party & Operational Resilience |
| 6. Command an incident | Digital Safety Response & Helping Others | Incident Response, Forensics & Recovery Coordination | Crisis Leadership, Communication & Regulatory Response |
| 7. Face an adaptive opponent | Recognising Evolving Attacks & Defending Choices | Adversary Behaviour, Detection & Defensive Strategy | Threat-Informed Defence, Control Trade-offs & Assurance |
| 8. Compete and reflect | Digital Citizenship, Ethics & Lifelong Security Habits | Security Operations Capstone & Evidence-Based Debrief | Enterprise Cyber Strategy, Exercising & Board Reporting |

Names are initial editorial proposals, not claims of implemented courses. Each course must have unique objectives, distinct lesson bodies and suitable examples, with intentional cross-path reinforcement where justified.

## Lessons and reading sources

For each course provide a minimum of 8–12 in-depth lessons (final count driven by coverage), each with 3–6 clear objectives, plain-language explanation before technical vocabulary, several scenario-based worked examples, concept checks with reasoning, and a section for independent reflection. Include an original case study and a cumulative synthesis task or knowledge check. Course-level reading lists must feature reputable public materials relevant to its topic, selected from official primary sources where possible (for example NIST CSF and incident guidance, CISA secure-by-design and awareness guidance, OWASP foundational materials, MITRE ATT&CK conceptual technique pages, ENISA guides, ICO/privacy regulator public materials and appropriate security vendor-neutral documentation). Verify each actual URL, publication/source, relevance, current availability and licensing before publishing; do not invent or blindly scrape references. Distinguish external reading from required on-platform instruction. Avoid copyright reproduction; teach in original prose and link out. Content for entry-level learners should avoid assuming coding knowledge. Keep examples conceptual and safe, not operational exploit walkthroughs.

## Architecture and migration discipline

Inspect actual SQLAlchemy Course/Lesson/enrolment IDs, teaching seed scripts, API schema and current course contents before editing. Do not delete or replace existing demonstration-course records if learners are enrolled or have progress. Prefer additive versioned content publishing and an explicit mapping from existing courses to new content. Stable course identifiers/slugs, idempotent publication, audit-friendly content revisions, link metadata, pathway/stage tagging and rollout verification are required. Existing `/learn` requires an account; decide whether public course previews are appropriate while respecting current beta invitation controls. Preserve auth/session isolation, saved grades, assessments, workshop and game progression. Keep development/beta databases isolated and run preservation tests on actual PostgreSQL. No unreviewed schema, destructive seed or silent renumbering.

## UX and acceptance

`Browse Courses` opens a dedicated discovery view with three pathway selectors, eight stage filters and clear course cards stating outcomes, lesson count, expected workload and access requirements. Search or subject filters are desirable if a 24-course catalogue becomes hard to scan. Inside a course, learners must have chapter navigation, meaningful lesson content, reading progress/resume, previous/next lesson and a visible end-of-course further-reading list. Reading-only completion must be possible without game participation. The existing journey links need to navigate to a real relevant course without auto-enrolment; avoid dead ends. Test desktop/mobile, keyboard, focus, low bandwidth and long-form reading.

## Release gates

1. Content audit + approved curriculum/lesson outlines and course crosswalk; editorial review of each pathway.
2. Original, fact-checked lesson authoring (no placeholders) and verified reputable public reading URLs; evidence of learner comprehension with novice/experienced reviewers.
3. Idempotent additive publication with representative existing-account preservation, access control and isolated DB migration checks.
4. API/UI, accessibility, unit, Playwright, real-API/PostgreSQL, CI, security-related regression and deployment verification.
5. One coherent **course-library** release to development, then owner-approved source promotion to ongoing beta **after green gates**. Local beta deployment requires a separate safe release guide and explicit owner runtime verification.

**Scope boundary:** Keep actual games, Red/Blue engine and existing gameplay scoring untouched. The 24-course goal is new course authoring and its reader/catalogue UX, not a catalogue of 24 superficial titles or an automatic declaration of completion.
