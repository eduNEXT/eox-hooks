"""
Backend file for Course Modes related objects.
"""


def get_all_course_modes():
    """
    Gets course modes list from edxapp.

    Returns:
        [list]: list of course modes.
    """
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
