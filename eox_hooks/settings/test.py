"""
Test Django settings for eox_hooks project.
"""
import codecs
import os

import yaml

from .common import *  # pylint: disable=wildcard-import, unused-wildcard-import

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'eox_hooks',
]

TIME_ZONE = 'UTC'

EOX_HOOKS_DEFINITIONS = {
    "sender.example": {
        "module": "eox_hooks.tests.test_utils",
        "action": "custom_action_mock",
        "fail_silently": True,
    },
}

USE_EOX_HOOKS = True

EOX_HOOKS_TEST_ENVIRONMENT = True

EOX_HOOKS_ENROLLMENTS_BACKEND = "eox_hooks.edxapp_wrapper.backends.enrollments_l_v1_test"

EOX_HOOKS_COURSES_BACKEND = "eox_hooks.edxapp_wrapper.backends.courses_j_v1_test"

EOX_HOOKS_COURSE_MODES_BACKEND = "eox_hooks.edxapp_wrapper.backends.course_modes_l_v1_test"

EOX_HOOKS_MODELS_BACKEND = "eox_hooks.edxapp_wrapper.backends.models_l_v1_test"

# This key needs to be defined so that the check_apps_ready passes and the
# AppRegistry is loaded
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}


def plugin_settings(settings):  # pylint: disable=function-redefined
    """
    For the platform tests
    """
    # setup the databases used in the tutor local environment
    if os.environ['LMS_CFG']:
        with codecs.open(os.environ['LMS_CFG'], encoding='utf-8') as f:
            env_tokens = yaml.safe_load(f)
        settings.DATABASES = env_tokens['DATABASES']


# Integration test settings module
INTEGRATION_TEST_SETTINGS = {
    # Retrieved from the Tutor environment where the integration tests run
    "EOX_HOOKS_BASE_URL": f"http://{os.environ.get('LMS_HOST', 'local.edly.io')}/eox-hooks",
    "API_TIMEOUT": 5,
}
