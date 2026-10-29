"use client";
import { useState } from "react";
import type { Module } from "./types";
import styles from "./lab.module.css";

/** Ungraded local reflection, deliberately separate from saved practice results. */
export default function LessonTopic({
  section,
  onPractice,
}: {
  section: Module["sections"][number];
  onPractice: () => void;
}) {
  const [choice, setChoice] = useState<number | null>(null);
  const [checked, setChecked] = useState(false);
  const [page, setPage] = useState(0);
  const start = page * 5;
  const check = section.check;
  return (
    <section id={"topic-" + section.id} className={styles.topicSection}>
      <h3>{section.title}</h3>
      <p className={styles.muted}>Objective: {section.objective}</p>
      <p>{section.body}</p>
      {section.steps?.map((step) => (
        <div key={step.title}>
          <h4>{step.title}</h4>
          <p>{step.body}</p>
        </div>
      ))}
      {check && (
        <form
          className={styles.reflection}
          onSubmit={(event) => {
            event.preventDefault();
            setChecked(true);
          }}
        >
          <fieldset>
            <legend>Pause and decide: {check.prompt}</legend>
            {check.options.map((option, index) => (
              <label key={option}>
                <input
                  type="radio"
                  name={check.id}
                  checked={choice === index}
                  onChange={() => {
                    setChoice(index);
                    setChecked(false);
                  }}
                />
                {option}
              </label>
            ))}
          </fieldset>
          <button disabled={choice === null}>Check my reasoning</button>
          <p className={styles.muted}>
            Ungraded reflection. This does not change your saved practice
            results.
          </p>
          {checked && (
            <p role="status">
              <strong>
                {choice === check.answer
                  ? "That fits the evidence. "
                  : "Reconsider the evidence. "}
              </strong>
              {check.explanation}
            </p>
          )}
        </form>
      )}
      <details>
        <summary>
          Explore {section.worked_cases.length} worked decisions
        </summary>
        <p role="status">
          Decisions {start + 1}–
          {Math.min(start + 5, section.worked_cases.length)} of{" "}
          {section.worked_cases.length}
        </p>
        {section.worked_cases.slice(start, start + 5).map((item) => (
          <div key={item.situation} className={styles.worked}>
            <h4>{item.situation}</h4>
            <p>{item.reasoning}</p>
          </div>
        ))}
        <div className={styles.pager}>
          <button
            disabled={page === 0}
            onClick={() => setPage((old) => old - 1)}
          >
            Previous decisions
          </button>
          <button
            disabled={start + 5 >= section.worked_cases.length}
            onClick={() => setPage((old) => old + 1)}
          >
            Next decisions
          </button>
        </div>
      </details>
      <p>
        <a href={section.source.url} target="_blank" rel="noopener noreferrer">
          Optional public reading: {section.source.title} ↗
        </a>
      </p>
      <p className={styles.muted}>
        Reference reviewed {section.source.reviewed}. External reading is
        optional; the core teaching is included here.
      </p>
      {!!section.extra_readings?.length && (
        <details>
          <summary>Further implementation reading (advanced)</summary>
          <ul>
            {section.extra_readings.map((source) => (
              <li key={source.url}>
                <a href={source.url} target="_blank" rel="noopener noreferrer">
                  {source.title} ↗
                </a>{" "}
                · reviewed {source.reviewed}
              </li>
            ))}
          </ul>
        </details>
      )}
      <button onClick={onPractice}>Practise this topic →</button>
    </section>
  );
}
