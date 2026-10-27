"""Fixed, source-reviewed curriculum releases; never import from request input.

A release is selected by both academy and course title. Existing release modules
must remain available while database lesson markers still reference their version.
"""
import cyber_foundations
import digital_citizenship
import python_foundations

RELEASES = {
    'python': python_foundations,
    'cyber': cyber_foundations,
    'citizenship': digital_citizenship,
}


def release_for(course):
    return next((release for release in RELEASES.values()
                 if course.academy_id == release.ACADEMY_ID and
                 course.title == release.COURSE_TITLE), None)
