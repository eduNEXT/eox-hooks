"""This file contains all the test for the tasks.py file.
Classes:
    SingalsTestCase: Test tasks.
"""
from django.test import TestCase
from testfixtures import LogCapture

from eox_hooks.actions import default_action


class TestActionss(TestCase):
    """Tasks test class."""

    def setUp(self):
        self.kwargs = {
            "course_id": "course_id",
            "username": "username",
        }
        self.sender = "sender.example"

    def test_default_action(self):
        """Used to test the correct execution of the default action."""
        message = "This logging action was triggered by sender.example with the following arguments: {}" \
                  .format(str(self.kwargs))

        with LogCapture() as log:
            default_action(sender=self.sender, **self.kwargs)
            log.check(("eox_hooks.actions",
                       "INFO",
                       message))
