"""Non-destructive publication of individually approved reading courses.

Default is read-only preview. Explicit --publish only after editorial review,
database backup, and integration testing in the isolated development database.
Never deletes or rewrites an enrolled course or existing lesson content.
"""
import argparse
import sys
from pathlib import Path
from sqlalchemy import select
from database import SessionLocal
from models import Academy, Course, Lesson

sys.path.insert(0, str(Path(__file__).resolve().parent))
from production_learning.explorers_discover import COURSE as EXPLORERS
from production_learning.academy_discover import COURSE as ACADEMY
from production_learning.command_discover import COURSE as COMMAND
from production_learning.explorers_understand import COURSE as EXPLORERS_UNDERSTAND
from production_learning.explorers_check import COURSE as EXPLORERS_CHECK
from production_learning.explorers_investigate import COURSE as EXPLORERS_INVESTIGATE
from production_learning.explorers_defend import COURSE as EXPLORERS_DEFEND
from production_learning.explorers_command import COURSE as EXPLORERS_COMMAND
from production_learning.explorers_opponent import COURSE as EXPLORERS_OPPONENT
from production_learning.explorers_compete import COURSE as EXPLORERS_COMPETE
from production_learning.academy_understand import COURSE as ACADEMY_UNDERSTAND
from production_learning.academy_check import COURSE as ACADEMY_CHECK
from production_learning.academy_investigate import COURSE as ACADEMY_INVESTIGATE
from production_learning.academy_defend import COURSE as ACADEMY_DEFEND
from production_learning.academy_command import COURSE as ACADEMY_COMMAND
from production_learning.academy_opponent import COURSE as ACADEMY_OPPONENT
COURSES = [EXPLORERS, ACADEMY, COMMAND, EXPLORERS_UNDERSTAND, EXPLORERS_CHECK, EXPLORERS_INVESTIGATE, EXPLORERS_DEFEND, EXPLORERS_COMMAND, EXPLORERS_OPPONENT, EXPLORERS_COMPETE, ACADEMY_UNDERSTAND, ACADEMY_CHECK, ACADEMY_INVESTIGATE, ACADEMY_DEFEND, ACADEMY_COMMAND, ACADEMY_OPPONENT]
REQUIRED_RELEASE_COURSES = 24
PATHWAYS = {"secondary": "secondary", "university": "university", "professional": "cyber"}
STAGES = {"discover", "understand", "check", "investigate", "defend", "command", "opponent", "compete"}

def validate(course):
    if course["revision"] != "v1":
        raise ValueError("Expected approved content revision v1")
    if course["academy_id"] not in ("secondary","university","cyber"):
        raise ValueError("Unknown academy")
    if course["pathway"] not in ("secondary","university","professional"):
        raise ValueError("Unknown pathway")
    if course["stage"] not in ("discover","understand","check","investigate","defend","command","opponent","compete"):
        raise ValueError("Unknown stage")
    if not (8 <= len(course["lessons"]) <= 12):
        raise ValueError("Every released course must contain 8-12 reviewed lessons")
    if course["academy_id"] != PATHWAYS[course["pathway"]]:
        raise ValueError("Pathway and academy disagree")
    if [row["position"] for row in course["lessons"]] != list(range(1, len(course["lessons"]) + 1)):
        raise ValueError("Lesson positions must be contiguous and one-indexed")
    if len({row["title"] for row in course["lessons"]}) != len(course["lessons"]):
        raise ValueError("Duplicate lesson titles")
    for row in course["lessons"]:
        if len(row["content"].split()) < 600:
            raise ValueError(f"Lesson below 600-word editorial minimum: {course['title']} / {row['title']}")
        if not ("Worked example:" in row["content"] or "Reflection:" in row["content"]):
            raise ValueError("Lesson lacks worked example/reflection")
    if "Further reading" not in course["lessons"][-1]["content"]:
        raise ValueError("Final lesson lacks further reading")

def publish(db, course):
    validate(course)
    academy = db.get(Academy, course["academy_id"])
    if academy is None:
        raise RuntimeError("Expected academy missing; do not create or modify account roles")
    old = db.scalar(select(Course).where(Course.academy_id == course["academy_id"], Course.title == course["title"]))
    if old is not None:
        rows = db.scalars(select(Lesson).where(Lesson.course_id == old.id).order_by(Lesson.position)).all()
        expected = course["lessons"]
        if old.description != course["description"] or len(rows) != len(expected) or any(
            row.position != expected[i]["position"] or row.title != expected[i]["title"] or row.content != expected[i]["content"]
            for i, row in enumerate(rows)
        ):
            raise RuntimeError("Course already exists with different content; use reviewed versioned migration")
        return "unchanged"
    new = Course(academy_id=course["academy_id"], title=course["title"], description=course["description"], status="published")
    db.add(new)
    db.flush()
    for item in course["lessons"]:
        db.add(Lesson(course_id=new.id, title=item["title"], content=item["content"], position=item["position"]))
    return "staged"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true", help="Explicitly publish the reviewed manuscript")
    args = parser.parse_args()
    ids = {(course["pathway"], course["stage"]) for course in COURSES}
    if len(ids) != len(COURSES):
        raise RuntimeError("Duplicate pathway/stage publication mapping")
    required = {(path, stage) for path in PATHWAYS for stage in STAGES}
    if len(COURSES) == REQUIRED_RELEASE_COURSES and ids != required:
        raise RuntimeError(f"Missing or unexpected pathway/stage courses: {required.symmetric_difference(ids)}")
    if len({(course["academy_id"], course["title"]) for course in COURSES}) != len(COURSES):
        raise RuntimeError("Duplicate course title in the same academy")
    failures = []
    for course in COURSES:
        try:
            validate(course)
        except (AssertionError, ValueError) as exc:
            failures.append((course["key"], str(exc)))
    print(f"Editorial audit: {len(COURSES)}/{REQUIRED_RELEASE_COURSES} courses registered; {len(failures)} invalid")
    for key, reason in failures:
        print(f"  NOT READY {key}: {reason}")
    if len(COURSES) != REQUIRED_RELEASE_COURSES or failures:
        if args.publish:
            raise RuntimeError("Refusing incomplete or noncompliant 24-course publication")
        print("DRY RUN ONLY. No database writes.")
        return
    if not args.publish:
        print("DRY RUN: complete manuscript set validated; nothing written.")
        return
    with SessionLocal() as db:
        try:
            results = [(course["key"], publish(db, course)) for course in COURSES]
            db.commit()  # All 24 publish or none; never commit partial content.
        except Exception:
            db.rollback()
            raise
        for key, result in results:
            print(key, result)

if __name__ == "__main__":
    main()
