"""
Course related definitions.
"""

from importlib import import_module

from django.conf import settings


def get_load_single_xblock(*args, **kwargs):
    """
    Gets load_single_xblock function from edxapp.
    """
    backend_function = settings.EOX_HOOKS_COURSES_BACKEND
    backend = import_module(backend_function)

    return backend.get_load_single_xblock(*args, **kwargs)


def get_item_not_found_exception():
    """
    Gets ItemNotFoundError exception from edxapp.
    """
    backend_function = settings.EOX_HOOKS_COURSES_BACKEND
    backend = import_module(backend_function)

    return backend.get_item_not_found_exception()
