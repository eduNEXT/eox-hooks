"""This file contains all the test for the general models.py file.

Classes:
    TestAuditModel: Test HookExecutionAudit.
"""
import datetime
import time

from django.test import TestCase

from eox_hooks.constants import Status
from eox_hooks.models import HookExecutionAudit


class TestAuditModel(TestCase):
    """Test class for hooks execution audit model."""

    def test_string_method(self):
        """Function that checks the correct behavior of the str model method."""
        audit_entry = HookExecutionAudit.objects.create(
            status=Status.SUCCESS,
            trigger_event="trigger_event",
            action_name="action_name",
            tenant_domain="tenant_domain",
            action_duration=datetime.timedelta(seconds=time.time()),
        )

        expected_output = "Execution {key}: Action '{action_name}' executed at {time} with status {status}." .format(
            key=audit_entry.key,
            action_name=audit_entry.action_name,
            time=audit_entry.executed_at,
            status=audit_entry.status.name,
        )
        self.assertEqual(expected_output, str(audit_entry))
