"""This file contains all the test for the receivers.py file.

Classes:
    SingalsTestCase: Test Receivers.
"""
from django.test import TestCase, override_settings
from mock import Mock, patch

from eox_hooks.receivers import hooks_handler


@override_settings(
    EOX_HOOKS_DEFINITIONS={
        "sender.example": {
            "task": "eox_hooks.tests.test_utils.custom_task_mock",
        },
    },
    USE_EOX_HOOKS=True)
class TestReceivers(TestCase):
    """Receivers test class."""

    def setUp(self):
        """Set up class for Receivers testing."""
        self.sender = Mock()
        self.sender.__name__ = "sender.example"

    @patch('eox_hooks.receivers.log.warning')
    def test_sender_not_in_config(self, log):
        """Used to test what happends if the sender is not defined."""
        self.sender.__name__ = "non_existant_sender.example"

        hooks_handler(self.sender)

        log.assert_called()
