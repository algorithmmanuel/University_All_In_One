# Owner playthrough — navigation and learning progression remediation

**Recorded:** 30 October 2026 (Africa/Lagos)  
**Status:** Approved observations received; proposed remediation scoped, **not implemented or tested**. Development pause remains in effect for unrelated features.  
**Source:** Owner's six-page `Testing Observations.docx`, pages 1–5. Page 6 contains an empty item 6, so no sixth issue is inferred.

## Scope and design intent

Address the owner's reported confusing navigation without asserting that unreported functionality is defective. Preserve existing user accounts, authentication, beta isolation, content, 30-game library, 24 workshops, 500-question practice, saved progress, role-based Red/Blue gameplay and the navy/teal site palette with seat-specific simulator accents. Do not alter simulator secrecy, scoring or mechanics for a navigation fix. The existing eight stages may remain a **shared pedagogical framework**, but must not imply identical pathway curricula.

### UX-NAV-01 — Visible help and orientation (High)
Add a persistent, keyboard-accessible **Start here / How EduCyber works** entry point. Provide an accessible short guide and a concise glossary of Discover, Understand, Check understanding, Investigate with guidance, Manage consequences, Decision Workshop, games, Cyber Lab and Red/Blue. Define the purpose, prerequisites, expected duration (when known), whether login is required, how progress is saved and where the user goes next. Use progressive disclosure: brief inline descriptions and a route map rather than making a long manual mandatory. Provide back-to-journey and breadcrumbs; test mobile and keyboard navigation.

**Acceptance:** A first-time tester can explain the pathways and locate a workshop, mission, assessment and simulator without developer assistance.

### UX-NAV-02 — Meaningfully differentiated audience pathways (Critical)
Define **Cyber Explorers** as everyday digital-safety / novice exploration, **Cyber Academy** as structured technical foundations and investigation, and **Cyber Command** as operational/organisational decision-making and adversarial practice. Explain each with suitability, outcomes, level and sample activities *before selection*. Keep **Explore all pathways** as catalogue browsing, **not** a fourth curriculum. On selection, show visibly different entry copy, a stage-specific recommended activity sequence, outcome and next-step options, rather than a cosmetic tab change. Retain a common eight-stage framework where pedagogically useful, but use pathway-specific content mappings and examples; do not clone eight independent engines or falsely claim all resources are unique. Keep direct later-stage entry available to experienced users, and allow switching pathways without deleting progress.

**Acceptance:** A user selecting each pathway sees distinct recommendations at Discover and at least one later stage, knows why a recommendation belongs there, can switch pathways and resume saved progress. An independent tester can distinguish all three from the screen, not the documentation alone.

### UX-NAV-03 — Intentional introductory assessment and labels (High)
The public six-question `Spot the risk` activity may be a common *optional diagnostic*, but label it honestly as shared and avoid presenting it as a unique pathway mission. Each pathway must have a pathway-relevant recommended first activity. Remove duplicated command verbs: e.g. **Start the six-question preview** and **Browse foundation courses**, not “Open Try…” or “Open Browse…”. Apply terminology, grammar and accessible names consistently across buttons, headings, browser titles and help.

**Acceptance:** No duplicate-verb buttons remain; the shared preview and pathway-specific activities are visibly distinguished; links lead to the named experience.

### UX-NAV-04 — Distraction-free assessment view (High)
Move the six-question assessment into a focused route or equivalent isolated view that does not render the 30-game catalogue beneath its active questions. Preserve keyboard focus, progress (question n of 6), back/exit controls, responsive/mobile layout and reduced-motion preference. Avoid involuntary loss of answered work. Give users a clear return route to the pathway.

**Acceptance:** During assessment only the assessment context is visible; the library cannot intrude into the active assessment viewport; leaving and returning behaves predictably.

### UX-NAV-05 — Completion, feedback and next step (Critical)
After the six-question activity, show an explicit completion state: score, explanations, missed concepts, retry and an actionable next step. For authenticated learners, save results only when consent/storage rules and existing progress architecture allow; guests retain a clearly described session-only experience. **A six-question score must not act as a definitive competence placement**. Use transparent advisory bands, with a separate novice/experienced self-selection and accessible **Choose another stage** override. Recommend an introductory activity when core concepts were missed and a progressively harder pathway-specific activity when strong; never lock the curriculum based solely on six items. Distinguish diagnostic suggestions from measured mastery. Avoid duplicate awarding or accidental progress writes.

**Acceptance:** Every completion state has a usable next action; score-based advice is explainable, optional and never gates advanced entry; guest/authenticated behavior and session independence are tested.

### UX-NAV-06 — Journey consistency and telemetry (High)
Provide one clearly understood `Home → Pathway → Stage → Activity → Results → Next step` journey, with consistent headings, breadcrumbs, progress indicators and return links across courses, assessments, games and workshops. Instrument privacy-conscious aggregate navigation/abandonment events only if already permitted by product privacy controls; do not add tracking by default. Collect structured first-time and experienced tester observations.

**Acceptance:** No dead-end completion screens or involuntary loops in covered journeys; browser back, direct URLs, re-login and pathway switching work without losing completed activities.

## Implementation order and acceptance gates

1. **Baseline & contract:** inspect current Next.js routes/components, journey-stage map, public `Spot the risk` implementation, state persistence and existing tests. Map current URLs and capture screenshots before editing. Clarify whether a shared diagnostic is required and identify pathway-specific existing content; no schema or engine changes presumed.
2. **Information architecture:** write an explicit pathway-content-stage matrix and screen copy; define deep links, back navigation and focused routes. Obtain owner review of three sample pathway screens before broad duplication.
3. **Implement cohesive UX release:** help entry point, pathway descriptions/mappings, copy cleanup, focused assessment, results/recommendations and consistent next action. Prefer additive, reversible UI changes; any needed data migration requires separate justification, backup and preservation tests.
4. **Verify:** frontend unit and accessibility checks (semantic labels, keyboard, focus, contrast); Playwright desktop/mobile journeys for guest, existing authenticated learner, new learner and experienced direct entry; three pathway differentiation assertions; complete six questions and follow different recommendation bands; no catalogue on question screen; switching pathways; browser history; refresh; logout/session isolation; stale response and saved-progress regression. Run established API, PostgreSQL, frontend/build/browser and security-related regression gates appropriate to changed surfaces.
5. **Owner acceptance:** ask owner to play full novice and experienced journeys with fresh and existing accounts. Capture first-click orientation, number of loops/dead ends and whether users understand *Decision Workshop* unaided. Verify beta separately; **do not promote to beta or claim laptop deployment without owner authorisation and independent evidence**.

## Release discipline / out of scope

This is a planned **navigation and onboarding correction**, not a request to rebuild 30 games, rework simulator rules, introduce AI, expand question banks, or replace the eight-stage framework wholesale. Update this plan, roadmap, status and handover at each actual milestone. The six-page feedback document contains five populated numbered findings; preserve its assumption that everything else is working. No implementation, testing, CI, deployment or beta promotion is claimed by this documentation checkpoint.

## Single-release authorisation and first implementation checkpoint — 30 October 2026

Owner explicitly authorised one major navigation/onboarding release and requested subsequent promotion into the ongoing tester-facing beta, while excluding changes to actual games and gameplay. Preserve two independent runtime environments. Work started on development branch: added `/help`, dedicated `/preview`, six-question completion/review/non-gating guidance, pathway-distinct Discover recommendations, clearer button labels and visible pathway explanations. Existing question bank and game engines are untouched. **Pending:** complete cross-route UX and browser regressions, CI/build and owner-machine readiness before any beta promotion. The existing beta is not yet updated. The permission to promote is conditional on passing acceptance gates; never infer successful deployment from commits.
