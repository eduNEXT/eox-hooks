"""
Simple backend that returns the platform's models
"""


def get_certificate_model():
    """Return the GeneratedCertificate model class when called during runtime"""
    from lms.djangoapps.certificates.models import GeneratedCertificate  # pylint: disable=C0415, E0401
    return GeneratedCertificate


def get_user_profile_model():
    """Return the UserProfile model class when called during runtime"""
    from common.djangoapps.student.models import UserProfile  # pylint: disable=C0415, E0401
    return UserProfile
