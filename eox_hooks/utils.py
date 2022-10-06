"""
Utils functions for actions.
"""
import collections

from django.conf import settings


def flatten_dict(dictionary, parent_key='', sep='_'):
    """
    This function returns a flatten dictionary-like object.
    """
    items = []
    for key, value in dictionary.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, collections.MutableMapping):
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
