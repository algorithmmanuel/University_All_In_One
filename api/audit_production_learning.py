"""Read-only, whole-library editorial duplication inventory.

Usage (from repository root):
  python api/audit_production_learning.py --output exports/editorial_audit.json
  python api/audit_production_learning.py --check

A repeated run of 70 normalised words may produce many overlapping windows.
This tool groups *adjacent* repeated windows into source-passage clusters so
editors fix the underlying lesson, rather than 677 individual windows.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STAGES = ("discover", "understand", "check", "investigate", "defend",
          "command", "opponent", "compete")
PREFIXES = ("explorers", "academy", "command")
WINDOW = 70


def load_courses(directory: Path = ROOT / "production_learning") -> list[dict]:
    courses = []
    for prefix in PREFIXES:
        for stage in STAGES:
            path = directory / f"{prefix}_{stage}.py"
            if not path.is_file():
                raise FileNotFoundError(f"Missing course manuscript: {path}")
            spec = importlib.util.spec_from_file_location(
                f"editorial_{prefix}_{stage}", path
            )
            if spec is None or spec.loader is None:
                raise RuntimeError(f"Cannot read manuscript {path}")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            courses.append(module.COURSE)
    return courses


def audit(courses: list[dict], window: int = WINDOW) -> dict:
    if window < 2:
        raise ValueError("window must be at least 2")
    lessons = {}
    course_word_counts = defaultdict(list)
    for course in courses:
        for lesson in course["lessons"]:
            key = f'{course["key"]}:{lesson["position"]}'
            if key in lessons:
                raise ValueError(f"Duplicate lesson identity: {key}")
            words = re.findall(r"[a-z0-9]+", lesson["content"].casefold())
            lessons[key] = {"tokens": words, "title": lesson["title"],
                            "course": course["key"]}
            course_word_counts[course["key"]].append(
                len(lesson["content"].split())
            )

    # Index every window, but only retain ones copied into another lesson.
    occurrences = defaultdict(list)
    for key, item in lessons.items():
        tokens = item["tokens"]
        for start in range(len(tokens) - window + 1):
            occurrences[tuple(tokens[start:start + window])].append((key, start))
    repeated = {
        sequence: sites for sequence, sites in occurrences.items()
        if len({key for key, _ in sites}) > 1
    }

    # Union overlapping windows within the same source text. This converts
    # tens of sliding-window hits into one editorial passage cluster.
    parent = {sequence: sequence for sequence in repeated}

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    for key, item in lessons.items():
        tokens = item["tokens"]
        previous = None
        previous_start = -2
        for start in range(len(tokens) - window + 1):
            current = tuple(tokens[start:start + window])
            if current not in repeated:
                previous = None
                continue
            if previous is not None and previous_start == start - 1:
                union(previous, current)
            previous, previous_start = current, start

    groups = defaultdict(lambda: {"sequences": set(), "locations": set(),
                                  "windows": 0, "sample": ""})
    for sequence, sites in repeated.items():
        group = groups[find(sequence)]
        group["sequences"].add(sequence)
        group["windows"] += 1
        group["locations"].update(key for key, _ in sites)
        if not group["sample"]:
            group["sample"] = " ".join(sequence[:22])

    clusters = [
        {"window_count": group["windows"],
         "lesson_count": len(group["locations"]),
         "locations": sorted(group["locations"]),
         "opening_words": group["sample"]}
        for group in groups.values()
    ]
    clusters.sort(key=lambda c: (-c["window_count"], -c["lesson_count"],
                                 c["opening_words"]))
    for idx, group in enumerate(clusters, 1):
        group["id"] = f"R{idx:03d}"

    course_summary = {}
    for course, counts in sorted(course_word_counts.items()):
        relevant = [group for group in clusters if any(
            loc.startswith(course + ":") for loc in group["locations"]
        )]
        course_summary[course] = {
            "lessons": len(counts),
            "minimum_words": min(counts),
            "affected_passage_clusters": len(relevant),
            "affected_lessons": len({
                loc for group in relevant for loc in group["locations"]
                if loc.startswith(course + ":")
            }),
        }
    return {
        "course_count": len(courses),
        "lesson_count": len(lessons),
        "window_words": window,
        "duplicated_window_signatures": len(repeated),
        "passage_cluster_count": len(clusters),
        "courses": course_summary,
        "clusters": clusters,
        "note": "Exact token overlap only; human editors must review semantic similarity.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write JSON report to this path")
    parser.add_argument("--check", action="store_true",
                        help="Exit nonzero when duplicate passages remain")
    args = parser.parse_args()
    result = audit(load_courses())
    summary = {key: result[key] for key in (
        "course_count", "lesson_count", "duplicated_window_signatures",
        "passage_cluster_count"
    )}
    print(json.dumps(summary, indent=2))
    for course, item in result["courses"].items():
        if item["affected_passage_clusters"]:
            print(f"{course}: {item['affected_passage_clusters']} clusters; "
                  f"{item['affected_lessons']} affected lessons")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n",
                               encoding="utf-8")
        print(f"Report: {args.output}")
    return 1 if args.check and result["duplicated_window_signatures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
