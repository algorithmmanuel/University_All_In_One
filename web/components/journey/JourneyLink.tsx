"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { activityJourney } from "../../lib/learning-journey";
/** Return to the stage that suggested this activity; carries no completion claim. */
export default function JourneyLink() {
  const [href, setHref] = useState("/journey");
  useEffect(() => {
    setHref(activityJourney(window.location.pathname, window.location.search));
  }, []);
  return <Link href={href}>Learning journey</Link>;
}
