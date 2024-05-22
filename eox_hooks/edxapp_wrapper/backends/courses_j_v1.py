"""
Backend file for Course related objects.
"""
from courseware.module_render import load_single_xblock  # pylint: disable=C0415, E0401


def get_load_single_xblock():
    """
    Gets load_single_xblock function from edxapp.

    Returns:
        [Function]: load_single_xblock function.
    """
    return load_single_xblock


def get_item_not_found_exception():
    """
    Gets ItemNotFoundError exception from edxapp.

    Returns:
        [Class]: ItemNotFoundError exception.
    """
    try:
        from xmodule.modulestore.exceptions import ItemNotFoundError  # pylint: disable=C0415, E0401
    except ImportError:
        ItemNotFoundError = Exception
    return ItemNotFoundError
