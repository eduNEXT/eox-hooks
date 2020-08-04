"""This file contains all the test for the receivers.py file.

Classes:
    TestReceivers.
"""
from django.conf import settings
from django.test import TestCase, override_settings
from mock import Mock, patch

from eox_hooks.receivers import hooks_handler


class TestReceivers(TestCase):
    """Receivers test class."""

    def setUp(self):
        """Set up class for Receivers testing."""
        self.sender = Mock()
        self.trigger_event = "sender.example"
        self.signal = Mock()

    @patch("eox_hooks.receivers._get_dispatch_uid")
    @patch("eox_hooks.receivers.action_handler")
    def test_trigger_response_action(self, action_handler, get_dispatch_uid):
        """
        Used to test that if USE_EOX_HOOKS is set to true then the handler triggers
        the execution of the action handlers.
        """
        get_dispatch_uid.return_value = ("eox-hooks:sender.example",)
        configuration = settings.EOX_HOOKS_DEFINITIONS.get(self.trigger_event)

        hooks_handler(self.sender, self.signal)

        action_handler.assert_called_once_with("sender.example", configuration, sender=self.sender)

    @patch("eox_hooks.receivers._get_dispatch_uid")
    @patch("eox_hooks.receivers.action_handler")
    def test_with_bad_uid(self, action_handler, get_dispatch_uid):
        """
        Used to test that if USE_EOX_HOOKS is set to true then the handler triggers
        the execution of the action handlers.
        """
        get_dispatch_uid.return_value = ("sender.example",)

        hooks_handler(self.sender, self.signal)

        action_handler.assert_not_called()

    @override_settings(USE_EOX_HOOKS=False)
    @patch("eox_hooks.receivers.action_handler")
    def test_not_trigger_response_action(self, action_handler):
        """
        Used to test that if USE_EOX_HOOKS is set to false then the handler won't trigger
        the execution of the action handlers.
        """
        hooks_handler(self.sender, self.signal)

        action_handler.assert_not_called()

    @override_settings(EOX_HOOKS_DEFINITIONS={})
    def test_without_hooks_configuration_defined(self):
        """
        Used to test what happends if the current tenant is using eox-hooks but there is not a
        configuration defined.

        This should result in the calling of a default action.
        """
        self.assertIsNone(hooks_handler(self.sender, self.signal))
