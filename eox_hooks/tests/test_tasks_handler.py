"""This file contains all the test for the tasks_handler.py file.

Classes:
    SingalsTestCase: TestTasksHandler.
"""
from django.test import TestCase, override_settings
from mock import patch

from eox_hooks.tasks_handler import task_handler


@override_settings(USE_EOX_HOOKS=True)
class TestTasksHandler(TestCase):
    """Receivers test class."""

    def setUp(self):
        """Set up class for Receivers testing."""
        self.sender = "sender"
        self.configuration = {
            "task": "eox_hooks.tests.test_utils.custom_task_mock",
        }
