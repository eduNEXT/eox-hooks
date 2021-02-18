"""
Unit tests for the serializers.
"""
import datetime

from django.test import TestCase

from eox_hooks.serializers import CourseSerializer, UserSerializer, get_user_model


class TestUserSerializer(TestCase):
    """
    Test for UserSerializer.
    """

    def setUp(self):
        self.user_model = get_user_model()
        self.expected_data = {
            'email': 'marie_curie@example.com',
            'username': 'macurie',
            'first_name': 'Marie',
            'last_name': 'Curie',
            'id': '1',
        }
        self.datetime = datetime.datetime.now()

    def test_valid_serializer(self):
        """
        Test serializer returns all the users data.
        """
        user = self.user_model.objects.create(**self.expected_data)

        serializer = UserSerializer(user)

        self.assertTrue(self.expected_data, serializer.data)

    def test_invalid_serializer(self):
        """
        Test serializer when the data is invalid.
        """
        data = {
            'first_name': 'marie',
            'id': 1,
        }

        serializer = UserSerializer(data=data)

        self.assertFalse(serializer.is_valid())


class TestCourseSerializer(TestCase):
    """
    Test for CourseSerializer.
    """

    def setUp(self):
        self.expected_data = {
            'id': '1',
            'name': 'Test Course',
            'number': 'C003',
            'org': 'Test-org',
            'other_course_settings': {
                'other_course_setting': '90088',
            },
            'cert_html_view_overrides': {},
        }

    def test_valid_serializer(self):
        """
        Test serializer returns all the users data.
        """
        data = {
            'id': '1',
            'display_name_with_default_escaped': 'Test Course',
            'display_number_with_default': 'C003',
            'display_org_with_default': 'Test-org',
            'other_course_settings': {
                'other_course_setting': '90088',
            },
            'cert_html_view_overrides': {},
        }

        serializer = CourseSerializer(data)

        self.assertTrue(self.expected_data, serializer.data)

    def test_invalid_serializer(self):
        """
        Test serializer when a user does not have the require fields.
        """
        data = {
            'id': 7,
            'display_name_with_default_escaped': 'Test Course',
        }

        serializer = CourseSerializer(data=data)

        self.assertFalse(serializer.is_valid())
