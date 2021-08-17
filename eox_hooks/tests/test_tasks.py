"""
This file contains all the test for the tasks.py file.

Classes:
    EnrollmentCreationTest.
"""
from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from opaque_keys.edx.keys import CourseKey

from eox_hooks.tasks import create_enrollments_for_program


class EnrollmentCreationTest(TestCase):
    """
    Test class for trigger enrollment creation for program.
    """

    get_enrollment = patch("eox_hooks.tasks.CourseEnrollment")

    def setUp(self):
        """
        Setup common conditions for test cases.
        """
        self.user = User.objects.create_user(username="test")
        self.invalid_followup_enrollments = [
            {
                "course_id": "course-v1:edx+DemoX+Demo_Course",
                "mode": "premium"
            },
        ]
        self.valid_followup_enrollments = [
            {
                "course_id": "course-v1:Demo+DemoX+Demo_Course",
                "mode": "honor"
            },
        ]
        self.course = Mock(id="course-v1:Demo+DemoX+Demo_Course", org="Demo")
        self.course_key = CourseKey.from_string(self.course.id)

    @get_enrollment
    def test_enrollment_mode_invalid(self, course_enrollment):
        """
        Tests enrollment creation when the configuration is invalid.

        Expected behavior:
            - Followup enrollment is not created.
        """
        with self.assertLogs('eox_hooks.tasks', 'ERROR'):
            create_enrollments_for_program(  # pylint: disable=no-value-for-parameter
                username=self.user.username,
                followup_enrollments=self.invalid_followup_enrollments,
            )
        course_enrollment.enroll.assert_not_called()

    @override_settings(course_org_filter=["edx"])
    @get_enrollment
    def test_enrollment_org_invalid(self, course_enrollment):
        """
        Tests enrollment creation when the configuration is invalid.

        Expected behavior:
            - Followup enrollment is not created.
        """
        with self.assertLogs('eox_hooks.tasks', 'ERROR'):
            create_enrollments_for_program(  # pylint: disable=no-value-for-parameter
                username=self.user.username,
                followup_enrollments=self.invalid_followup_enrollments,
            )
        course_enrollment.enroll.assert_not_called()

    @get_enrollment
    def test_enrollment_key_invalid(self, course_enrollment):
        """
        Tests enrollment creation when the configuration is invalid.

        Expected behavior:
            - Followup enrollment is not created.
        """
        enrollment_config = [
            {
                "course_id": "Demo",
                "mode": "honor"
            },
        ]

        with self.assertLogs('eox_hooks.tasks', 'ERROR'):
            create_enrollments_for_program(  # pylint: disable=no-value-for-parameter
                username=self.user.username,
                followup_enrollments=enrollment_config,
            )
        course_enrollment.enroll.assert_not_called()

    @override_settings(course_org_filter=["Demo"])
    @get_enrollment
    def test_enrollments_for_program(self, course_enrollment):
        """
        Tests valid enrollment creation after user's enrollment in a program.

        Expected behavior:
            - Followup enrollments are created.
        """
        create_enrollments_for_program(  # pylint: disable=no-value-for-parameter
            username=self.user.username,
            followup_enrollments=self.valid_followup_enrollments,
        )

        course_enrollment.enroll.assert_called_once_with(
            self.user,
            self.course_key,
            "honor",
        )
