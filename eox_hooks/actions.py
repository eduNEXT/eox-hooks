"""
Module for actions.
"""
import logging

import requests
from crum import get_current_request
from opaque_keys.edx.keys import CourseKey

from eox_hooks.edxapp_wrapper.courses import get_item_not_found_exception, get_load_single_xblock
from eox_hooks.edxapp_wrapper.models import get_certificate_model
from eox_hooks.serializers import CertificateSerializer, CourseSerializer, UserSerializer
from eox_hooks.tasks import create_enrollments_for_program
from eox_hooks.utils import FakeRequest, _get_course, flatten_dict, get_trigger_settings

COURSE_PASSING_GRADE = 1
ItemNotFoundError = get_item_not_found_exception()
load_single_xblock = get_load_single_xblock()
GeneratedCertificate = get_certificate_model()
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
        certificate = GeneratedCertificate.objects.get(
            user__id=certificate.user.id, course_id=certificate.course.course_key,
        )
        extended_data = get_extended_certificate_data(certificate)
        data.update(extended_data)

    response = requests.post(webhook_url, flatten_dict(data))  # pylint: disable=W3101
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


def trigger_enrollments_creation(**kwargs):
    """
    Custom action that starts an async task that enrolls a user in a list of courses.

    After a user's enrollment to a Course Program, this action ensures that the
    user is also enrolled in the courses that define the program.

    If the course does not have the setting EDNX_TRIGGER_FOLLOWUP_ENROLLMENTS
    in its other_course_settings, then no other enrollment is created.

    The setting should look like this:

    "EDNX_TRIGGER_FOLLOWUP_ENROLLMENTS": [
        {
            "course_id": "course-v1:Demo+CSTest+2020",
            "mode": "honor"
        }
    ]

    Keyword args:
        course_key (str): course identifier.
        user (User): user that just enrolled in the course.
    """
    enrollment = kwargs.get("enrollment")
    course = _get_course(enrollment.course.course_key)

    followup_enrollments = getattr(course, "other_course_settings", {}).get(
        "EDNX_TRIGGER_FOLLOWUP_ENROLLMENTS"
    )

    if not followup_enrollments:
        return

    create_enrollments_for_program.delay(
        enrollment.user.pii.username, followup_enrollments,
    )


def trigger_grades_assignment(**kwargs):
    """
    Custom action that propagates grades to a course component.

    After a user's certificate generation, this action ensures that the grade
    obtained in a course belonging to a Course Program is mapped into the
    component that represents the course in the program.

    If the course does not have the setting EDNX_TRIGGER_GRADES_ASSIGNMENT
    in its other_course_settings, then the grade is not propagated.

    The setting should look like this:

    {
        "EDNX_TRIGGER_GRADES_ASSIGNMENT": {
            "block_id": "467f8ab131634e52bb6c22b60940d857",
            "program_id": "course-v1:Demo+CSTest+2020",
            "exact_score": true
        }
    }

    For example:

    Program A has three courses X, Y and Z. Then, this course has three xblocks
    -of type staffgradedxblock- that represent each course: x, y and z respectively.

    If exact score is true:
        User `U` obtains 90% of the grade in X, then 0.9 is assigned to the component x.
    Otherwise:
        User `U` obtains 90% of the grade in X, then 1 is assigned to the component x.

    Keyword args:
        certificate (CertificateData): certificate data generated by the course.
    """
    certificate = kwargs.get("certificate")
    course = _get_course(certificate.course.course_key)

    grades_assignment_settings = getattr(course, "other_course_settings", {}).get(
        "EDNX_TRIGGER_GRADES_ASSIGNMENT", {}
    )

    program_id = grades_assignment_settings.get("program_id")
    block_id = grades_assignment_settings.get("block_id")
    if not program_id or not block_id:
        return

    course_program_key = CourseKey.from_string(program_id)
    usage_key_block = course_program_key.make_usage_key("staffgradedxblock", block_id)

    if grades_assignment_settings.get("exact_score"):
        grade = certificate.grade
    else:
        grade = COURSE_PASSING_GRADE

    django_request = FakeRequest() if not get_current_request() else get_current_request()

    try:
        xblock_instance = load_single_xblock(
            django_request, certificate.user.id, program_id, str(usage_key_block)
        )
    except ItemNotFoundError:
        log.error(
            "Couldn't propagate score from course %s to Block %s because the latter was not found.",
            program_id,
            usage_key_block,
        )
        return

    xblock_instance.runtime.publish(
        xblock_instance, "grade", {
            "value": float(grade),
            "max_value": float(xblock_instance.weight)
        }
    )
