"""Models module for eox-hooks."""
import uuid

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from eox_hooks.constants import Status


@python_2_unicode_compatible
class HookExecutionAudit(models.Model):
    """Model used to audit the eox-hooks actions."""

    key = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="Public identifier",
    )

    status = models.PositiveIntegerField(
        choices=Status.choices(), default=Status.SUCCESS, editable=False,
    )
    executed_at = models.DateTimeField(auto_now_add=True, editable=False)
    hook_name = models.CharField(max_length=150)
    task_name = models.CharField(max_length=150)
    tenant_domain = models.CharField(max_length=150)
    task_duration = models.FloatField(null=True)

    objects = models.Manager()

    def __str__(self):
        return "Execution {key}: Task '{task_name}' executed at {time} with status {status}." \
               .format(key=self.key, task_name=self.task_name, time=self.executed_at, status=self.status)
