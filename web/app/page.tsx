import Link from "next/link";
import { PreviewQuiz } from "../components/home/preview-quiz";
import { GameLibrary } from "../components/home/game-library";
import { AccountNavigation } from "../components/home/account-navigation";
import JourneyEntry from "../components/journey/JourneyEntry";

export default function Home() {
  return (
    <>
      <header className="container nav">
        <div className="brand">
          EduCyber
        </div>
        <div className="header-controls">
          <AccountNavigation />
        </div>
      </header>
      <main>
        <section className="hero">
          <div className="container">
            <span className="pill">Learn at your own starting point</span>
            <h1>
              Understand the risk.
              <br />
              Shape the outcome.
            </h1>
            <p>
              Build cybersecurity knowledge, investigate evidence and make
              consequential decisions. Follow one learning journey, from your
              first concept to a match against another learner.
            </p>
            <div className="actions">
              <Link className="btn" href="/journey?stage=discover&pathway=all">
                Begin my journey →
              </Link>
              <Link className="btn secondary" href="/journey#choose-stage">
                Find my starting point →
              </Link>
            </div>
          </div>
        </section>
        <div className="container section">
          <JourneyEntry />
        </div>
        <PreviewQuiz />
        <GameLibrary />
        <section className="container section">
          <div className="panel">
            <span className="tag">EXPLORE BY ACTIVITY</span>
            <h2>Return to the materials you need</h2>
            <p>
              Use the journey to choose a next step, or open a familiar
              collection directly. Guided missions, defender strategy and Red /
              Blue matches offer different kinds of decisions.
            </p>
            <nav className="actions" aria-label="Learning collections">
              <Link href="/learn">Foundation courses</Link>
              <Link href="/assessments">Course assessments</Link>
              <Link href="/cyber-lab?tab=learn">
                Applied cybersecurity modules
              </Link>
              <Link href="/cyber-lab?tab=practice">
                500-question practice bank
              </Link>
              <Link href="/cyber-lab">Defender strategy scenarios</Link>
              <Link href="/red-blue">Red / Blue simulator</Link>
            </nav>
            <p className="small">
              Saved learning and play require an eligible learner account. All
              scenarios are fictional and conceptual.
            </p>
          </div>
        </section>
      </main>
      <footer className="footer">
        <div className="container">
          EduCyber · Learn, investigate, defend and reflect.
        </div>
      </footer>
    </>
  );
}
