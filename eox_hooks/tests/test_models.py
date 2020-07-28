"""This file contains all the test for the general models.py file.

Classes:
    TestAuditModel: Test HookExecutionAudit.
"""
import time

from django.test import TestCase

from eox_hooks.constants import Status
from eox_hooks.models import HookExecutionAudit


class TestAuditModel(TestCase):
    """Test class for hooks execution audit model."""

    def test_create_audit_entry_with_timing(self):
        """Used to test the successful creation of an audit entry."""
        audit_entry = HookExecutionAudit.objects.create(
            status=Status.SUCCESS,
            hook_name="hook_name",
            task_name="task_name",
            tenant_domain="tenant_domain",
            task_duration=time.time(),

        )

        self.assertIsNotNone(audit_entry.id)

    def test_create_audit_entry_without_timing(self):
        """Used to test the successful creation of an audit entry."""
        audit_entry = HookExecutionAudit.objects.create(
            status=Status.SUCCESS,
            hook_name="hook_name",
            task_name="task_name",
            tenant_domain="tenant_domain",
        )

        self.assertIsNotNone(audit_entry.id)
