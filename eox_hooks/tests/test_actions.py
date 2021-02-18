"""This file contains all the test for the actions.py file.

Classes:
    TestPostToWebhookUrl.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

from eox_hooks.actions import get_request_fields


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
