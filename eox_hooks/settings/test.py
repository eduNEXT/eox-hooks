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

# This key needs to be defined so that the check_apps_ready passes and the
# AppRegistry is loaded
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
