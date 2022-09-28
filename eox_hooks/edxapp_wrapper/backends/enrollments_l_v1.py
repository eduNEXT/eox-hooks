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
        from common.djangoapps.student.models import CourseEnrollment  # pylint: disable=C0415
    except ImportError:
        CourseEnrollment = object
    return CourseEnrollment
