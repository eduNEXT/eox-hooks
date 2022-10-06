"""
Task file for eox-hooks plugin.
"""
import logging

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey

from eox_hooks.edxapp_wrapper.course_modes import get_all_course_modes
from eox_hooks.edxapp_wrapper.enrollments import get_course_enrollment

MODES_FOR_COURSE = get_all_course_modes()
ENROLLMENT_MAX_RETRIES = 3
User = get_user_model()
CourseEnrollment = get_course_enrollment()
log = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=ENROLLMENT_MAX_RETRIES)
def create_enrollments_for_program(self, username, followup_enrollments):
    """
    Create enrollments for a list of courses that define a Course Program.

    Args:
        username (str): identification of the user to be enrolled.
        mode (str): CourseMode for the enrollment.
        followup_enrollments ([Dict]): list of values used in the enrollment
        creation. The valid attributes are:
            - course_id
            - mode
    """
    try:
        user = User.objects.get(username=username)

        for enrollment in followup_enrollments:

            course_key_str = enrollment.pop("course_id", "")

            try:
                course_key = CourseKey.from_string(course_key_str)
            except InvalidKeyError:
                log.error(
                    "Couldn't create enrollment for course because the configuration is not valid: "
                    "course ID missing or invalid."
                )
                continue

            mode = enrollment.get("mode", "audit")
            mode_not_valid = mode.lower() not in MODES_FOR_COURSE
            course_org_not_valid = course_key.org not in getattr(
                settings, "course_org_filter", []
            )

            if mode_not_valid or course_org_not_valid:
                log.error(
                    "Couldn't create enrollment for %s because the configuration is not valid: "
                    "invalid organization or course mode.",
                    course_key_str,
                )
                continue

            CourseEnrollment.enroll(user, course_key, mode)

    except Exception as error:
        raise self.retry(exc=error)
