"""This module defines generic tasks for defined hooks."""
import logging

from celery import Task
from eox_hooks.constants import Status
from eox_hooks.models import HookExecutionAudit

log = logging.getLogger(__name__)


class BaseTask(Task):
    """Base task for all tasks defined for hooks."""
    abstract = True

    def __init__(self):
        self.execution_time = None

    def on_failure(self, retval, task_id, args, kwargs):
        audit_entry = HookExecutionAudit.objects.create(
            status=Status.FAIL,
            hook_name=kwargs.pop("sender"),
            task_name=self.__name__,
            tenant_domain="tenant_domain",
        )
        log.warning(str(audit_entry))

    def on_success(self, retval, task_id, args, kwargs):
        audit_entry = HookExecutionAudit.objects.create(
            status=Status.SUCCESS,
            hook_name=kwargs.pop("sender"),
            task_name=self.__name__,
            tenant_domain="tenant_domain",
            task_duration=self.execution_time,
        )
        log.info(str(audit_entry))


class DefaultTask(BaseTask):
    """
    Default task called when:

    - The signal handler receives a signal that is not defined.
    - The module/task defined in the configurations does not exist.
    - The current tenant does not have the correct settings.
    """

    def run(self, **kwargs):
        sender = kwargs.pop("sender")

        log.info("This logging task was triggered by {} with the following arguments: {}"
                .format(sender, str(kwargs)))
