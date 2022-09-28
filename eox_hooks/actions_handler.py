"""This module defines the handlers for the actions triggered by a signal received by eox-hooks."""
import logging
from importlib import import_module

log = logging.getLogger(__name__)


def action_handler(trigger_event, configuration, **kwargs):
    """
    Function that executes actions given a specific configuration.
    """
    action = action_lookup(
        module_name=configuration.get("module", "missing_module"),
        action=configuration.get("action", ""),
    )

    if not action:
        return None

    action_result = None
    try:
        kwargs["trigger_event"] = trigger_event
        action_result = action(**kwargs)
        log.info("The action %s triggered by %s ended successfully.", action, trigger_event)
    except Exception:  # pylint: disable=broad-except
        log.exception("The action %s triggered by %s failed", action, trigger_event)

        if not configuration.get("fail_silently"):
            raise

    return action_result


def action_lookup(module_name, action):
    """
    Function that returns a function defined in path,
    if the path is not find then a default action is returned.
    The path must look like: eox_hooks.actions.default_logging
    Where eox_hooks.actions is module_name and action_name is default_logging
    """
    try:
        module = import_module(module_name)
        return getattr(module, action)
    except ImportError:
        message = f"The module {module_name} with the action {action} does not exist."
    except AttributeError:
        message = f"The action {action} does not exist in the module {module.__name__}."

    log.error(message)
    return None
