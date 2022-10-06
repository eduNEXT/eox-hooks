"""
Backend file for Course related objects.
"""

from mock import Mock


def get_load_single_xblock():
    """
    Gets load_single_xblock function from edxapp.

    Returns:
        [Function]: load_single_xblock function.
    """
    return Mock()


def get_item_not_found_exception():
    """
    Gets ItemNotFoundError exception from edxapp.

    Returns:
        [Class]: ItemNotFoundError exception.
    """
    return Exception
