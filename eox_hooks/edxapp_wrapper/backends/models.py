"""
Simple backend that returns the platform's models
"""
from django.conf import settings


def get_openedx_certificate_model():
    """Return the GeneratedCertificate model class when called during runtime"""
    if not getattr(settings, "EOX_HOOKS_TEST_ENVIRONMENT", False):
        # pylint: disable=import-error,import-outside-toplevel
        from lms.djangoapps.certificates.models import GeneratedCertificate

        return GeneratedCertificate
    # Return None when testing to avoid ImportError
    return None


def get_openedx_user_profile_model():
    """Return the UserProfile model class when called during runtime"""
    if not getattr(settings, "EOX_HOOKS_TEST_ENVIRONMENT", False):
        from student.models import UserProfile  # pylint: disable=import-error,import-outside-toplevel

        return UserProfile
    # Return None when testing to avoid ImportError
    return None
