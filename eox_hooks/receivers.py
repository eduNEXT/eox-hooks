"""This module defines the signals receivers for defined hooks."""
import logging

from django.conf import settings

from eox_hooks.actions_handler import action_handler

log = logging.getLogger(__name__)


def _get_dispatch_uid(receivers):
    """
    Generator to read the dispatch_uid, which is in a nested tuple.
    """
    for receiver in receivers:
        try:
            yield receiver[0][0]
        except IndexError:
            pass


def hooks_handler(sender, signal, **kwargs):
    """Eox-hooks signal receiver."""
    if not getattr(settings, "USE_EOX_HOOKS", False) or not settings.EOX_HOOKS_DEFINITIONS:
        return None

    trigger_event = None
    for uid in _get_dispatch_uid(signal.receivers):
        if uid.startswith('eox-hooks:'):
            trigger_event = uid.split(':')[1]
            break

    if trigger_event not in settings.EOX_HOOKS_DEFINITIONS:
        return None

    current_configuration = settings.EOX_HOOKS_DEFINITIONS.get(trigger_event, {})
    return action_handler(trigger_event, current_configuration, sender=sender, **kwargs)
