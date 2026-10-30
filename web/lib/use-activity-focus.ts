'use client';
import { useEffect, useRef } from 'react';
import { focusActivity } from './activity-focus';

/** Increment trigger only after a deliberate open/resume has loaded successfully. */
export function useActivityFocus(trigger: number) {
  const heading = useRef<HTMLHeadingElement>(null);
  useEffect(() => {
    if (trigger === 0) return;
    const frame = window.requestAnimationFrame(() => {
      focusActivity(heading.current, window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    });
    return () => window.cancelAnimationFrame(frame);
  }, [trigger]);
  return heading;
}
