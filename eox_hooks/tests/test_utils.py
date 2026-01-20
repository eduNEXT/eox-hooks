"""
Test utils functions.
"""
from django.test import TestCase

from eox_hooks.utils import flatten_dict, unflatten_dict


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

    def test_unflatten_dict_default_delimiter(self):
        """
        Used to test unflatten_dict function with default delimiter

        This should return a nested dictionary matching the original hierarchy.
        """
        flat_data = {
            "base.footer.logo_url": "https://edunext.co",
            "base.footer.copy": "All rights reserved",
            "foo": "eduNEXT",
        }
        expected_nested = {
            "base": {
                "footer": {
                    "logo_url": "https://edunext.co",
                    "copy": "All rights reserved",
                }
            },
            "foo": "eduNEXT",
        }

        nested = unflatten_dict(flat_data)

        self.assertEqual(expected_nested, nested)

    def test_unflatten_dict_custom_delimiter(self):
        """
        Used to test unflatten_dict function with custom delimiter

        This should return a nested dictionary even when using a non-default delimiter.
        """
        flat_data = {
            "user|profile|name": "Alice",
            "user|profile|age": 30,
            "course|id": "C001",
        }
        expected_nested = {
            "user": {
                "profile": {
                    "name": "Alice",
                    "age": 30,
                }
            },
            "course": {
                "id": "C001",
            },
        }

        nested = unflatten_dict(flat_data, delimiter="|")

        self.assertEqual(expected_nested, nested)
