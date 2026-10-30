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
from production_learning.explorers_discover import COURSE

def validate(course):
    assert course["revision"] == "v1"
    assert course["academy_id"] == "secondary"
    assert course["pathway"] == "secondary"
    assert course["stage"] == "discover"
    assert len(course["lessons"]) >= 8
    assert len({row["position"] for row in course["lessons"]}) == len(course["lessons"])
    assert len({row["title"] for row in course["lessons"]}) == len(course["lessons"])
    for row in course["lessons"]:
        assert len(row["content"].split()) >= 90, "Reject shallow editorial material"
        assert "Worked example:" in row["content"] or "Reflection:" in row["content"]
    assert "Further reading" in course["lessons"][-1]["content"]

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
    db.commit()
    return "published"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true", help="Explicitly publish the reviewed manuscript")
    args = parser.parse_args()
    validate(COURSE)
    if not args.publish:
        print("DRY RUN: manuscript validated; nothing written.")
        return
    with SessionLocal() as db:
        result = publish(db, COURSE)
        print(result)

if __name__ == "__main__":
    main()
