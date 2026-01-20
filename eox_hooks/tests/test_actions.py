"""This file contains all the test for the actions.py file.

Classes:
    TestPostToWebhookUrl.
    TriggerEnrollmentsTest.
"""
import datetime
from unittest.mock import MagicMock, patch

from django.test import TestCase
from opaque_keys.edx.keys import CourseKey
# pylint: disable=line-too-long
from openedx_events.learning.data import CertificateData, CourseData, CourseEnrollmentData, UserData, UserPersonalData

from eox_hooks.actions import (
    get_request_fields,
    post_to_webhook_url,
    trigger_enrollments_creation,
    trigger_grades_assignment,
)


class TestPostToWebhookUrl(TestCase):
    """post_to_webhook_url action test class."""

    def setUp(self):
        """Set up class for post_to_webhook_url testing."""
        self.user = UserData(
            pii=UserPersonalData(
                username="taniacher",
                email="test@example.com",
                name="Tania Chernova",
            ),
            id=1,
            is_active=True,
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
            "name": "user.pii.name",
            "username": "user.pii.username",
        }
        expected_data = {
            "name": "Tania Chernova",
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
            "username": "user.pii.username",
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

    @patch('eox_hooks.actions.requests.post')
    @patch('eox_hooks.actions.get_trigger_settings')
    def test_post_to_webhook_url_with_custom_headers(self, mock_settings, mock_post):
        """
        Used to test post_to_webhook_url with custom headers.

        This should verify that the headers defined in the configuration are passed
        correctly to the requests call.
        """
        mock_settings.return_value = {
            "url": "https://webhook.site/test",
            "headers": {
                "Authorization": "Token token=secret_key_123",
                "X-Custom-Header": "CustomValue"
            },
            "fields": {"email": "user.pii.email"}
        }
        mock_post.return_value.status_code = 200

        self.kwargs['trigger_event'] = 'post_certificate_creation'
        result = post_to_webhook_url(**self.kwargs)

        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs['headers']['Authorization'], "Token token=secret_key_123")
        self.assertEqual(kwargs['headers']['X-Custom-Header'], "CustomValue")
        self.assertTrue(result)

    @patch('eox_hooks.actions.requests.post')
    @patch('eox_hooks.actions.get_trigger_settings')
    def test_post_to_webhook_url_without_headers_in_config(self, mock_settings, mock_post):
        """
        Used to test post_to_webhook_url without headers in config.

        This should verify that the function does not fail if the 'headers' field
        does not exist in the configuration (backward compatibility).
        """
        mock_settings.return_value = {
            "url": "https://webhook.site/test",
            "fields": {"username": "user.pii.username"}
        }
        mock_post.return_value.status_code = 200

        self.kwargs['trigger_event'] = 'post_certificate_creation'

        result = post_to_webhook_url(**self.kwargs)

        _, kwargs = mock_post.call_args
        self.assertIn('headers', kwargs)
        self.assertEqual(kwargs['headers'], {})
        self.assertTrue(result)


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
        enrollment = CourseEnrollmentData(
            user=UserData(
                pii=UserPersonalData(
                    username="test",
                    email="test@example.com",
                    name="Test Example",
                ),
                id=39,
                is_active=True,
            ),
            course=CourseData(
                course_key=CourseKey.from_string("course-v1:edX+DemoX+Demo_Course"),
                display_name="Demonstration Course",
            ),
            mode="audit",
            is_active=True,
            creation_date=datetime.datetime.now(),
        )
        self.kwargs = {
            "enrollment": enrollment,
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
                    "course_id": "course-v1:edX+Demo123+Demo_Course",
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
                    "course_id": "course-v1:edX+Demo123+Demo_Course",
                },
            ],
        )


class TriggerGradingTest(TestCase):
    """
    Test class for trigger grading for program.
    """

    load_xblock = patch("eox_hooks.actions.load_single_xblock")
    get_course = patch("eox_hooks.actions._get_course")

    def setUp(self):
        """
        Setup common conditions for test cases.
        """
        self.certificate = CertificateData(
            user=UserData(
                pii=UserPersonalData(
                    username="test",
                    email="test@example.com",
                    name="Test Example",
                ),
                id=39,
                is_active=True,
            ),
            course=CourseData(
                course_key=CourseKey.from_string("course-v1:edX+DemoX+Demo_Course"),
                display_name="Demonstration Course",
            ),
            mode="audit",
            current_status="notpassing",
            grade=0.5,
            download_url="https://downdloadurl.com",
            name="Certs",
        )
        self.kwargs = {
            "certificate": self.certificate,
        }
        self.course_key = CourseKey.from_string("course-v1:edx+DemoX+Demo_Course")
        self.grading_config = {
            "block_id": "467f8ab131634e52bb6c22b60940d857",
            "program_id": "course-v1:edx+DemoX+Demo_Course",
        }
        self.usage_key = self.course_key.make_usage_key(
            "staffgradedxblock",
            self.grading_config.get("block_id")
        )

        # -------- programs ---------
        self.grading_config_programs = [
            {
                "block_id": "467f8ab131634e52bb6c22b60940d857",
                "program_id": "course-v1:edx+DemoX+Demo_Course"
            },
            {
                "block_id": "467f8ab131634e52bb6c22b60940d856",
                "program_id": "course-v1:edx2+DemoX+Demo_Course"
            }
        ]

    @load_xblock
    @get_course
    def test_course_without_settings(self, get_course, load_xblock):
        """
        Tests action when the user gets a certificate from a course without other_course_settings.
        This is a version of a course not configured as part of a program.

        Expected behavior:
            - Action returns without propagating grading.
        """
        mock_course = MagicMock()
        del mock_course.other_course_settings
        get_course.return_value = mock_course

        trigger_grades_assignment(**self.kwargs)

        load_xblock.return_value.runtime.publish.assert_not_called()

    @load_xblock
    @get_course
    def test_missing_grade_config(self, get_course, load_xblock):
        """
        Tests action when the user gets a certificate from a course without grading
        configuration.
        This is a version of a course not configured as program.

        Expected behavior:
            - Action returns without propagating grading.
        """
        mock_course = MagicMock(
            other_course_settings={
                "other_setting": "other_setting_value",
            }
        )
        get_course.return_value = mock_course

        trigger_grades_assignment(**self.kwargs)

        load_xblock.return_value.runtime.publish.assert_not_called()

    @load_xblock
    @get_course
    def test_trigger_passing_grade(self, get_course, load_xblock):
        """
        Tests action when the user gets a certificate from a course that belongs to
        a program. This version just propagates just the passing grade.

        Expected behavior:
            - Action propagates the passing grade to the program course.
        """
        mock_course = MagicMock()
        mock_course.other_course_settings.get.return_value = self.grading_config
        get_course.return_value = mock_course
        load_xblock.return_value.weight = 1

        trigger_grades_assignment(**self.kwargs)

        load_xblock.return_value.runtime.publish.assert_called_once_with(
            load_xblock.return_value,
            "grade",
            {
                "value": 1,
                "max_value": 1,
            }
        )

    @load_xblock
    @get_course
    def test_trigger_exact_grade(self, get_course, load_xblock):
        """
        Tests action when the user gets a certificate from a course that belongs to
        a program. This version propagates the exact grade obtained in the course.

        Expected behavior:
            - Action propagates the passing grade to the program course.
        """
        mock_course = MagicMock()
        self.grading_config["exact_score"] = True
        mock_course.other_course_settings.get.return_value = self.grading_config
        get_course.return_value = mock_course
        load_xblock.return_value.weight = 1

        trigger_grades_assignment(**self.kwargs)

        load_xblock.return_value.runtime.publish.assert_called_once_with(
            load_xblock.return_value,
            "grade",
            {
                "value": 0.5,
                "max_value": 1,
            }
        )

    @load_xblock
    @get_course
    def test_trigger_exact_grade_2_programs(self, get_course, load_xblock):
        """
        Tests action when the user gets a certificate from a course that belongs to
        a program. This version propagates the exact grade obtained in the course.

        Expected behavior:
            - Action propagates the passing grade to the program(s) course(s).
        """
        for grading_config in self.grading_config_programs:
            mock_course = MagicMock()
            grading_config["exact_score"] = True
            mock_course.other_course_settings.get.return_value = grading_config
            get_course.return_value = mock_course
            load_xblock.return_value.weight = 1

            trigger_grades_assignment(**self.kwargs)

            load_xblock.return_value.runtime.publish(
                load_xblock.return_value,
                "grade",
                {
                    "value": 0.5,
                    "max_value": 1,
                }
            )
