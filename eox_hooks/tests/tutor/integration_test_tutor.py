"""
Test integration file.
"""
from django.test import TestCase, override_settings


@override_settings(ALLOWED_HOSTS=['testserver'], SITE_ID=2)
class TutorIntegrationTestCase(TestCase):
    """
    Tests integration with openedx
    """

    def setUp(self):
        """
        Set up the base URL for the tests
        """
        self.base_url = 'http://local.edly.io'

    # pylint: disable=import-outside-toplevel,unused-import
    def test_current_settings_code_imports(self):
        """
        Running this imports means that our backends import the right signature
        """
        import eox_hooks.edxapp_wrapper.backends.course_modes_l_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.courses_p_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.enrollments_l_v1  # isort:skip
        import eox_hooks.edxapp_wrapper.backends.models_l_v1  # isort:skip

    def test_info_view(self):
        """
        Tests the info view endpoint in Tutor
        """
        info_view_url = f'{self.base_url}/eox-hooks/eox-info'

        response = self.client.get(info_view_url)

        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIn('version', response_data)
        self.assertIn('name', response_data)
        self.assertIn('git', response_data)
