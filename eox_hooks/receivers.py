"""This module defines the signals receivers for defined hooks."""
import logging
from importlib import import_module

from django.conf import settings

from eox_hooks.constants import Status
from eox_hooks.models import HookExecutionAudit

log = logging.getLogger(__name__)

DEFAULT_TASK_MODULE = "eox_hooks.tasks"
DEFAULT_TASK_NAME = "default_task"


def hooks_handler(sender, **kwargs):
    """Eox-hooks signal receiver."""
    if not getattr(settings, "USE_EOX_HOOKS", False):
        return

    try:
        current_sender = sender.__name__
    except AttributeError:
        current_sender = None  # what should I do here?

    if current_sender not in settings.EOX_HOOKS_DEFINITIONS:
        log.warning("Hook with name {} not configured in the current tenant, a default hook will be used."
                    .format(current_sender))

    current_configuration = settings.EOX_HOOKS_DEFINITIONS.get(current_sender)
    current_configuration = __check_current_configuration(current_configuration)
    __task_executer(current_configuration, current_sender, **kwargs)


def __task_executer(configuration, sender, **kwargs):
    """
    Function that executes tasks given a specific configuration.

    This function also starts the timer for the timing feature and set the tasks as async/sync.
    This given the current configuration.
    """
    task = configuration.get("task")
    try:
        task(**kwargs)
        audit_entry = HookExecutionAudit.objects.create(
            status=Status.SUCCESS,
            hook_name=sender,
            task_name=task.__name__,
            tenant_domain="tenant_domain"
        )
        log.info(str(audit_entry))
    except Exception:  # pylint: disable=broad-except
        audit_entry = HookExecutionAudit.objects.create(
            status=Status.FAIL,
            hook_name=sender,
            task_name=task.__name__,
            tenant_domain="tenant_domain"
        )
        log.warning(str(audit_entry))


def __check_current_configuration(configuration):
    """
    TODO: fix this docstring
    Function that makes sure that the configuration passed has the correct fields.
    """
    if not configuration:
        configuration = {}

    configuration["task"] = __task_lookup(configuration.get("task"))

    if not configuration.get("timing"):
        log.info("The task {} will be executed without timing.".format(configuration.get("task")))

    if not configuration.get("async"):
        log.info("The task {} will be executed asynchronously.".format(configuration.get("task")))

    return configuration


def __task_lookup(path):
    """
    Function that returns a function defined in path, if the path is not find then a default task is
    returned.

    The path must look like: eox_hooks.tasks.default_logging
    Where eox_hooks.tasks is module_name and task_name is default_logging
    """
    try:
        module_name, current_task = path.rsplit(".", 1)
    except AttributeError:
        module_name, current_task = DEFAULT_TASK_MODULE, DEFAULT_TASK_NAME

    try:
        module = import_module(module_name)
        return getattr(module, current_task)
    except (ImportError, AttributeError):
        log.info("An error ocurred while getting the task {}, a default task will be used."
                 .format(current_task))
        module = import_module(DEFAULT_TASK_MODULE)
        return getattr(module, DEFAULT_TASK_NAME)
