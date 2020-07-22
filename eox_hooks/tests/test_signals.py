"""This file contains all the test for the signals.py file.

Classes:
    SingalsTestCase: Test signals.
"""
from django.test import TestCase, override_settings
from mock import Mock, patch

from eox_hooks.signals import pre_enrollment_checking


@override_settings(CUSTOM_PRE_ENROLLMENT_TASK="eox_hooks.tests.test_utils.custom_task_mock")
class TestSignals(TestCase):
    """Signals test class."""

    def setUp(self):
        """Set up class for signals testing."""
        self.sender = Mock()

    @override_settings(USE_EOX_HOOKS_PRE_ENROLLMENT=True)
    @patch("eox_hooks.tests.test_utils.custom_task_mock")
    def test_executing_custom_task(self, custom_task_mock):
        """Used to test executing custom task when hook setting is set to true."""
        pre_enrollment_checking(self.sender)

        custom_task_mock.assert_called()

    @override_settings(USE_EOX_HOOKS_PRE_ENROLLMENT=False)
    @patch("eox_hooks.tests.test_utils.custom_task_mock")
    def test_not_executing_custom_task(self, custom_task_mock):
        """Used to test not executing custom task when hook setting is set to false."""
        pre_enrollment_checking(self.sender)

        custom_task_mock.assert_not_called()
