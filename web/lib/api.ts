import { parsePathways, type AcademyCard } from './pathways';

/** Public, read-only API client; use AbortSignal to avoid stale UI updates. */
export async function fetchPathways(signal?: AbortSignal): Promise<AcademyCard[]> {
  const base = (process.env.NEXT_PUBLIC_API_BASE_URL || (typeof window === 'undefined' ? 'http://127.0.0.1:3000' : '')).replace(/\/$/, '');
  const response = await fetch(`${base}/api/v1/pathways`, { signal });
  if (!response.ok) throw new Error('API unavailable');
  const payload: unknown = await response.json();
  return parsePathways(payload);
}
