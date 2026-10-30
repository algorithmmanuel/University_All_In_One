/** Move to a newly opened workspace without a second browser-generated scroll. */
export function focusActivity(element: HTMLElement | null, reducedMotion: boolean): void {
  if (!element) return;
  element.focus({ preventScroll: true });
  element.scrollIntoView({ behavior: reducedMotion ? 'instant' : 'smooth', block: 'start' });
}
