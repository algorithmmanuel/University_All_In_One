# Lesson editorial handover — 31 October 2026

**Current result:** exact-duplication remediation complete across the measured library: **468 → 0** repeated 70-word signatures and **15 → 0** passage clusters. Fifteen course batches reviewed, 118 lesson bodies changed. Independent acceptance and publication remain blocked. Read the final validation section below before the historical batch entries.

**Scope:** development manuscripts only, `feature/beta-continuous-improvement`. Keep beta unchanged and publication blocked. No database operations, publisher execution or editorial approval signatures are authorised by these edits.

## Recovered checkpoint and baseline

Fresh checkout had no uncommitted changes. Remote development head was `befb040926d25c21945ebfbaafb664e2d066e9c2`; `658c357ae15b52f72be611beb483ff475ebe8ade` is an ancestor and documents the batch workflow. The audit implementation was introduced earlier in `d5dff93`; audit regression expectation was later corrected in `d077094`. The two initial Stage 7 revisions are present and preserved exactly. The historical 677-window CI count is superseded by the fresh local baseline below. Earlier status headings describing only six manuscript courses are historical: the present source has 24 draft courses and 192 lessons, with editorial acceptance still incomplete.

Read `api/audit_production_learning.py`, `api/test_audit_production_learning.py`, `api/test_production_course_manuscript.py`, the publication-boundary tests, the course release guide and curriculum plan before continuing. Audit counts are exact normalised-token signatures, grouped by adjacent matches; they are **not counts of duplicated paragraphs**. A clean exact-text audit does not establish semantic originality or educational acceptance.

## Completed batch evidence

| Checkpoint | Global repeated 70-word signatures | Global passage clusters | Course outcome |
| --- | ---: | ---: | --- |
| Fresh baseline at `befb040` | 468 | 15 | Stage 7: six affected lessons; Stage 8: four cross-course matches despite its historical within-course pass |
| Explorers Stage 7 completed | 345 | 7 | All eight reviewed; six rewritten; neither Stage 7 nor Stage 8 remains in the exact-overlap inventory |

Stage 7 lessons 1–2 are byte-for-byte equivalent in parsed content to the recovered checkpoint. Lessons 3–8 now have 653, 666, 638, 650, 656 and 663 words. They teach interruption fatigue, trust boundaries in an attack chain, reversible decisions under uncertainty, secondary recovery fraud, coordinated reporting and bounded counterfactual reasoning. Each includes distinct explanation, a fictional worked case and an exercise with reasoning. All course metadata, lesson titles, positions and relationships are preserved. No application code or assessments changed.

Local checks for this batch: four audit regressions passed; manuscript suite **16 passed, one failed**, solely the remaining whole-library 70-word overlap gate (345 signatures). Exact substantive-paragraph gate and all depth/structure tests passed. Preservation comparison passed for course metadata, lesson identities and both completed revisions. No fresh passing CI is claimed. Publication boundary test initially could not import SQLAlchemy in this fresh environment; rerun after installing the pinned test requirements and record the actual result.

## Reference review

On 31 October, web retrieval of NCSC `https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online` succeeded. It supports optional background on separate email passwords, two-step verification, updates and backups, and is labelled accordingly in Stage 7 lesson 8. CISA `https://www.cisa.gov/secure-our-world` returned HTTP 403; it is not represented as verified and was removed from this revised course's reading list. No source prose was copied. Human editorial review, browser accessibility and broader reference/licensing checks remain release requirements.

## Next work and acceptance hold

Next unfinished course in pathway/stage audit order: **Cyber Academy Stage 2 — Understand, lesson 1**, `api/production_learning/academy_understand.py`. Complete all eight lessons before moving on. Academy Stage 4 Investigate and Stage 5 Defend are independently assigned with separate file ownership in this session; they are not complete until centrally reviewed and validated. Re-run the global audit after each course and record its exact snapshot. The largest remaining families are shared Academy evidence prompts and Command banking decision prompts; replace them with subject-specific instruction, not word substitutions.

Publication remains blocked until both uniqueness gates pass globally, all 24 manuscripts receive substantive independent review and source validation, genuine hash-bound approvals exist, the full CI/reader/PostgreSQL-preservation gates pass, and release is authorised. Do not merge into beta, publish, reseed or alter learner records. CI runs may be pending or failing; distinguish their actual state from local checks.


## Completed batch: academy_defend

Reconstructed service objectives, network flow matrices, workload privilege, monitoring pipelines, deployed patch evidence, restoration checks, bounded containment and retry-safe resilience exercises. The central review checked the distinction between authentication/authorisation, network permission/application authority, backup availability/restoration integrity and timeout/commit uncertainty.

All eight lessons reviewed; word counts: 649, 646, 643, 637, 643, 649, 627, 694. Metadata, schema, titles and lesson positions match the prior committed course exactly. Per-course structure/depth and global exact-match exclusion checks passed; `git diff --check` passed. Proposed-commit global audit: **345 → 343 signatures**, **7 → 7 clusters**. The audit includes all 24 courses / 192 lessons and excludes other in-progress agent edits. A shared passage remains counted while any two other lessons still contain it. Snapshot: `docs/content-audit/2026-10-31-academy-defend.json`. No automatic human approval or fresh green CI is implied.

References: NIST CSF https://www.nist.gov/cyberframework and OWASP Top 10 https://owasp.org/projects/top-ten were opened and relevance checked on 31 October; these are optional overviews, not deployment prescriptions. Independent editorial/licensing acceptance remains open.

Exact next unfinished audit course: **academy_understand, lesson 1** (complete all eight lessons; source `api/production_learning/academy_understand.py`). Parallel assignments are provisional until their individual reviewed batches are recorded here. Beta, databases and publication block remain unchanged.

Dependency follow-up: installed repository-pinned CI requirements in an isolated temporary Python environment. All **five** publication-boundary negative tests passed with a nonconnecting in-memory URL; tests mock approvals and make no publication/database calls. The earlier missing-SQLAlchemy import blocker is resolved.


## Completed batch: academy_investigate

Reconstructed hypothesis testing, dependency scope, timezone-aware timelines, identity versus committed-action evidence, network/process correlation, evidence handling, bounded assessments and testable debrief recommendations. Central review checked the J8 recalculation case, explicit UTC conversions, account-versus-human attribution and limits of absent logs; none of these repeats the defensive-engineering exercises.

All eight lessons reviewed; word counts: 704, 720, 684, 716, 721, 734, 718, 782. Metadata, schema, titles and lesson positions match the prior committed course exactly. Per-course structure/depth and global exact-match exclusion checks passed; `git diff --check` passed. Proposed-commit global audit: **343 → 327 signatures**, **7 → 3 clusters**. The audit includes all 24 courses / 192 lessons and excludes other in-progress agent edits. A shared passage remains counted while any two other lessons still contain it. Snapshot: `docs/content-audit/2026-10-31-academy-investigate.json`. No automatic human approval or fresh green CI is implied.

References: NIST SP 800-61 Rev. 3 https://csrc.nist.gov/pubs/sp/800/61/r3/final and OWASP Logging Cheat Sheet https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html were opened and checked for incident-response and logging relevance on 31 October. Independent editorial/licensing acceptance remains open.

Exact next unfinished audit course: **academy_understand, lesson 1** (complete all eight lessons; source `api/production_learning/academy_understand.py`). Parallel assignments are provisional until their individual reviewed batches are recorded here. Beta, databases and publication block remain unchanged.


## Completed batch: academy_understand

Reconstructed request trust boundaries, routing versus filtering, DNS/TLS diagnosis, OS process privilege, configuration drift, session lifecycles, object-level ownership and integrated design. Central review checked the distinction between a network path and resource authorisation, certificate assurance versus business legitimacy, and foundational layer-by-layer diagnosis versus Stage 5 operational-control validation.

All eight lessons reviewed; word counts: 642, 626, 651, 643, 631, 631, 640, 659. Metadata, schema, titles and lesson positions match the prior committed course exactly. Per-course structure/depth and global exact-match exclusion checks passed; `git diff --check` passed. Proposed-commit global audit: **327 → 320 signatures**, **3 → 3 clusters**. The audit includes all 24 courses / 192 lessons and excludes other in-progress agent edits. A shared passage remains counted while any two other lessons still contain it. Snapshot: `docs/content-audit/2026-10-31-academy-understand.json`. No automatic human approval or fresh green CI is implied.

References: NIST SP 800-207 https://csrc.nist.gov/pubs/sp/800/207/final retrieved and checked on 31 October, supporting resource-focused access decisions and the limits of location-based trust. Link verification is not human editorial acceptance.

Exact next unfinished audit course: **academy_command, lesson 1** (complete all eight lessons; source `api/production_learning/academy_command.py`). Parallel assignments are provisional until their individual reviewed batches are recorded here. Beta, databases and publication block remain unchanged.


## Completed batch: explorers_compete

Reviewed all eight previously revised citizenship lessons. Replaced four remaining recycled cross-topic blocks with operational consent choices, accessible corrections, placement offboarding and comparable learning measurements; replaced all eight formulaic reflection prompts with subject-specific synthesis tasks. Preserved useful prior examples and exercises. This is a focused semantic cleanup, not a claim that every paragraph was newly rewritten. It addresses filler visible after exact overlap had already disappeared.

All eight lessons reviewed; word counts: 659, 617, 685, 658, 694, 675, 613, 703. Metadata, schema, titles and lesson positions match the prior committed course exactly. Per-course structure/depth and global exact-match exclusion checks passed; `git diff --check` passed. Proposed-commit global audit: **320 → 320 signatures**, **3 → 3 clusters**. The audit includes all 24 courses / 192 lessons and excludes other in-progress agent edits. A shared passage remains counted while any two other lessons still contain it. Snapshot: `docs/content-audit/2026-10-31-explorers-compete.json`. No automatic human approval or fresh green CI is implied.

References: NCSC personal-protection page rechecked; eSafety Commissioner consent-sharing page opened and relevance checked, with Australian legal/reporting scope explicitly separated from Nigerian practice. Removed the unverifiable CISA403 link. Source accessibility does not satisfy independent editorial acceptance.

Exact next unfinished audit course: **academy_command, lesson 1** (complete all eight lessons; source `api/production_learning/academy_command.py`). Parallel assignments are provisional until their individual reviewed batches are recorded here. Beta, databases and publication block remain unchanged.


## Completed batch: academy_command

Reconstructed response declaration, triage authority, forensic collection impact, event-time versus knowledge-time chronology, shared-integration containment, acknowledged-work recovery, causal corrective actions and a multi-cause tabletop. Central review checked response decisions versus the earlier investigation-only course and the distinction between lost acknowledgement, receipt and committed work.

All eight lessons reviewed; word counts: 671, 716, 707, 665, 693, 708, 708, 749. Metadata, schema, titles and lesson positions match the prior committed course exactly. Per-course structure/depth and global exact-match exclusion checks passed; `git diff --check` passed. Proposed-commit global audit: **320 → 316 signatures**, **3 → 3 clusters**. The audit includes all 24 courses / 192 lessons and excludes other in-progress agent edits. A shared passage remains counted while any two other lessons still contain it. Snapshot: `docs/content-audit/2026-10-31-academy-command.json`. No automatic human approval or fresh green CI is implied.

References: NIST SP 800-61 Rev.3 and SP 800-86 official publication pages opened and relevance checked; the older forensic guide is explicitly identified as general context, not current legal admissibility or a replacement for organisational procedures.

Exact next unfinished audit course: **academy_opponent, lesson 1** (complete all eight lessons; source `api/production_learning/academy_opponent.py`). Parallel assignments are provisional until their individual reviewed batches are recorded here. Beta, databases and publication block remain unchanged.


## Completed batch: command_understand

Reconstructed service ownership, measurable appetite, policy-to-procedure traceability, architecture authority, scoped effectiveness claims, three-lines independence, supplier concentration and governance decisions. Central review checked that internal audit does not become the operational approver and supplier assurance is bounded by service and period.

All eight lessons reviewed; word counts: 647, 663, 650, 648, 655, 647, 667, 689. Metadata, schema, titles and lesson positions match the prior committed course exactly. Per-course structure/depth and global exact-match exclusion checks passed; `git diff --check` passed. Proposed-commit global audit: **316 → 307 signatures**, **3 → 3 clusters**. The audit includes all 24 courses / 192 lessons and excludes other in-progress agent edits. A shared passage remains counted while any two other lessons still contain it. Snapshot: `docs/content-audit/2026-10-31-command-understand.json`. No automatic human approval or fresh green CI is implied.

References: Official NIST CSF and SP 800-53 Rev.5 publication pages opened and checked for governance outcomes and configurable controls. No fictional target or contract term is presented as a regulatory obligation.

Exact next unfinished audit course: **academy_opponent, lesson 1** (complete all eight lessons; source `api/production_learning/academy_opponent.py`). Parallel assignments are provisional until their individual reviewed batches are recorded here. Beta, databases and publication block remain unchanged.


## Completed batch: command_check

Reconstructed risk causal statements, impact and workload reasoning, mitigation dependencies, leaver deprovisioning assurance, meaningful denominators, sampling limits, accountable exceptions and a decision dashboard. Central review detected a duplicated vendor-MFA case shared with Understand and required a substantive replacement: lesson4 now reconciles HR events, missed application-account batches and rehire dates with explained period limitations.

All eight lessons reviewed; word counts: 656, 649, 640, 681, 629, 638, 649, 691. Metadata, schema, titles and lesson positions match the prior committed course exactly. Per-course structure/depth and global exact-match exclusion checks passed; `git diff --check` passed. Proposed-commit global audit: **307 → 298 signatures**, **3 → 3 clusters**. The audit includes all 24 courses / 192 lessons and excludes other in-progress agent edits. A shared passage remains counted while any two other lessons still contain it. Snapshot: `docs/content-audit/2026-10-31-command-check.json`. No automatic human approval or fresh green CI is implied.

References: Official NIST CSF and SP 800-53 publication pages opened and relevance checked on 31 October. Examples and calculations are fictional teaching cases, not quantitative forecasts or regulatory thresholds.

Exact next unfinished audit course: **academy_opponent, lesson 1** (complete all eight lessons; source `api/production_learning/academy_opponent.py`). Parallel assignments are provisional until their individual reviewed batches are recorded here. Beta, databases and publication block remain unchanged.


## Completed batch: academy_defend

Central semantic review identified that lesson2 repeated the foundation flow-matrix exercise. Replaced that lesson with a new outbound reporting integration, worker-versus-laptop DNS evidence, an inappropriate inbound supplier exception and receiving-tenant migration. The other seven validated defensive lessons remain unchanged. All eight rechecked for course continuity; this is a focused substantive correction.

All eight lessons reviewed; word counts: 649, 674, 643, 637, 643, 649, 627, 694. Metadata, schema, titles and lesson positions match the prior committed course exactly. Per-course structure/depth and global exact-match exclusion checks passed; `git diff --check` passed. Proposed-commit global audit: **298 → 298 signatures**, **3 → 3 clusters**. The audit includes all 24 courses / 192 lessons and excludes other in-progress agent edits. A shared passage remains counted while any two other lessons still contain it. Snapshot: `docs/content-audit/2026-10-31-academy-defend.json`. No automatic human approval or fresh green CI is implied.

References: Existing checked NIST CSF and OWASP overviews retained; the new supplier example is fictional and assumes no undocumented actual product behaviour.

Exact next unfinished audit course: **academy_opponent, lesson 1** (complete all eight lessons; source `api/production_learning/academy_opponent.py`). Parallel assignments are provisional until their individual reviewed batches are recorded here. Beta, databases and publication block remain unchanged.


## Completed batch: academy_opponent

Reconstructed threat relevance, reconnaissance lookalikes, entry-route changes, capability paths, privilege-change evidence, detection trade-offs, timed counterfactuals and a threat-informed capstone. Central review replaced lesson3 after finding a repeated two-session foundation exercise: it now analyses an adversary shifting from rejected approvals to recovery-contact changes and recovery-issued sessions, with distinct safe evidence and tests.

All eight lessons reviewed; word counts: 624, 621, 665, 617, 639, 640, 640, 708. Metadata, schema, titles and lesson positions match the prior committed course exactly. Per-course structure/depth and global exact-match exclusion checks passed; `git diff --check` passed. Proposed-commit global audit: **298 → 287 signatures**, **3 → 3 clusters**. The audit includes all 24 courses / 192 lessons and excludes other in-progress agent edits. A shared passage remains counted while any two other lessons still contain it. Snapshot: `docs/content-audit/2026-10-31-academy-opponent.json`. No automatic human approval or fresh green CI is implied.

References: MITRE ATT&CK, NIST SP 800-61r3 and OWASP Session Management official pages opened and relevance checked. These support conceptual behaviour and defensive control analysis, not attack execution or course certification.

Exact next unfinished audit course: **academy_compete, lesson 1** (complete all eight lessons; source `api/production_learning/academy_compete.py`). Parallel assignments are provisional until their individual reviewed batches are recorded here. Beta, databases and publication block remain unchanged.


## Completed batch: command_investigate

Reconstructed event classification, delegated decisions, evidence gaps, transaction-aware containment, stakeholder updates, supplier response, recovery acceptance and leadership tabletop. Central review checked separate treatment of confirmed facts, hypotheses and legal obligations, and the distinction between technical advice and accountable business acceptance.

All eight lessons reviewed; word counts: 632, 674, 652, 631, 648, 640, 659, 719. Metadata, schema, titles and lesson positions match the prior committed course exactly. Per-course structure/depth and global exact-match exclusion checks passed; `git diff --check` passed. Proposed-commit global audit: **287 → 266 signatures**, **3 → 3 clusters**. The audit includes all 24 courses / 192 lessons and excludes other in-progress agent edits. A shared passage remains counted while any two other lessons still contain it. Snapshot: `docs/content-audit/2026-10-31-command-investigate.json`. No automatic human approval or fresh green CI is implied.

References: Official NIST SP 800-61r3 and CSF pages opened and relevance checked; banking cases are fictional, no jurisdiction-specific deadlines invented.

Exact next unfinished audit course: **academy_compete, lesson 1** (complete all eight lessons; source `api/production_learning/academy_compete.py`). Parallel assignments are provisional until their individual reviewed batches are recorded here. Beta, databases and publication block remain unchanged.


## Completed batch: command_check

Central semantic review required two further differentiated lessons. Lesson6 now samples payment-adjustment authorisations with unmatched postings and cancelled tickets. Lesson8 now reconciles vulnerability denominators, an expired supplier exception and incomplete privileged-account coverage; it replaces the repeated backup-versus-service-recovery capstone. All eight reviewed with the earlier distinct leaver case retained.

All eight lessons reviewed; word counts: 656, 649, 640, 681, 629, 665, 649, 700. Metadata, schema, titles and lesson positions match the prior committed course exactly. Per-course structure/depth and global exact-match exclusion checks passed; `git diff --check` passed. Proposed-commit global audit: **266 → 266 signatures**, **3 → 3 clusters**. The audit includes all 24 courses / 192 lessons and excludes other in-progress agent edits. A shared passage remains counted while any two other lessons still contain it. Snapshot: `docs/content-audit/2026-10-31-command-check.json`. No automatic human approval or fresh green CI is implied.

References: Previously checked official NIST CSF and SP 800-53 sources retained; numerical denominators and sample limitations explicitly explained as fictional exercises.

Exact next unfinished audit course: **academy_compete, lesson 1** (complete all eight lessons; source `api/production_learning/academy_compete.py`). Parallel assignments are provisional until their individual reviewed batches are recorded here. Beta, databases and publication block remain unchanged.


## Completed batch: academy_compete

Reconstructed an integrated Lumen capstone with distinct scope, impact map, evidence register, containment, delegated-export access, key-dependent archive recovery, audience-specific reporting and independent debrief. Central review required an inline evidence packet, queued-job privilege revocation and cursor scope checks, and wrong-key/missing-key-authority recovery instead of another retry-duplication exercise. Lessons7–8 updated for continuity; controllers are optional and no missing external packet is required.

All eight lessons reviewed; word counts: 839, 634, 621, 618, 629, 643, 662, 654. Metadata, schema, titles and lesson positions match the prior committed course exactly. Per-course structure/depth and global exact-match exclusion checks passed; `git diff --check` passed. Proposed-commit global audit: **266 → 167 signatures**, **3 → 2 clusters**. The audit includes all 24 courses / 192 lessons and excludes other in-progress agent edits. A shared passage remains counted while any two other lessons still contain it. Snapshot: `docs/content-audit/2026-10-31-academy-compete.json`. No automatic human approval or fresh green CI is implied.

References: Official NIST SP 800-84, CSF and SP 800-53 pages checked for exercise design, outcome framing and control context. These are optional readings rather than a source of fictional evidence.

Exact next unfinished audit course: **command_defend, lesson 1** (complete all eight lessons; source `api/production_learning/command_defend.py`). Parallel assignments are provisional until their individual reviewed batches are recorded here. Beta, databases and publication block remain unchanged.


## Completed batch: command_defend

Reconstructed critical-service outcomes, hidden dependencies, recovery-option decisions, transaction reconciliation, supplier responsibilities, concentration and practical exit, controlled exercises and board resilience claims. Central review checked defined customer outcomes, realistic fallback capacity, joint acceptance and the separation of service recovery from equipment installation.

All eight lessons reviewed; word counts: 650, 656, 657, 660, 653, 660, 642, 698. Metadata, schema, titles and lesson positions match the prior committed course exactly. Per-course structure/depth and global exact-match exclusion checks passed; `git diff --check` passed. Proposed-commit global audit: **167 → 162 signatures**, **2 → 2 clusters**. The audit includes all 24 courses / 192 lessons and excludes other in-progress agent edits. A shared passage remains counted while any two other lessons still contain it. Snapshot: `docs/content-audit/2026-10-31-command-defend.json`. No automatic human approval or fresh green CI is implied.

References: Basel operational resilience canonical page and NIST SP 800-34 Rev.1 page opened and relevance checked; US federal contingency context explicitly qualified and international principles not treated as local legal rules.

Exact next unfinished audit course: **command_command, lesson 1** (complete all eight lessons; source `api/production_learning/command_command.py`). Parallel assignments are provisional until their individual reviewed batches are recorded here. Beta, databases and publication block remain unchanged.


## Completed batch: command_command

Reconstructed a Meridian executive crisis arc: delegated authority, reconciling situation metrics, business consequences of restrictions, controlled staff instructions, calibrated public statements, entity-specific notification assessment, verified external engagement and crisis-exit ownership. Central review checked pending-item/customer/loss distinctions and refusal to invent jurisdictional notification deadlines.

All eight lessons reviewed; word counts: 668, 680, 663, 665, 677, 718, 686, 735. Metadata, schema, titles and lesson positions match the prior committed course exactly. Per-course structure/depth and global exact-match exclusion checks passed; `git diff --check` passed. Proposed-commit global audit: **162 → 151 signatures**, **2 → 2 clusters**. The audit includes all 24 courses / 192 lessons and excludes other in-progress agent edits. A shared passage remains counted while any two other lessons still contain it. Snapshot: `docs/content-audit/2026-10-31-command-command.json`. No automatic human approval or fresh green CI is implied.

References: FSB Effective Practices for Cyber Incident Response and Recovery (2020) and NIST CSF official pages opened and relevance checked. Notification decisions require applicable official rules and qualified entity-specific assessment; these resources are not legal deadlines.

Exact next unfinished audit course: **command_opponent, lesson 1** (complete all eight lessons; source `api/production_learning/command_opponent.py`). Parallel assignments are provisional until their individual reviewed batches are recorded here. Beta, databases and publication block remain unchanged.


## Completed batch: command_opponent

Reconstructed service-value threat scenarios, conditional intelligence relevance, layered pathway mapping, availability trade-offs, end-to-end detection-to-response evidence, compensation limits, assurance coverage and adaptive investment. Central review checked account admission versus business authority and that threat headlines or campaign labels do not establish local exposure.

All eight lessons reviewed; word counts: 630, 629, 622, 624, 633, 629, 634, 688. Metadata, schema, titles and lesson positions match the prior committed course exactly. Per-course structure/depth and global exact-match exclusion checks passed; `git diff --check` passed. Proposed-commit global audit: **151 → 151 signatures**, **2 → 2 clusters**. The audit includes all 24 courses / 192 lessons and excludes other in-progress agent edits. A shared passage remains counted while any two other lessons still contain it. Snapshot: `docs/content-audit/2026-10-31-command-opponent.json`. No automatic human approval or fresh green CI is implied.

References: Official MITRE ATT&CK, NIST SP 800-53A Rev.5 and NIST CSF pages opened and relevance checked. CISA KEV returned403 and was omitted rather than labelled verified.

Exact next unfinished audit course: **command_compete, lesson 1** (complete all eight lessons; source `api/production_learning/command_compete.py`). Parallel assignments are provisional until their individual reviewed batches are recorded here. Beta, databases and publication block remain unchanged.


## Completed batch: command_compete

Reconstructed distinct enterprise strategy cases: rural lending launch, constrained investment portfolio, subsidiary release-programme measurement, acquisition-document exposure exercise, archive migration evidence, card-delivery concentration, board acquisition challenge and staged strategic migration. Central review checked investment assumptions, genuine supplier independence, corrected denominators and explicit conditions for expanding rollout.

All eight lessons reviewed; word counts: 628, 638, 621, 616, 625, 622, 635, 716. Metadata, schema, titles and lesson positions match the prior committed course exactly. Per-course structure/depth and global exact-match exclusion checks passed; `git diff --check` passed. Proposed-commit global audit: **151 → 0 signatures**, **2 → 0 clusters**. The audit includes all 24 courses / 192 lessons and excludes other in-progress agent edits. A shared passage remains counted while any two other lessons still contain it. Snapshot: `docs/content-audit/2026-10-31-command-compete.json`. No automatic human approval or fresh green CI is implied.

References: Official NIST CSF Profiles, NIST SP 800-84 and Basel operational resilience pages opened and relevance checked. Fictional targets and policies are clearly educational rather than regulatory requirements.

Exact next unfinished audit course: **No unfinished exact-duplication course remains.** Next is semantic/editorial acceptance review, starting Cyber Explorers Discover lesson 1, not publication.. Parallel assignments are provisional until their individual reviewed batches are recorded here. Beta, databases and publication block remain unchanged.


## Final validation and next acceptance task

Completed development source corresponds to GitHub content commit `c4f56ceeb1779356d227201fac714dc4eb9f85d8`. The connected GitHub app recreated all 17 local batch/correction commits with identical Git tree hashes and their ordered parent chain. Direct CLI push lacked credentials; app transfer preserves the reviewed content/history. Final documentation follows separately. Expected-head development update must reject any concurrent branch change. Beta observed before the update: `c8e5fbc06c057b59ed70dc1d907b28b52fcaefeb`; no beta ref or runtime/database operation is part of this work.

| Pathway/course scope | Course batches | Lesson bodies updated | Nature of work |
| --- | ---: | ---: | --- |
| Explorers Stage 7 Opponent | 1 | 6 | Remaining lessons rewritten; earlier lessons 1–2 exactly preserved |
| Explorers Stage 8 Compete | 1 | 8 | Four residual boilerplate passages replaced; eight specific reflections and reference/context improvements; useful prior teaching retained |
| Academy stages 2, 4, 5, 6, 7, 8 | 6 | 48 | Complete course rewrites with central differentiation/continuity corrections |
| Command stages 2–8 | 7 | 56 | Complete professional course rewrites with central case-diversity corrections |
| Total | 15 | 118 | Nine other courses unchanged; all 24 courses / 192 lessons included in global checks |

Actual local checks on the completed content:

- Whole-library audit `--check`: **PASS, 0 signatures / 0 clusters**. Baseline was 468 / 15; overlapping signatures were reviewed as passage families, not counted as separate paragraphs. Per-batch proposed-commit inventories and before/after counts are recorded above and in `docs/content-audit/` (each file's latest correction is current; Git history retains earlier snapshots).
- Focused audit + manuscript + publication-boundary suite: **26 passed, 18 subtests passed**. Includes all 17 manuscript cases, both global paragraph/sequence uniqueness gates, four audit regressions and five fail-closed approval/uniqueness tests.
- Full database-independent backend regression using pinned CI dependencies: **819 passed, 48 skipped, 29 subtests passed**, 31.53 seconds. One dependency deprecation warning. This used synthetic/in-memory test fixtures, no live PostgreSQL or owner database. Integration-dependent skips remain unverified locally.
- All course metadata, dictionary schema, lesson counts/titles/positions compared against `befb040`: **PASS**. Explorers Opponent lessons 1–2 exactly unchanged. No auth/progress/routing/assessment/engine/publisher/application logic changes. `git diff --check`: PASS.
- Revised-course external references opened and checked for subject relevance; inaccessible CISA links omitted rather than declared verified. Broad NIST/OWASP/FSB/Basel overviews are labelled supplementary, historical and jurisdictional context qualified. Entire-library licensing/reference review and independent learner accessibility remain open.
- No new frontend unit/type/build, Playwright, real-API/PostgreSQL, preservation or formal-security execution is claimed locally for this prose-only change. Fresh GitHub Actions results must be checked on the pushed revision; **CI is not claimed passed** in this checkpoint.

**Exact next unfinished task:** independent semantic/editorial acceptance review, **Cyber Explorers Discover, lesson 1**, `api/production_learning/explorers_discover.py`, followed by its complete eight-lesson course. No course remains in the exact-duplication inventory. Re-review natural concept overlap separately from repeated teaching; passing exact checks does not establish originality, comprehension or practical accuracy. Record specific evidence and reviewer findings without creating approvals on the owner's behalf. Prioritise the nine unchanged courses for substantive depth and reference review, while retaining full-library acceptance scope.

The publication hold remains until substantive independent review across all 24 courses, complete source/link/licensing checks, novice/experienced comprehension evidence, genuine exact-hash approvals, green full CI/reader/PostgreSQL-preservation gates and explicit release authority. Do not publish, reseed, merge into beta or alter learner records. No beta invitations or unrelated development.
