"""
Module for actions.
"""
import logging

import requests

from eox_hooks.serializers import CertificateSerializer, CourseSerializer, UserSerializer
from eox_hooks.utils import _get_course, flatten_dict, get_trigger_settings

log = logging.getLogger(__name__)


def post_to_webhook_url(**kwargs):
    """
    Send data to a webhook url specified in the microsite eox-hooks settings,
    inside the trigger event settings.
    Here is an example of how the settings should look like for this action to
    work properly:

    "EOX_HOOKS_DEFINITIONS": {
        "trigger_event": {
            "config" : {
                "send_certificate_data": false,
                "url": "https://test-webhook.com/hooks/catch/947765lp",
                "fields": {
                    "first_name": "user.second_name",
                    "recipient_email": "user.email"
                },
                "extra_fields": {
                    "email_message": "Something extra."
                }
            }
            ...
        }
    }

    When the action gets called, it will try to get the user object from the kwargs
    and access the attributes specified in the fields. It will also include all the
    extra_fields. Finally, it will make the request call to the URL with a dict
    containing the all of the data.

    If the setting send_certificate_data is True, then besides passing the fields
    defined in the settings, it also sends all the information from a certificate,
    the user, and the course associated with it.
    """
    trigger_event = kwargs.get("trigger_event")
    trigger_settings = get_trigger_settings(trigger_event)
    webhook_url = trigger_settings.get("url", "")
    fields = trigger_settings.get("fields", {})
    extra_fields = trigger_settings.get("extra_fields", {})

    data = get_request_fields(fields, extra_fields, **kwargs)

    if trigger_settings.get("send_certificate_data", False):
        certificate = kwargs.get("certificate", {})
        extended_data = get_extended_certificate_data(certificate)
        data.update(extended_data)

    response = requests.post(webhook_url, flatten_dict(data))
    log.info(
        "post_to_webhook_url request information: %s",
        response.text,
    )
    return response.status_code == 200


def get_extended_certificate_data(certificate):
    """
    Add to the webhook request all the information from a
    certificate, the user, and the course associated with it.
    """
    course = _get_course(certificate.course_id)
    user_serializer = UserSerializer(certificate.user)
    certificate_serializer = CertificateSerializer(certificate)
    course_serializer = CourseSerializer(course)

    extended_data = {
        "certificate": certificate_serializer.data,
        "user": user_serializer.data,
        "course": course_serializer.data,
    }

    return extended_data


def get_request_fields(fields, extra_fields, **kwargs):
    """
    Retrieves a dictionary with all the fields specified in the
    eox_hooks configs.
    """
    data = {}

    for name, field in fields.items():
        try:
            attributes = field.split(".")
            obj = kwargs.get(attributes.pop(0))

            for attr in attributes:
                obj = getattr(obj, attr, None)
        except AttributeError:
            obj = None

        # If not built-in function then simply return string representation
        if obj and not type(obj).__module__ == "builtins":
            obj = str(obj)

        data[name] = obj

    # Include extra-fields
    for name, field in extra_fields.items():
        data[name] = field

    return data
