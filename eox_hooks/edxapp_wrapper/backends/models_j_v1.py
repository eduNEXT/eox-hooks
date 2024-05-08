"""
Simple backend that returns the platform's models
"""
from lms.djangoapps.certificates.models import GeneratedCertificate  # pylint: disable=C0415, E0401
from student.models import UserProfile  # pylint: disable=C0415, E0401


def get_certificate_model():
    """Return the GeneratedCertificate model class when called during runtime"""
    return GeneratedCertificate


def get_user_profile_model():
    """Return the UserProfile model class when called during runtime"""
    return UserProfile
