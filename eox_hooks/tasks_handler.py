"""This module defines the handlers for the tasks triggered by a signal received by eox-hooks."""
import logging
from importlib import import_module

from django.conf import settings

from eox_hooks.constants import Status
from eox_hooks.helpers import Timer
from eox_hooks.models import HookExecutionAudit

log = logging.getLogger(__name__)

DEFAULT_TASK_MODULE = "eox_hooks.tasks"
DEFAULT_TASK_NAME = "default_task"


def task_handler(sender, configuration, **kwargs):
    """
    Function that executes tasks given a specific configuration.
    """
    try:
        module_name, task = configuration.get("task").rsplit(".", 1)
    except AttributeError:
        module_name, task = DEFAULT_TASK_MODULE, DEFAULT_TASK_NAME

    task = task_lookup(module_name, task)
    timer = Timer(configuration.get("timing"))
    try:
        timer.start()
        task(sender=sender, **kwargs)
        execution_time = timer.stop()
        audit_task_execution(Status.SUCCESS, sender, task, execution_time)
    except Exception:  # pylint: disable=broad-except
        audit_task_execution(Status.FAIL, sender, task)


def task_lookup(module_name, task):
    """
    Function that returns a function defined in path, if the path is not find then a default task is
    returned.
    The path must look like: eox_hooks.tasks.default_logging
    Where eox_hooks.tasks is module_name and task_name is default_logging
    """
    try:
        module = import_module(module_name)
    except ImportError:
        log.info("The module {} does not exist with the task {}. A default task will be used."
                 .format(module_name, task))
        module, task = import_module(DEFAULT_TASK_MODULE), DEFAULT_TASK_NAME

    try:
        return getattr(module, task)
    except AttributeError:
        log.info("The task {} does not exist in the module {}. A default task will be used."
                 .format(task, module.__name__))
        module, task = import_module(DEFAULT_TASK_MODULE), DEFAULT_TASK_NAME
        return getattr(module, task)


def audit_task_execution(status, sender, task, execution_time=None):
    """Function that creates an audit entry for the current task execution."""
    audit_entry = HookExecutionAudit.objects.create(
        status=status,
        hook_name=sender,
        task_name=task.__name__,
        tenant_domain=getattr(settings, "EDNX_TENANT_DOMAIN", "default_tenant_domain"),
        task_duration=execution_time
    )
    if status == Status.SUCCESS:
        log.info(str(audit_entry))
    else:
        log.warning(str(audit_entry))
