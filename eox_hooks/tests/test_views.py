"""This file contains all the test for the general views.py file.

Classes:
    EOXInfoTestCase: Test info_view.
"""
from os.path import dirname, realpath
from subprocess import CalledProcessError, check_output

from django.test import TestCase
from django.urls import reverse
from mock import patch
from rest_framework import status

import eox_hooks
from eox_hooks import views


class EOXInfoTestCase(TestCase):
    """Possible test's scenarios for info_view."""

    def setUp(self):
        """Setup common conditions for every test case"""
        self.url = reverse('eox-info')
        self.view_directory = dirname(realpath(views.__file__))

    def test_view_info_accesible(self):
        """
        This method tests the desired behavior of info_view when this
        does not raise any exception.

        Expected behavior:
            - Return expected content.
            - Status code 200.
        """
        git_data = check_output(
            ['git', 'rev-parse', 'HEAD'],
            cwd=self.view_directory,
        )
        expected_result = {
            'version': eox_hooks.__version__,
            'name': 'eox-hooks',
            'git': git_data.decode().rstrip('\r\n'),
        }

        response = self.client.get(self.url)

        content = response.json()
        self.assertEqual(expected_result, content)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @patch('eox_hooks.views.check_output')
    def test_view_info_response_data(self, check_output_mock):
        """
        This method tests the desired behavior of info_view when
        raise a CalledProcessError exception.

        Expected behavior:
            - check_output called once with the right values.
            - Return expected content.
            - Status code 200.
        """
        check_output_mock.side_effect = CalledProcessError(
            cmd='test-error',
            returncode=0,
        )
        expected_result = {
            'version': eox_hooks.__version__,
            'name': 'eox-hooks',
            'git': '',
        }

        response = self.client.get(self.url)

        content = response.json()
        check_output_mock.assert_called_once_with(
            ['git', 'rev-parse', 'HEAD'],
            cwd=self.view_directory,
        )
        self.assertEqual(expected_result, content)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
