"""
Test Django settings for eox_hooks project.
"""

from __future__ import unicode_literals

from .common import *  # pylint: disable=wildcard-import

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

# This key needs to be defined so that the check_apps_ready passes and the
# AppRegistry is loaded
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

EOX_CORE_LOAD_PERMISSIONS = False
EOX_CORE_COURSES_BACKEND = "eox_core.edxapp_wrapper.backends.courses_h_v1"
EOX_CORE_COURSEKEY_BACKEND = "eox_core.edxapp_wrapper.backends.coursekey_h_v1"
EOX_CORE_USERS_BACKEND = "eox_core.edxapp_wrapper.backends.users_h_v1_test"
EOX_CORE_BEARER_AUTHENTICATION = 'eox_core.edxapp_wrapper.backends.bearer_authentication_j_v1_test'
