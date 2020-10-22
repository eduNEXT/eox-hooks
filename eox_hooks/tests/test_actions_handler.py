"""This file contains all the test for the actions_handler.py file.

Classes:
    TestActionHandler.
"""
from django.test import TestCase
from mock import Mock, patch
from testfixtures import LogCapture

from eox_hooks.actions_handler import action_handler, action_lookup


class TestActionHandler(TestCase):
    """ActionHandler test class."""

    def setUp(self):
        """Set up class for ActionHandler testing."""
        self.trigger_event = "trigger_event"
        self.configuration = {
            "module": "eox_hooks.tests.test_utils",
            "action": "custom_action_mock",
            "fail_silently": True,
        }

    @patch("eox_hooks.actions_handler.action_lookup")
    def test_executing_custom_action(self, action_lookup_mock):
        """Used to test executing custom action when hook setting is set to true."""
        action_mock = Mock()
        action_lookup_mock.return_value = action_mock

        action_handler(self.trigger_event, self.configuration)

        action_mock.assert_called_once()

    @patch("eox_hooks.actions_handler.action_lookup")
    def test_action_fail_silently(self, action_lookup_mock):
        """Used to test executing custom action that fails silently."""
        action_mock = Mock()
        action_lookup_mock.return_value = action_mock
        action_mock.side_effect = Exception()
        log_message = "The action {} triggered by {} failed.".format(action_mock,
                                                                     self.trigger_event)

        with LogCapture() as log:
            action_handler(self.trigger_event, self.configuration)
            log.check(("eox_hooks.actions_handler",
                       "ERROR",
                       log_message))

    @patch("eox_hooks.actions_handler.action_lookup")
    def test_action_not_fail_silent(self, action_lookup_mock):
        """
        Used to test raising exception when action failing using the configuration `fail_silently`.
        """
        action_mock = Mock()
        action_mock.side_effect = Exception()
        action_lookup_mock.return_value = action_mock
        configuration = {
            "module": "eox_hooks.tests.test_utils",
            "action": "custom_action_mock",
            "fail_silently": False,
        }

        with self.assertRaises(Exception):
            action_handler(self.trigger_event, configuration)


class TestActionLookup(TestCase):
    """ActionLookup test class."""

    @patch("eox_hooks.tests.test_utils.custom_action_mock")
    def test_return_specified_action(self, custom_action_mock):
        """Used to verify the successful lookup of an existent task."""
        module_name, action = "eox_hooks.tests.test_utils", "custom_action_mock"

        action = action_lookup(module_name, action)

        self.assertEqual(action, custom_action_mock)

    def test_with_non_existent_action(self):
        """Used to test what happends if a non-existent action is passed."""
        module_name, action = "eox_hooks.tests.test_utils", "non_existent_action"
        log_message = "The action {} does not exist in the module {}.".format(
            action,
            module_name,
        )

        with LogCapture() as log:
            action = action_lookup(module_name, action)
            log.check(("eox_hooks.actions_handler",
                       "ERROR",
                       log_message))

    def test_with_non_existent_module(self):
        """Used to test what happends if a non-existent module is passed."""
        module_name, action = "non_existent_module", "custom_action_mock"
        log_message = "The module {} with the action {} does not exist.".format(
            module_name,
            action,
        )

        with LogCapture() as log:
            action = action_lookup(module_name, action)
            log.check(("eox_hooks.actions_handler",
                       "ERROR",
                       log_message))
