"""This module defines generic actions for defined hooks."""
import logging

log = logging.getLogger(__name__)


def default_action(**kwargs):
    """
    Default action called when:
    - The signal handler receives a signal that is not defined.
    - The module/action defined in the configurations does not exist.
    - The current tenant does not have the correct settings.
    """
    sender = kwargs.pop("sender")

    log.info("This logging action was triggered by {} with the following arguments: {}"
             .format(sender, str(kwargs)))
