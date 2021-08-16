"""
Backend file for Course Modes related objects.
"""


def get_all_course_modes():
    """
    Gets course modes list from edxapp.

    Returns:
        [list]: list of course modes.
    """
    try:
        from course_modes.models import CourseMode  # pylint: disable=import-outside-toplevel
        modes_for_course = CourseMode.ALL_MODES
    except ImportError:
        modes_for_course = [
            "honor",
            "professional",
            "verified",
            "audit",
            "no-id-professional",
            "credit",
            "masters",
        ]
    return modes_for_course
