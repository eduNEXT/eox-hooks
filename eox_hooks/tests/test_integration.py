"""
Test views file.
"""
from unittest.mock import MagicMock, patch
from django.test import TestCase
from eox_hooks.actions import post_to_webhook_url


class TutorIntegrationTestCase(TestCase):
    """
    POC code to run tests that cover the integration with openedx
    """

    def test_runs_code(self):
        """
        Just to make sure our test infrastructure is behaving
        """
        assert True

    # pylint: disable=import-outside-toplevel,unused-import
    def test_current_settings_code_imports(self):
        """
        Running this imports means that our backends import the right signature
        """
        import eox_hooks.edxapp_wrapper.backends.course_modes_j_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.course_modes_l_v1_test  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.course_modes_l_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.courses_j_v1_test  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.courses_j_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.courses_l_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.courses_p_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.enrollments_l_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.enrollments_l_v1_test  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.enrollments_j_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.models_j_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.models_l_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.models_l_v1_test  # isort:skip


class TestPostToWebhook(TestCase):
    """
    Test eox-hooks functions
    """
    @patch('eox_hooks.actions.requests.post')
    def test_post_to_webhook_url(self, mock_post):
        """
        Test function post_to_webhook_url
        """
        mock_trigger_event = "trigger_event"

        mock_post.return_value = MagicMock(status_code=200)

        result = post_to_webhook_url(trigger_event=mock_trigger_event)

        self.assertTrue(result)
