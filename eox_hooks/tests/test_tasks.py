"""This file contains all the test for the tasks.py file.

Classes:
    SingalsTestCase: Test tasks.
"""
from django.test import TestCase
from mock import patch

from eox_hooks.tasks import default_task


class TestTasks(TestCase):
    """Tasks test class."""

    def setUp(self):
        self.kwargs = {
            "course_id": "course_id",
            "username": "username",
        }
        self.sender = "sender.example"

    @patch('eox_hooks.tasks.log.info')
    def test_default_task(self, log):
        """Used to test the correct execution of the default task."""
        default_task(sender=self.sender, **self.kwargs)

        log.assert_called()
