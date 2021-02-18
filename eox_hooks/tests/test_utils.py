"""
Test utils functions.
"""
from django.test import TestCase

from eox_hooks.utils import flatten_dict


def custom_action_mock(**kwargs):  # pylint: disable=unused-argument
    """Function used to test custom signal receiver."""


class TestUtils(TestCase):
    """Utils functions test class."""

    def test_flatten_dict(self):
        """
        Used to test flatten_dict function

        This should return a 1-level dictionary.
        """
        data = {
            "user": {
                "first_name": "Mansa",
                "last_name": "Musa",
                "username": "imsorich",
                "profile": {
                    "favorite_food": "pizza",
                    "age": 15,
                },
            },
            "course": {
                "id": "C003",
                "name": "Test-Course",
                "number": 100,
            },
            "certificate_id": "C0010",
        }
        expected_data = {
            "user_first_name": "Mansa",
            "user_last_name": "Musa",
            "user_username": "imsorich",
            "user_profile_favorite_food": "pizza",
            "user_profile_age": 15,
            "course_id": "C003",
            "course_name": "Test-Course",
            "course_number": 100,
            "certificate_id": "C0010",
        }

        result_data = flatten_dict(data)

        self.assertEqual(expected_data, result_data)
