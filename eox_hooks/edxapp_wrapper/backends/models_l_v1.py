"""
Simple backend that returns the platform's models
"""


def get_certificate_model():
    """Return the GeneratedCertificate model class when called during runtime"""
    try:
        from lms.djangoapps.certificates.models import GeneratedCertificate  # pylint: disable=import-outside-toplevel
    except ImportError:
        GeneratedCertificate = None
    return GeneratedCertificate


def get_user_profile_model():
    """Return the UserProfile model class when called during runtime"""
    try:
        from common.djangoapps.student.models import UserProfile  # pylint: disable=import-outside-toplevel
    except ImportError:
        UserProfile = None
    return UserProfile
