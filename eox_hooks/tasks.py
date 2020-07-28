"""This module defines generic tasks for defined hooks."""
import logging

log = logging.getLogger(__name__)


def default_task(**kwargs):
    """
    Default task called when:

    - The signal handler receives a signal that is not defined.
    - The module/task defined in the configurations does not exist.
    - The current tenant does not have the correct settings.
    """
    sender = kwargs.pop("sender")

    log.info("This logging task was triggered by {} with the following arguments: {}"
             .format(sender, str(kwargs)))
