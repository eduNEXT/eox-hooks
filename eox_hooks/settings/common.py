"""
Common Django settings for eox_hooks project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret-key'


# Application definition

INSTALLED_APPS = []

ROOT_URLCONF = 'eox_hooks.urls'


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_TZ = True


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info:
    https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.EOX_HOOKS_ENROLLMENTS_BACKEND = "eox_hooks.edxapp_wrapper.backends.enrollments_l_v1"
    settings.EOX_HOOKS_COURSES_BACKEND = "eox_hooks.edxapp_wrapper.backends.courses_l_v1"
    settings.EOX_HOOKS_COURSE_MODES_BACKEND = "eox_hooks.edxapp_wrapper.backends.course_modes_l_v1"
    settings.EOX_HOOKS_MODELS_BACKEND = "eox_hooks.edxapp_wrapper.backends.models_l_v1"
