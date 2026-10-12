"""Add sample quiz questions to the three demonstration courses."""
from sqlalchemy import select
from database import SessionLocal
from models import Course, QuizQuestion
from expanded_quiz_bank import BANK as EXPANDED_BANK

BANK = {
    "Cyber Safety Foundations": [
        ("A scholarship email asks you to log in through an unfamiliar link. What should you do?",
         ["Enter your password", "Verify through the school's official website", "Forward the link to friends"], 1,
         "Verify requests through independently located official channels."),
        ("What best protects an online account?",
         ["Reusing a familiar password", "A unique password and MFA", "Sharing credentials with a trusted friend"], 1,
         "Unique passwords and multifactor authentication reduce account takeover risk."),
        ("A website offers an unexpected software download. What is safest?",
         ["Install immediately", "Disable antivirus", "Verify the source and avoid untrusted downloads"], 2,
         "Untrusted downloads can contain malware.")
    ],
    "Introduction to Python": [
        ("Which Python type represents True or False?", ["str", "bool", "list"], 1,
         "Python uses the bool type for Boolean values."),
        ("Which keyword starts a conditional branch?", ["if", "loop", "switch"], 0,
         "Python uses if for conditional branching."),
        ("Which statement iterates through a sequence?", ["try", "for", "def"], 1,
         "The for statement iterates through items in a sequence.")
    ],
    "Digital Citizenship Essentials": [
        ("What is a digital footprint?", ["Only your device password", "Traces left by online activity", "Your shoe size"], 1,
         "Online activity can leave a lasting record."),
        ("What should you avoid posting publicly?", ["Private identity information", "A general study tip", "A public weather forecast"], 0,
         "Avoid exposing sensitive personal information."),
        ("What is a good response to online bullying?", ["Join in", "Report it to a trusted adult or appropriate service", "Share it widely"], 1,
         "Seek support and report harmful conduct.")
    ]
}

def main():
    with SessionLocal() as db:
        for title, items in BANK.items():
            course = db.scalar(select(Course).where(Course.title == title))
            if course is None:
                print("Missing course:", title, "- run seed_learning.py first")
                continue
            for position, (prompt, options, answer, explanation) in enumerate(items, 1):
                existing = db.scalar(select(QuizQuestion.id).where(
                    QuizQuestion.course_id == course.id, QuizQuestion.prompt == prompt))
                if existing is None:
                    db.add(QuizQuestion(course_id=course.id, prompt=prompt, options=options,
                                        correct_index=answer, explanation=explanation, position=position))
        db.flush()
        for title, items in EXPANDED_BANK.items():
            course = db.scalar(select(Course).where(Course.title == title))
            if course is None:
                continue
            existing_rows = db.scalars(select(QuizQuestion).where(
                QuizQuestion.course_id == course.id).order_by(QuizQuestion.position, QuizQuestion.id)).all()
            prompts = {q.prompt for q in existing_rows}
            remaining = max(0, 50 - len(existing_rows))
            position = max((q.position for q in existing_rows), default=0)
            for prompt, options, answer, explanation in items:
                if remaining == 0:
                    break
                if prompt in prompts:
                    continue
                position += 1
                db.add(QuizQuestion(course_id=course.id, prompt=prompt, options=options,
                                    correct_index=answer, explanation=explanation, position=position))
                prompts.add(prompt)
                remaining -= 1
        db.commit()
    print("Demonstration quizzes expanded to 50 questions per course (existing questions preserved).")

if __name__ == "__main__":
    main()
