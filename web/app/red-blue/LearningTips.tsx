import type { Action, Match } from "./types";
import styles from "./arena.module.css";

/** Educational suggestions based only on this seat's permitted orders and telemetry. */
export default function LearningTips({
  match, actions, selected,
}: {
  match: Match;
  actions: Action[];
  selected: string;
}) {
  const offered = match.orders.filter((order) =>
    (order.target === selected || order.target === null) &&
    !order.action.startsWith("wait_")
  );
  const alerts = match.observations.filter((event) =>
    event.target === selected && (event.type === "alert" || event.type === "finding")
  );
  const selectedAsset = match.assets.find((asset) => asset.id === selected);
  const example = offered
    .map((order) => ({ order, info: actions.find((action) => action.id === order.action) }))
    .find((item) => item.info);
  return (
    <section className={styles.panel} aria-label="Learning mode coaching">
      <span className={styles.eyebrow}>LEARNING MODE · EDUCATIONAL COACH</span>
      <h3>Think about your next move</h3>
      <p>
        {match.side === "blue"
          ? "Prioritise service continuity, controls and evidence. An alert is an investigation lead, not proof of successful attacker access."
          : "Compare your believed access and dated reconnaissance with your objective. Hidden defensive controls can invalidate an earlier assessment."}
      </p>
      <p>
        {selectedAsset
          ? `For ${selectedAsset.name}, you have ${offered.length} active non-pass choice(s) in the current seat projection.`
          : "Choose a visible asset to review possible decisions."}
        {alerts.length ? ` You have ${alerts.length} recorded alert or finding event(s) for this asset.` : ""}
      </p>
      {example ? (
        <p>
          <strong>One permitted option:</strong> {example.order.action.replaceAll("_", " ")}.
          {" "}{example.info?.explanation} This is a learning prompt, not a claim that the action will succeed.
        </p>
      ) : <p>No targeted action is currently offered. Waiting may be the only permitted decision.</p>}
      <p className={styles.muted}>
        These hints use only your visible inventory, permitted actions, and authorised evidence. Realistic mode hides this assistance.
      </p>
    </section>
  );
}
