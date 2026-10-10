"""Idempotent demonstration courses. Run explicitly after Alembic migration."""
from sqlalchemy import select
from database import SessionLocal
from models import Course, Lesson

DEMO = [
    ("cyber", "Cyber Safety Foundations", "Demo course: phishing, passwords, and safe browsing.", [
        ("Recognising phishing", "Phishing messages may impersonate schools, banks or employers. Verify requests through independently located official channels. Never enter passwords through unfamiliar links."),
        ("Protecting your accounts", "Use a unique long password for every account, preferably with a password manager. Enable multifactor authentication where available."),
        ("Safer browsing", "Check website addresses carefully, install updates, and avoid downloading files from untrusted sources.")]),
    ("university", "Introduction to Python", "Demo course: core Python programming concepts.", [
        ("Variables and data types", "Python variables can reference strings, integers, floats and booleans. Example: student_name = 'Ada'."),
        ("Conditional logic", "Use if, elif and else to branch based on conditions. Indentation determines code blocks."),
        ("Loops", "Use for to iterate through sequences and while to repeat while a condition is true.")]),
    ("secondary", "Digital Citizenship Essentials", "Demo course: responsible and secure use of technology.", [
        ("Your digital footprint", "Online posts can persist. Think before sharing information about yourself or others."),
        ("Privacy basics", "Limit sharing of personal details, review privacy settings and ask a trusted adult when uncertain."),
        ("Respectful online conduct", "Communicate respectfully, avoid cyberbullying and report threatening behaviour.")]),
]

def main():
    with SessionLocal() as db:
        for academy_id, title, description, lesson_items in DEMO:
            course = db.scalar(select(Course).where(Course.academy_id == academy_id, Course.title == title))
            if course is None:
                course = Course(academy_id=academy_id, title=title, description=description, status="published")
                db.add(course)
                db.flush()
            for position, (lesson_title, content) in enumerate(lesson_items, 1):
                existing = db.scalar(select(Lesson.id).where(Lesson.course_id == course.id, Lesson.title == lesson_title))
                if existing is None:
                    db.add(Lesson(course_id=course.id, title=lesson_title, content=content, position=position))
        db.commit()
    print("Demo courses ready (existing courses and lessons preserved).")

if __name__ == "__main__":
    main()
