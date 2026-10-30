import Link from "next/link";
import PlayGuide from "../../components/help/PlayGuide";

export default function HelpPage() {
  return <main className="container section" style={{maxWidth:1100}}>
    <nav aria-label="Help navigation"><Link href="/">Home</Link> · <Link href="/journey">Learning journey</Link> · <Link href="/dashboard">My dashboard</Link></nav>
    <span className="tag">START HERE / PLAYER GUIDE</span>
    <h1>How EduCyber works</h1>
    <p>A practical guide to the three pathways, all eight learning stages, every activity type and saved play. Begin with the first-visit steps or use the contents to find the game you want to play.</p>
    <p>Each pathway will grow through richer materials within these eight stages. Your existing records stay with your account as you study, investigate, defend and reflect.</p>
    <PlayGuide />
  </main>;
}
