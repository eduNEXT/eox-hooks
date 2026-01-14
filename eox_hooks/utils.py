"""
Utils functions for actions.
"""
import collections

from django.conf import settings


class FakeRequest:
    """
    This class represents a fake request, this is needed when the action
    "trigger_grades_assignment" is executed in an async server.
    """
    META = {}

    @staticmethod
    def is_secure():
        """
        Returns a True to mock-up https.
        """
        return True

    @staticmethod
    def get_host():
        """
        Returns a string with the site name to mock-up the host.
        """
        return settings.SITE_NAME


def flatten_dict(dictionary, parent_key='', sep='_'):
    """
    This function returns a flatten dictionary-like object.
    """
    items = []
    for key, value in dictionary.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, collections.abc.MutableMapping):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def get_trigger_settings(trigger_event):
    """
    This functions returns the settings of a specific trigger event
    defined inside the config dictionary, in the EOX_HOOKS_DEFINITIONS settings.

    For example, if the trigger name is trigger_event, then add your configurations
    in the trigger dictionary as follows:
    "trigger_event": {
        "config" : {
            ...
        }
        ...
    }

    Arguments:
        - trigger_event: Name of the trigger event whose settings you want to return.

    Returns:
        - dictionary.
    """
    return settings.EOX_HOOKS_DEFINITIONS.get(trigger_event, {}).get('config', {})


def _get_course(course_key):
    """Returns a course given its key."""
    from xmodule.modulestore.django import modulestore  # pylint: disable=import-error,import-outside-toplevel

    return modulestore().get_course(course_key)


def unflatten_dict(flat_dict, delimiter='.'):
    """
    Expands a flat dictionary with delimited keys into a nested dictionary structure.

    This function iterates through keys containing a specific delimiter (default is '.')
    and creates the corresponding nested dictionary tree. It is particularly useful
    for converting flat configuration files or environment variables into structured
    JSON-like objects.

    Args:
        flat_dict (dict): The dictionary with flat, delimited keys.
        delimiter (str): The character used to separate nested levels. Defaults to '.'.

    Returns:
        dict: A deeply nested dictionary representing the original hierarchy.

    Example:
        >>> flat_data = {
        ...     "base.footer.logo_url": "https://edunext.co",
        ...     "base.footer.copy": "All rights reserved",
        ...     "foo": "eduNEXT"
        ... }
        >>> unflatten_dict(flat_data)
        {
            'base': {
                'footer': {
                    'logo_url': 'https://edunext.co',
                    'copy': 'All rights reserved'
                }
            },
            'foo': 'eduNEXT'
        }
    """
    unflattened = {}

    for key, value in flat_dict.items():
        parts = key.split(delimiter)
        target = unflattened

        # Traverse/create the path for all parts except the leaf
        for part in parts[:-1]:
            target = target.setdefault(part, {})

        # Assign the final value to the leaf key
        target[parts[-1]] = value

    return unflattened
