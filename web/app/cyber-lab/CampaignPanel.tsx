"use client";
import type { Catalog, CampaignStep } from "./types";
import styles from "./lab.module.css";

export default function CampaignPanel({
  campaign,
  busy,
  onNext,
}: {
  campaign: NonNullable<Catalog["campaign"]>;
  busy: boolean;
  onNext: (step: CampaignStep) => void;
}) {
  return (
    <section aria-label="Your campaign" className={styles.campaign}>
      <span className={styles.eyebrow}>YOUR DEFENCE CAMPAIGN</span>
      <h3>Learn it. Practise it. Put it under pressure.</h3>
      <p>
        {campaign.completed} of {campaign.total} chapter activity milestones met
      </p>
      <ol className={styles.campaignGrid}>
        {campaign.chapters.map((chapter, index) => (
          <li key={chapter.scenario}>
            <span className={styles.eyebrow}>CHAPTER {index + 1}</span>
            <h4>{chapter.title}</h4>
            <p>{chapter.scenario_title}</p>
            <ul>
              <li>
                {chapter.module_read ? "✓" : "○"} Current module marked read
              </li>
              <li>
                {chapter.practice_distinct >= chapter.practice_target
                  ? "✓"
                  : "○"}{" "}
                {chapter.practice_distinct} distinct supporting questions
                submitted · target {chapter.practice_target}
              </li>
              <li>
                {chapter.wins ? "✓" : "○"} {chapter.wins} saved scenario win
                {chapter.wins === 1 ? "" : "s"}
              </li>
            </ul>
            <button disabled={busy} onClick={() => onNext(chapter.next)}>
              {chapter.next.label} →
            </button>
          </li>
        ))}
      </ol>
      <p className={styles.muted}>{campaign.notice}</p>
    </section>
  );
}
