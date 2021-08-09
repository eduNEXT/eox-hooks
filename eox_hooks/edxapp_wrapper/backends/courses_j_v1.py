"""
Backend file for Courses.
"""


# pylint: disable=import-error, import-outside-toplevel
def get_course_overview():
    """
    Gets Course Overview class model from edxapp.

    Returns:
        [Class]: Course Overview edxapp model.
    """
    try:
        from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
    except ImportError:
        CourseOverview = object
    return CourseOverview