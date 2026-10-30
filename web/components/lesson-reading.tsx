/** Render authored plain-text lessons without HTML injection.
 * Only absolute HTTPS addresses become external reading links.
 */
import type { ReactNode } from 'react';

const URLS = /(https:\/\/[^\s<>()[\]{}"']+)/g;

export default function LessonReading({ content }: { content: string }) {
  const parts = content.split(URLS);
  const output: ReactNode[] = parts.map((part,index) => {
    if (part.startsWith('https://')) {
      const clean = part.replace(/[.,;!?]+$/,'');
      const tail = part.slice(clean.length);
      try {
        const u = new URL(clean);
        if (u.protocol === 'https:' && u.hostname && !u.username && !u.password) {
          return <span key={index}><a href={clean} target="_blank" rel="noopener noreferrer">{u.hostname} (external resource)</a>{tail}</span>;
        }
      } catch {
        // Invalid URLs remain ordinary text.
      }
    }
    return <span key={index}>{part}</span>;
  });
  return <div className="lesson-reading" style={{whiteSpace:'pre-wrap',lineHeight:1.85,overflowWrap:'anywhere'}}>{output}</div>;
}
