"""
Test Django settings for eox_hooks project.
"""


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

EOX_HOOKS_ENROLLMENTS_BACKEND = "eox_hooks.edxapp_wrapper.backends.enrollments_j_v1"

EOX_HOOKS_COURSES_BACKEND = "eox_hooks.edxapp_wrapper.backends.courses_j_v1"

EOX_HOOKS_COURSE_MODES_BACKEND = "eox_hooks.edxapp_wrapper.backends.course_modes_j_v1"

# This key needs to be defined so that the check_apps_ready passes and the
# AppRegistry is loaded
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
