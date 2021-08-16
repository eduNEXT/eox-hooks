"""
Course Modes related definitions.
"""

from importlib import import_module

from django.conf import settings


def get_all_course_modes(*args, **kwargs):
    """
    Gets course modes list from edxapp.
    """
    backend_function = settings.EOX_HOOKS_COURSE_MODES_BACKEND
    backend = import_module(backend_function)

    return backend.get_all_course_modes(*args, **kwargs)
