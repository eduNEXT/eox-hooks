"""This file contains all the test for the functions defined in apps.py file.

Classes:
    TestAppsHelpers.
"""
from django.test import TestCase
from mock import patch

from eox_hooks.apps import get_signal_module


class TestAppsHelpers(TestCase):
    """
    Class that tests function helpers defined in Apps.
    """

    @patch("eox_hooks.apps.import_module")
    def test_get_signal_module_success(self, _):
        """Used to test getting the signal module of an existent signal."""
        signal_module = get_signal_module("defined_signal")

        self.assertEqual("openedx.core.lib.triggers.v1.defined_signal", signal_module)

    @patch("eox_hooks.apps.import_module")
    def test_get_signal_module_fail(self, import_mock):
        """
        Used to test getting the signal module of a non-existent module, this should return the
        default module.
        """
        import_mock.side_effect = ImportError

        signal_module = get_signal_module("undefined_signal")

        self.assertEqual("eox_hooks.dummy_signal", signal_module)
