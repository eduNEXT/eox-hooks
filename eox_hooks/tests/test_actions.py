"""This file contains all the test for the actions.py file.

Classes:
    TestPostToWebhookUrl.
    TriggerEnrollmentsTest.
"""
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from eox_hooks.actions import get_request_fields, trigger_enrollments_creation


class TestPostToWebhookUrl(TestCase):
    """post_to_webhook_url action test class."""

    def setUp(self):
        """Set up class for post_to_webhook_url testing."""
        self.user = get_user_model().objects.create(
            id='1',
            first_name='Tania',
            last_name='Chernova',
            username='taniacher',
        )
        self.kwargs = {
            'user': self.user,
        }

    def test_get_request_fields(self):
        """
        Used to test get_request_fields

        This should return a dictionary with all the fields found.
        """
        fields = {
            "first_name": "user.first_name",
            "last_name": "user.last_name",
            "username": "user.username",
        }
        expected_data = {
            "first_name": "Tania",
            "last_name": "Chernova",
            "username": "taniacher",
        }

        result_data = get_request_fields(fields, {}, **self.kwargs)

        self.assertEqual(expected_data, result_data)

    def test_get_request_fields_missing_fields(self):
        """
        Used to test what happends if the fields indicated in the settings
        are not found.

        This should return a dictionary with the fields that were successfully
        found, and the ones that weren't are passed as None.
        """
        fields = {
            "favorite_color": "user.favorite_color",
            "favorite_food": "user.favorite_food",
            "username": "user.username",
            "course": "course.id",
        }
        extra_fields = {
            "custom_message": "testing get_request_fields",
        }
        expected_data = {
            "custom_message": "testing get_request_fields",
            "username": "taniacher",
            "favorite_color": None,
            "favorite_food": None,
            "course": None,
        }

        result_data = get_request_fields(fields, extra_fields, **self.kwargs)

        self.assertEqual(expected_data, result_data)


class TriggerEnrollmentsTest(TestCase):
    """
    Test class for trigger enrollment creation for program.
    """

    create_enrollments_for_program = patch("eox_hooks.actions.create_enrollments_for_program")
    get_course = patch("eox_hooks.actions._get_course")

    def setUp(self):
        """
        Setup common conditions for test cases.
        """
        self.user = MagicMock(username="test")
        self.kwargs = {
            "user": self.user,
        }

    @create_enrollments_for_program
    @get_course
    def test_course_without_settings(self, get_course, create_enroll_task):
        """
        Tests action when the user enrolls into a course without other_course_settings.
        This is a version of a course not configured as program.

        Expected behavior:
            - Action returns without creating other enrollments.
        """
        mock_course = MagicMock()
        del mock_course.other_course_settings
        get_course.return_value = mock_course

        trigger_enrollments_creation(**self.kwargs)

        create_enroll_task.delay.assert_not_called()

    @create_enrollments_for_program
    @get_course
    def test_enroll_into_regular_course(self, get_course, create_enroll_task):
        """
        Tests action when the user enrolls into a regular course. Meaning, a course
        not configured with EDNX_TRIGGER_FOLLOWUP_ENROLLMENTS.

        Expected behavior:
            - Action returns without creating other enrollments.
        """
        other_course_settings = {
            "course_setting": "setting_value",
        }
        mock_course = MagicMock(other_course_settings=other_course_settings)
        get_course.return_value = mock_course

        trigger_enrollments_creation(**self.kwargs)

        create_enroll_task.delay.assert_not_called()

    @create_enrollments_for_program
    @get_course
    def test_enroll_for_program(self, get_course, create_enroll_task):
        """
        Tests action when the user enrolls into a Course Program.

        Expected behavior:
            - Action starts an async task that creates the other enrollments.
        """
        other_course_settings = {
            "EDNX_TRIGGER_FOLLOWUP_ENROLLMENTS": [
                {
                    "course_id": "course-v1:edX+DemoX+Demo_Course",
                },
            ],
        }
        mock_course = MagicMock(other_course_settings=other_course_settings)
        get_course.return_value = mock_course

        trigger_enrollments_creation(**self.kwargs)

        create_enroll_task.delay.assert_called_once_with(
            "test",
            [
                {
                    "course_id": "course-v1:edX+DemoX+Demo_Course",
                },
            ],
        )
