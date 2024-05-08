"""
Test integration file.
"""
from unittest.mock import MagicMock, patch  # pylint: disable=C0411

from django.test import TestCase


class TutorIntegrationTestCase(TestCase):
    """
    Tests integration with openedx
    """


    # pylint: disable=import-outside-toplevel,unused-import
    def test_current_settings_code_imports(self):
        """
        Running this imports means that our backends import the right signature
        """
        import eox_hooks.edxapp_wrapper.backends.course_modes_j_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.course_modes_l_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.courses_j_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.courses_l_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.courses_p_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.enrollments_l_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.enrollments_j_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.models_j_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.models_l_v1  # isort:skip
