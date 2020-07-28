"""This module defines the handlers for the actions triggered by a signal received by eox-hooks."""
import logging
from importlib import import_module

from eox_hooks.tests.test_utils import custom_action_mock

log = logging.getLogger(__name__)


def action_handler(trigget_event, configuration, **kwargs):
    """
    Function that executes actions given a specific configuration.
    """
    action = action_lookup(
        module_name=configuration.get("module", "missing_module"),
        action=configuration.get("action", ""),
    )

    try:
        action(**kwargs)
        log.info("The action {} with triggered by {} ended successfully.".format(action, trigget_event))
    except Exception as exception:  # pylint: disable=broad-except
        log.error("The action {} with triggered by {} failed.".format(action, trigget_event))

        if not configuration.get("fail_silently"):
            raise exception


def action_lookup(module_name, action):
    """
    Function that returns a function defined in path, if the path is not find then a default action is
    returned.
    The path must look like: eox_hooks.actions.default_logging
    Where eox_hooks.actions is module_name and action_name is default_logging
    """
    try:
        module = import_module(module_name)
        return getattr(module, action)
    except ImportError:
        message = "The module {} with the action {} does not exist. A default action will be used."\
                  .format(
                      module_name,
                      action,
                    )
    except AttributeError:
        message = "The action {} does not exist in the module {}. A default action will be used."\
                  .format(
                      action,
                      module.__name__,
                    )

    log.warning(message)
    return custom_action_mock
