/** Typed public pathway catalogue. Never trust an API response without validation. */
export type AcademyId = 'secondary' | 'university' | 'professional';
export type AcademyCard = {
  id: AcademyId;
  icon: string;
  title: string;
  description: string;
  topics: string[];
};
export type PathwayResponse = {
  version: number;
  domain: string;
  pathways: Array<{
    id: AcademyId;
    title: string;
    description: string;
    learning_objectives: string[];
  }>;
};

export const fallbackAcademies: AcademyCard[] = [
  { id: 'secondary', icon: '🛡️', title: 'Cyber Explorers', description: 'Age-appropriate digital safety and defensive cybersecurity.', topics: ['Recognize phishing', 'Protect accounts', 'Respect online privacy'] },
  { id: 'university', icon: '💻', title: 'Cyber Academy', description: 'Applied foundations in networks, secure coding and incident investigation.', topics: ['Analyze security alerts', 'Correlate evidence', 'Practice secure development'] },
  { id: 'professional', icon: '🎯', title: 'Cyber Command', description: 'Cyber defense, incident command, governance and resilience simulations.', topics: ['Prioritize incidents', 'Coordinate containment', 'Plan recovery'] },
];

function isPathway(value: unknown): value is PathwayResponse['pathways'][number] {
  if (typeof value !== 'object' || value === null) return false;
  const item = value as Record<string, unknown>;
  return typeof item.id === 'string'
    && typeof item.title === 'string'
    && typeof item.description === 'string'
    && Array.isArray(item.learning_objectives)
    && item.learning_objectives.every(topic => typeof topic === 'string');
}

/** Validate public API data before rendering. Reject incomplete catalogues. */
export function parsePathways(value: unknown): AcademyCard[] {
  if (typeof value !== 'object' || value === null) throw new Error('Invalid pathway response');
  const data = value as Record<string, unknown>;
  if (data.domain !== 'cybersecurity' || !Array.isArray(data.pathways)
      || !data.pathways.every(isPathway)) throw new Error('Invalid pathway response');
  const paths = new Map(data.pathways.map(path => [path.id, path]));
  if (!fallbackAcademies.every(academy => paths.has(academy.id))) {
    throw new Error('Incomplete pathway catalogue');
  }
  return fallbackAcademies.map(academy => {
    const path = paths.get(academy.id)!;
    return { ...academy, title: path.title, description: path.description, topics: path.learning_objectives };
  });
}
