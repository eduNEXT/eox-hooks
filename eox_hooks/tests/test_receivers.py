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

    @patch("eox_hooks.tests.test_utils.custom_task_mock")
    def test_executing_custom_task(self, custom_task_mock):
        """Used to test executing custom task when hook setting is set to true."""
        custom_task_mock.__name__ = "custom_task_mock"

        hooks_handler(self.sender)

        custom_task_mock.assert_called()

    @override_settings(USE_EOX_HOOKS=False)
    @patch("eox_hooks.tests.test_utils.custom_task_mock")
    def test_not_executing_custom_task(self, custom_task_mock):
        """Used to test not executing custom task when hook setting is set to false."""
        custom_task_mock.__name__ = "custom_task_mock"

        hooks_handler(self.sender)

        custom_task_mock.assert_not_called()

    @patch("eox_hooks.tasks.default_task")
    def test_with_non_defined_signal(self, default_task):
        """
        Used to test what happends when a not configured signal is received.

        This should result in the calling of a default task.
        """
        default_task.__name__ = "default_task"
        self.sender.__name__ = "sender.signal"

        hooks_handler(self.sender)

        default_task.assert_called()

    @override_settings(EOX_HOOKS_DEFINITIONS={})
    @patch("eox_hooks.tasks.default_task")
    def test_without_hooks_configuration_defined(self, default_task):
        """
        Used to test what happends if the current tenant is using eox-hooks but there is not a
        configuration defined.

        This should result in the calling of a default task.
        """
        default_task.__name__ = "default_task"

        hooks_handler(self.sender)

        default_task.assert_called()

    @override_settings(EOX_HOOKS_DEFINITIONS={
        "sender.example": {
            "task": "eox_hooks.tests.test_utils.non_existent_task",
        }},
        USE_EOX_HOOKS=True)
    @patch("eox_hooks.tasks.default_task")
    def test_with_non_existent_task(self, default_task):
        """
        Used to test what happends if a non-existent task is set in the settings.

        This should result in the calling of a default task.
        """
        default_task.__name__ = "default_task"

        hooks_handler(self.sender)

        default_task.assert_called()

    @override_settings(EOX_HOOKS_DEFINITIONS={
        "sender.example": {
            "task": "eox_hooks.tests.non_existent.custom_task_mock",
        }},
        USE_EOX_HOOKS=True)
    @patch("eox_hooks.tasks.default_task")
    def test_with_non_existent_module(self, default_task):
        """
        Used to test what happends if a non-existent tasks module is set in the settings.

        This should result in the calling of a default task.
        """
        default_task.__name__ = "default_task"

        hooks_handler(self.sender)

        default_task.assert_called()
