"""
App configuration for eox_hooks.
"""

from __future__ import unicode_literals

from django.apps import AppConfig


class EoxHooksConfig(AppConfig):
    """
    EoxHooks configuration.
    """
    name = 'eox_hooks'
    verbose_name = 'EoxHooks'

    plugin_app = {
        'url_config': {
            'lms.djangoapp': {
                'namespace': 'eox-hooks',
                'regex': r'^eox-hooks/',
                'relative_path': 'urls',
            },
            'cms.djangoapp': {
                'namespace': 'eox-hooks',
                'regex': r'^eox-hooks/',
                'relative_path': 'urls',
            }
        },
        'settings_config': {
            'lms.djangoapp': {
                'common': {'relative_path': 'settings.common'},
                'test': {'relative_path': 'settings.test'},
                'production': {'relative_path': 'settings.production'},
            },
            'cms.djangoapp': {
                'common': {'relative_path': 'settings.common'},
                'test': {'relative_path': 'settings.test'},
                'production': {'relative_path': 'settings.production'},
            },
        }
    }
