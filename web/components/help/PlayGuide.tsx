import Link from "next/link";
import { AUDIENCES, STAGES, resourcesFor, journeyUrl } from "../../lib/learning-journey";
import styles from "./help.module.css";

const chapters = [
  ["start", "Your first visit"], ["pathways", "Choose your pathway"],
  ["stages", "Follow the eight stages"], ["study", "Read and practise"],
  ["investigations", "Play a guided mission"], ["workshops", "Play a decision workshop"],
  ["defender", "Play a defender simulation"], ["red-blue", "Play Red / Blue"],
  ["progress", "Save, return and move on"], ["trouble", "Get unstuck"],
] as const;

/** Learner-facing instructions only. Deployment/configuration belongs in the maintainer runbook. */
export default function PlayGuide() {
  return <>
    <nav className={styles.contents} aria-label="How to play contents">
      <h2>How to play · contents</h2>
      <ol>{chapters.map(([id,title]) => <li key={id}><a href={"#"+id}>{title}</a></li>)}</ol>
    </nav>

    <section id="start" className={styles.chapter} aria-labelledby="start-heading">
      <h2 id="start-heading" tabIndex={-1}>1. Your first visit</h2>
      <p>EduCyber combines lessons, question practice, guided investigations and strategy games. Start with a short decision, learn why it matters, then apply it in a case or simulation. All systems, attacks and business events in the games are fictional.</p>
      <ol>
        <li>Open <Link href="/journey">Learning journey</Link> and select Cyber Explorers, Cyber Academy or Cyber Command.</li>
        <li>If you are new, begin at Discover. Try your pathway’s six-question introduction, read each explanation and choose a suggested next stage or any stage yourself. This public preview needs no account and saves no learner score.</li>
        <li>For saved learning and games, <Link href="/account">sign in with your own learner account</Link>. If beta access requires an invitation, use your invitation or contact the organiser. Account registration and signing in are separate steps.</li>
        <li>Choose an activity and read its goal before pressing its start button. Opening a journey link only selects material; it does not enrol you, start a game or mark a stage complete.</li>
      </ol>
      <p><strong>A good first session:</strong> choose Cyber Explorers, try its introduction, study account protection, practise an account question, and play Scholarship Detective from its investigation library. Later, try Defend the branch with its briefing open. You do not need to complete everything in one sitting.</p>
    </section>

    <section id="pathways" className={styles.chapter} aria-labelledby="pathways-heading">
      <h2 id="pathways-heading" tabIndex={-1}>2. Choose your pathway</h2>
      <p>Each pathway uses the same eight stage names but has its own core materials. Switching pathways changes the introduction, teaching module, practice topics, ten investigations, eight allocated workshops and simulation scenarios. It is not simply the same game at a harder setting. Shared controls help you concentrate on the new decisions.</p>
      <div className={styles.pathways}>{AUDIENCES.filter(a=>a.id!=="all").map(a=><article className="card" key={a.id}>
        <h3>{a.title}</h3><p>{a.description}</p>
        <p>{a.id==="secondary" ? "Start with everyday security. Study Protect the branch; play Defend the branch, Ledger Under Pressure and Night Shift Outage." : a.id==="university" ? "Study connected systems. Use Defend connected services, Supplier Access Crisis, Branch Siege, Open Bucket, Closed Doors and Instructions in the Evidence. Python is an optional supporting subject." : "Study response, recovery and assurance. Play Recovery Under Pressure, The Maintenance Window and The Trusted Session, alongside organisational decision cases."}</p>
        <Link className="btn" href={journeyUrl("discover",a.id)}>Begin {a.title} →</Link>
      </article>)}</div>
      <p>Explore all pathways is a combined browsing view, not a fourth campaign. General collections and saved history remain accessible. You may deliberately explore outside your selected route.</p>
    </section>

    <section id="stages" className={styles.chapter} aria-labelledby="stages-heading">
      <h2 id="stages-heading" tabIndex={-1}>3. Follow the eight stages</h2>
      <p>Use the stage buttons in Learning journey. New learners can work in order; experienced learners can enter later. Stage numbers describe a learning sequence, not locked levels. The material can still be challenging in an earlier stage.</p>
      <ol className={styles.stages}>{STAGES.map(stage=><li key={stage.id}>
        <h3>{stage.title}</h3><p>{stage.description}</p>
        <ul>{AUDIENCES.filter(a=>a.id!=="all").map(a=><li key={a.id}><strong>{a.title}:</strong>{" "}<Link href={journeyUrl(stage.id,a.id)}>{resourcesFor(stage.id,a.id).filter(r=>!r.kind.includes("Saved history")).map(r=>r.title).join("; ")}</Link></li>)}</ul>
      </li>)}</ol>
      <p><strong>Stage six:</strong> Explorers and Command use focused three-decision incident workshops. Academy uses the full Branch Siege simulation, with a supporting workshop. These are different activity formats, labelled on the journey.</p>
      <p>After the final challenge, reflect on your result and use the invitation to explore the next pathway: Explorers → Academy → Command. Returning to study or replaying is useful too. Clicking Next stage or reaching stage eight does not award completion, a certificate or mastery.</p>
    </section>

    <section id="study" className={styles.chapter} aria-labelledby="study-heading">
      <h2 id="study-heading" tabIndex={-1}>4. Read and practise</h2>
      <h3>Courses and applied teaching</h3>
      <ol>
        <li>Open a recommended course in <Link href="/learn">My learning</Link>. Enrol if needed, then open a lesson.</li>
        <li>Read its objectives, examples and expected results. Try the short checks before revealing feedback. Python examples are teaching text, not a place to run arbitrary code.</li>
        <li>Use the lesson completion control when you finish. Saved lesson completion records activity; it is not proof of understanding.</li>
        <li>In <Link href="/cyber-lab?tab=learn">Cyber Lab learning</Link>, select the recommended module and work through its topics, reflections and examples. Optional external readings provide more depth; you can study the core material here.</li>
      </ol>
      <h3>Course assessments and topic practice</h3>
      <p>In <Link href="/assessments">Assessments</Link>, select an enrolled course and choose Quick, Standard, Extended or Custom within the available bank. Start the assessment, answer every selected question and submit once. Read the correct-answer explanations and the result’s evidence limits; shorter attempts cover less material. Your owned attempt history remains available.</p>
      <p>In <Link href="/cyber-lab?tab=practice">Cyber Lab practice</Link>, choose a topic, difficulty and session length. Start, answer the selected questions and submit. Fresh practice and review of recent mistakes are different modes; mistake review needs earlier submitted practice. Review the explanation and supporting teaching before another session. The 500-question bank is across all topics, not 500 questions per pathway or a requirement to answer all 500 at once.</p>
    </section>

    <section id="investigations" className={styles.chapter} aria-labelledby="investigations-heading">
      <h2 id="investigations-heading" tabIndex={-1}>5. Play a guided mission</h2>
      <p>There are ten guided investigations per pathway. These are structured evidence-and-decision cases, distinct from the evolving network games.</p>
      <ol>
        <li>Open your pathway’s <Link href="/missions">mission library</Link>, choose a game and press Play game. Read your role, objectives, workflow and current task.</li>
        <li>Open the evidence locker and inspect each record. Read beyond its title: ask what the record establishes and what remains uncertain. Use Need a hint? and its additional hint if needed.</li>
        <li>Select the finding most relevant to this task. Proceed to the decision desk, choose an action and press Commit decision. Read the action and finding explanations.</li>
        <li>Repeat for all three stages. New stages have new evidence and reset their selections. A mistaken answer affects the result and explanation; these missions generally follow authored stages rather than branching into a new network world.</li>
        <li>Review your saved result. Try the five optional review questions, including the explanations for choices you missed. These reviews are ungraded practice and do not change the saved mission score.</li>
      </ol>
      <h3>Using 2D or 3D</h3>
      <p>2D is the lightweight default. Enter the 3D investigation room if desired and use its Inspect artifact controls. Walking is optional. Both views show the same evidence; 3D does not create another mission or change scoring. Switch to the 2D workstation whenever useful. Inspection and finding selection carry between views within the current stage.</p>
      <p>Use Tab to reach controls, Enter or Space to activate buttons, and the normal keyboard controls for radio choices. On a small or slower device, use 2D and the textual records.</p>
    </section>

    <section id="workshops" className={styles.chapter} aria-labelledby="workshops-heading">
      <h2 id="workshops-heading" tabIndex={-1}>6. Play a decision workshop</h2>
      <p>A workshop is a short, saved case with three authored decisions. Each pathway has one allocated workshop per stage, eight overall. It complements full missions and simulations.</p>
      <ol>
        <li>Open the workshop from your stage. Read its briefing and objective, then choose Start saved workshop.</li>
        <li>Read the current situation and choose one offered response. The choice records its explanation and simplified effort; continue through three decisions.</li>
        <li>In Your case review, compare supported findings and unresolved issues. These are authored learning consequences, not measured real-world risk or a mastery score.</li>
        <li>Use Replay and compare another approach after completion. Change your decisions and inspect the comparison with your earlier approach.</li>
      </ol>
      <p>Return through saved workshop history to resume an unfinished case. Select All stages to see your pathway’s eight cases; Browse all workshops deliberately opens the combined library. Your older saved cases remain available even if they belong to another pathway.</p>
    </section>

    <section id="defender" className={styles.chapter} aria-labelledby="defender-heading">
      <h2 id="defender-heading" tabIndex={-1}>7. Play a defender simulation</h2>
      <p>Cyber Lab’s defender games have evolving assets, budgets, staff actions, compromise and service availability. Your choices change what happens. Defend the branch, Supplier Access Crisis, Recovery Under Pressure and Branch Siege have different openings and rules.</p>
      <ol>
        <li>Open the scenario recommended by your pathway. Read its briefing, success conditions, loss conditions and action costs before choosing Start a new shift.</li>
        <li>Inspect the map or asset list. Identify important services, their connections and what the current observations actually show. Quiet monitoring is not proof that everything is clean.</li>
        <li>Select an asset and an available action. Consider the remaining budget and staff, prerequisites and effects. Investigating, patching, monitoring, isolation and restoration solve different problems.</li>
        <li>Choose Advance turn when ready. The incident progresses, delayed work can complete and staff availability refreshes according to the scenario. No clock runs while you are planning.</li>
        <li>Read new observations and the decision timeline. Adapt your response; preserve important service while addressing the relevant entry conditions and existing compromise.</li>
        <li>At the end, read the outcome and debrief. In Branch Siege, use the same-incident replay/comparison to try another strategy against the same opening.</li>
      </ol>
      <p><strong>Example trade-off:</strong> isolating an affected application may restrict spread but interrupt its service and dependent systems. A patch can close a weakness without removing existing compromise. A recovery copy must be verified and the restored system validated before safe reconnection under the scenario’s rules. Read the offered prerequisites rather than repeatedly clicking an unavailable action.</p>
      <p>Branch Siege adds eight assets, uncertain reports, dependent services and delayed work. Check completion turns before assuming a patch or restoration has finished. Its emergency-staff option trades budget for temporary staff capacity. Read this capstone’s own briefing rather than reuse an earlier scenario’s win conditions.</p>
    </section>

    <section id="red-blue" className={styles.chapter} aria-labelledby="red-blue-heading">
      <h2 id="red-blue-heading" tabIndex={-1}>8. Play Red / Blue</h2>
      <p>Red tries to achieve the scenario’s attack objective. Blue tries to prevent it while managing protection and business consequences. Actions are conceptual; the game performs no real scanning, exploitation or malware execution.</p>
      <h3>First, try a computer match</h3>
      <ol>
        <li>Open <Link href="/red-blue">Red / Blue</Link> from your pathway. Choose the scenario, your seat and Rule-based computer. Blue with Easy is a useful first attempt; you can change the selections before starting.</li>
        <li>Press Start match. Read your side’s briefing, the target objective, required hold period and round limit. Difficulty changes the computer’s decisions, not its access to hidden information or resource advantage.</li>
        <li>Inspect known assets using the board or asset list. Read your evidence ledger and action field guide. You only see information available to your seat; an earlier observation can become stale.</li>
        <li>Select one offered action and any required target/source. Check its cost, prerequisites and remaining resources. Press Seal choice when satisfied.</li>
        <li>Both seats choose without seeing the other’s pending order. The round resolves after both have committed: Blue’s action resolves first, then Red’s. In computer play, the computer chooses from its opening information before your commitment takes effect.</li>
        <li>Read the resulting observations and repeat. A plausible action may fail because conditions changed or because the scenario models uncertainty. Follow the evidence instead of assuming the displayed action guarantees success.</li>
        <li>At match end, open the debrief. Compare the timeline, missed evidence and bounded alternative actions. For role reversal, start a new match in the other seat; an existing match does not swap seats.</li>
      </ol>
      <h3>Then play another learner</h3>
      <ol>
        <li>Use two different eligible learner accounts in separate browser profiles or sessions. Do not share one login for both seats.</li>
        <li>The creator chooses Another learner and a seat, then Start match. Choose Create invitation code and share it privately with the other learner.</li>
        <li>The second learner signs in independently, opens Join another learner, enters the Invitation code and presses Join match. The creator’s seat is already assigned; the joining learner takes the other seat.</li>
        <li>Each learner seals one choice per round. The first waits for the other; waiting does not automatically forfeit the game. Do not refresh repeatedly expecting to see the opponent’s hidden order.</li>
        <li>Both participants can reopen the completed debrief. Discuss what each knew when choosing, then create another match with exchanged roles.</li>
      </ol>
      <p>Invitation codes are single-use and expire after 24 hours. Replace invitation code invalidates the previous code. If joining fails, confirm that you are using a different eligible account and a current code. Instructor and spectator access are not enabled.</p>
    </section>

    <section id="progress" className={styles.chapter} aria-labelledby="progress-heading">
      <h2 id="progress-heading" tabIndex={-1}>9. Save, return and move on</h2>
      <p>Saved activities belong to the signed-in account. Use the <Link href="/dashboard">dashboard</Link> and the relevant activity’s history to resume. Course completion, assessment attempts, mission results, workshop decisions, defender runs and Red/Blue matches are separate records. The public preview is unsaved.</p>
      <p>Wait for a saved response before closing. If an action’s acknowledgement is interrupted, use its retry control or reopen saved state; avoid starting a replacement run just to repeat a possibly saved decision. Red/Blue provides Retry same choice for this situation.</p>
      <p>Changing pathway does not erase earlier work. Finish your chosen activity, review its explanation or debrief and decide whether to study, replay or continue. Reaching a later stage is not a competence award. You can return to earlier material or use the stage-eight invitation to explore the next pathway.</p>
    </section>

    <section id="trouble" className={styles.chapter} aria-labelledby="trouble-heading">
      <h2 id="trouble-heading" tabIndex={-1}>10. Get unstuck</h2>
      <ul>
        <li><strong>Cannot start:</strong> sign in with the correct eligible learner account, check the activity’s required selections and read any displayed message.</li>
        <li><strong>Action unavailable:</strong> check prerequisites, budget, staff, current round and whether an earlier choice is already sealed. Unavailable does not mean you need to click faster.</li>
        <li><strong>Nothing happens after sealing:</strong> in a human match, the other seat must also commit. Resume the same saved match after reconnecting.</li>
        <li><strong>3D slow or unavailable:</strong> switch to 2D. Use asset lists and keyboard controls; walking is optional. Reduced-motion preferences are respected by the supported views.</li>
        <li><strong>Session expired or connection lost:</strong> sign in again and reopen your saved activity. A server must acknowledge new work before you can assume it was saved.</li>
        <li><strong>Public beta unavailable:</strong> contact the organiser. The beta may be temporarily offline; do not enter account details on a replacement address you have not verified.</li>
      </ul>
      <p>Use <Link href="/feedback">Feedback</Link> to report the pathway, stage, activity, expected behaviour and what appeared. Include a sanitised screenshot if requested; never include passwords, session tokens, private invitation codes or real customer information.</p>
      <Link className="btn" href="/journey">Choose my pathway →</Link>
    </section>
  </>;
}
