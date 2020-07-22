"""This module defines the signals receivers for defined hooks."""
from importlib import import_module

from django.conf import settings


def pre_enrollment_checking(sender, **kwargs):  # pylint: disable=unused-argument
    """Pre-enrollment signal receiver."""

    if not getattr(settings, "USE_EOX_HOOKS_PRE_ENROLLMENT", False):
        return

    # Here use the custom task defined in settings
    if hasattr(settings, "CUSTOM_PRE_ENROLLMENT_TASK"):
        module_name, task_name = settings.CUSTOM_PRE_ENROLLMENT_TASK.rsplit(".", 1)
        module = import_module(module_name)
        getattr(module, task_name)(**kwargs)
