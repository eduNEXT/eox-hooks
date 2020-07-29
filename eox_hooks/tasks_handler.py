"""This module defines the handlers for the tasks triggered by a signal received by eox-hooks."""
import logging
from importlib import import_module

from celery.task import task as CELERY_TASK

from eox_hooks.constants import Status
from eox_hooks.models import HookExecutionAudit

log = logging.getLogger(__name__)

DEFAULT_TASK_MODULE = "eox_hooks.tasks"
DEFAULT_TASK_NAME = "default_task"


def task_handler(sender, configuration, **kwargs):
    """
    Function that executes tasks given a specific configuration.

    This function also starts the timer for the timing feature and set the tasks as async/sync.
    This given the current configuration.

    # TODO: explain arguments
    """
    if not configuration.get("sync"):
        CELERY_TASK(__task_wrapper).delay(configuration, sender, **kwargs)
    else:
        __task_wrapper(configuration, sender, **kwargs)


def __task_wrapper(configuration, sender, **kwargs):
    """This function `wrappes` the execution with error handling and timing."""
    task = __task_lookup(configuration.get("task"))
    try:
        task(sender=sender, **kwargs)
        __audit_task_execution(Status.SUCCESS, sender, task)
    except Exception:  # pylint: disable=broad-except
        __audit_task_execution(Status.FAIL, sender, task)


def __task_lookup(path):
    """
    Function that returns a function defined in path, if the path is not find then a default task is
    returned.

    The path must look like: eox_hooks.tasks.default_logging
    Where eox_hooks.tasks is module_name and task_name is default_logging
    """
    try:
        module_name, task = path.rsplit(".", 1)
    except AttributeError:
        module_name, task = DEFAULT_TASK_MODULE, DEFAULT_TASK_NAME

    try:
        module = import_module(module_name)
        return getattr(module, task)
    except (ImportError, AttributeError):
        log.info("An error ocurred while getting the task {}, a default task will be used."
                 .format(task))
        module = import_module(DEFAULT_TASK_MODULE)
        return getattr(module, DEFAULT_TASK_NAME)


def __audit_task_execution(status, sender, task, execution_time=None):
    """Function that creates an audit entry for the current task execution."""
    audit_entry = HookExecutionAudit.objects.create(
        status=status,
        hook_name=sender,
        task_name=task.__name__,
        tenant_domain="tenant_domain",
        task_duration=execution_time
    )
    if status == Status.SUCCESS:
        log.info(str(audit_entry))
    else:
        log.warning(str(audit_entry))
