"""This module defines the signals receivers for defined hooks."""
import logging

from django.conf import settings

from eox_hooks.tasks_handler import task_handler

log = logging.getLogger(__name__)

DEFAULT_TASK_MODULE = "eox_hooks.tasks"
DEFAULT_TASK_NAME = "default_task"
DEFAULT_SIGNAL_SENDER = "eox_hooks.default_hook_sender"


def hooks_handler(sender, **kwargs):
    """Eox-hooks signal receiver."""
    if not getattr(settings, "USE_EOX_HOOKS", False):
        return
    try:
        current_sender = sender.__name__
    except AttributeError:
        current_sender = DEFAULT_SIGNAL_SENDER

    if current_sender not in settings.EOX_HOOKS_DEFINITIONS:
        log.warning("Hook with name {} not configured in the current tenant, a default hook will be used."
                    .format(current_sender))

    current_configuration = settings.EOX_HOOKS_DEFINITIONS.get(current_sender, {})
    task_handler(current_sender, current_configuration, **kwargs)
