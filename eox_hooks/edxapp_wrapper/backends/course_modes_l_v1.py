"""
Backend file for Course Modes related objects.
"""
from common.djangoapps.course_modes.models import CourseMode  # pylint: disable=C0415, E0401


def get_all_course_modes():
    """
    Gets course modes list from edxapp.

    Returns:
        [list]: list of course modes.
    """
    modes_for_course = CourseMode.ALL_MODES
    return modes_for_course
