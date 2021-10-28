"""
Models definitions.
"""

from importlib import import_module

from django.conf import settings


def get_certificate_model():
    """
    Gets course enrollment model from edxapp.
    """
    backend_function = settings.EOX_HOOKS_MODELS_BACKEND
    backend = import_module(backend_function)

    return backend.get_certificate_model()


def get_user_profile_model():
    """
    Gets course enrollment model from edxapp.
    """
    backend_function = settings.EOX_HOOKS_MODELS_BACKEND
    backend = import_module(backend_function)

    return backend.get_user_profile_model()
