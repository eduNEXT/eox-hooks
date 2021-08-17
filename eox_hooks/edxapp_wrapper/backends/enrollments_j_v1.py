"""
Backend file for Course Enrollment related objects.
"""


def get_course_enrollment():
    """
    Gets Course Enrollment class model from edxapp.

    Returns:
        [Class]: Course Enrollment edxapp model.
    """
    try:
        from student.models import CourseEnrollment  # pylint: disable=import-outside-toplevel
    except ImportError:
        CourseEnrollment = object
    return CourseEnrollment
