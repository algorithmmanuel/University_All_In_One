import Link from "next/link";
import { STAGES, journeyUrl } from "../../lib/learning-journey";
import styles from "./journey.module.css";
/** Compact shared entry; detailed choices live in one public journey hub. */
export default function JourneyEntry() {
  return (
    <section className={styles.entry} aria-labelledby="journey-entry-heading">
      <span className="tag">YOUR LEARNING JOURNEY</span>
      <h2 id="journey-entry-heading">
        From first concepts to competing decisions
      </h2>
      <p>
        Begin with the basics or enter at a stage that suits your experience.
        Cyber Explorers, Cyber Academy and Cyber Command help you choose
        materials along the same journey.
      </p>
      <div className={styles.actions}>
        <Link className="btn" href={journeyUrl("discover")}>
          Start from the beginning →
        </Link>
        <Link className="btn secondary" href="/journey#choose-stage">
          I have experience · choose my stage →
        </Link>
      </div>
      <ol className={styles.overview}>
        {STAGES.map((s, i) => (
          <li key={s.id}>
            <Link href={journeyUrl(s.id)}>
              <span>{String(i + 1).padStart(2, "0")}</span>
              {s.title}
            </Link>
          </li>
        ))}
      </ol>
      <p className="small">
        Every stage is available. Use your dashboard to resume saved learning
        and play.
      </p>
    </section>
  );
}
