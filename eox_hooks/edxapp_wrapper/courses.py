"""
Courses definitions.
"""

from importlib import import_module

from django.conf import settings


def get_course_overview():
    """
    Gets course overview model from edxapp.
    """

    backend_function = settings.EOX_HOOKS_COURSES_BACKEND
    backend = import_module(backend_function)

    return backend.get_course_overview()
