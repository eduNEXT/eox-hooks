"""
Backend file for Course related objects.
"""


def get_load_single_xblock():
    """
    Gets load_single_xblock function from edxapp.

    Returns:
        [Function]: load_single_xblock function.
    """
    from lms.djangoapps.courseware.module_render import load_single_xblock  # pylint: disable=C0415, E0401
    return load_single_xblock


def get_item_not_found_exception():
    """
    Gets ItemNotFoundError exception from edxapp.

    Returns:
        [Class]: ItemNotFoundError exception.
    """
    from xmodule.modulestore.exceptions import ItemNotFoundError  # pylint: disable=C0415, E0401
    return ItemNotFoundError
