import { Suspense } from "react";
import { PreviewQuiz } from "../../components/home/preview-quiz";
export default function PreviewPage() {return <main><Suspense fallback={<p className="container section">Loading preview…</p>}><PreviewQuiz /></Suspense></main>;}
