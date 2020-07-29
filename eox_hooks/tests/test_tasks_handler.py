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

    @patch("eox_hooks.tests.test_utils.custom_task_mock")
    def test_executing_custom_task(self, custom_task_mock):
        """Used to test executing custom task when hook setting is set to true."""
        custom_task_mock.__name__ = "custom_task_mock"

        task_handler(self.sender, self.configuration)

        custom_task_mock.assert_called()

    @patch('eox_hooks.tasks_handler.log.warning')
    @patch("eox_hooks.tests.test_utils.custom_task_mock")
    def test_executing_task_raise_exception(self, custom_task_mock, log):
        """Used to test executing custom task when hook setting is set to true."""
        custom_task_mock.__name__ = "custom_task_mock"
        custom_task_mock.side_effect = Exception

        task_handler(self.sender, self.configuration)

        log.assert_called()

    @override_settings(EOX_HOOKS_DEFINITIONS={})
    @patch("eox_hooks.tasks.default_task")
    def test_without_hooks_configuration_defined(self, default_task):
        """
        Used to test what happends if the current tenant is using eox-hooks but there is not a
        configuration defined.

        This should result in the calling of a default task.
        """
        default_task.__name__ = "default_task"
        configuration = {}

        task_handler(self.sender, configuration)

        default_task.assert_called()

    @patch("eox_hooks.tasks.default_task")
    def test_with_non_existent_task(self, default_task):
        """
        Used to test what happends if a non-existent task is set in the settings.

        This should result in the calling of a default task.
        """
        default_task.__name__ = "default_task"
        configuration = {
            "sender.example": {
                "task": "eox_hooks.tests.test_utils.non_existent_task",
            }
        }

        task_handler(self.sender, configuration)

        default_task.assert_called()

    @patch("eox_hooks.tasks.default_task")
    def test_with_non_existent_module(self, default_task):
        """
        Used to test what happends if a non-existent tasks module is set in the settings.

        This should result in the calling of a default task.
        """
        default_task.__name__ = "default_task"
        configuration = {
            "sender.example": {
                "task": "eox_hooks.tests.non_existent.custom_task_mock",
            }
        }

        task_handler(self.sender, configuration)

        default_task.assert_called()
