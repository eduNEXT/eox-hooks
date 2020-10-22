"""
App configuration for eox_hooks.
"""

from __future__ import unicode_literals

from importlib import import_module

from django.apps import AppConfig

OPENEDX_HOOKS_TRIGGER_MODULE = "openedx.core.lib.triggers.v1"
EOX_HOOKS_DEFAULT_TRIGGER = "eox_hooks.dummy_signal"


def get_signal_module(signal_name):
    """
    Function that checks whether a module with `signal_name` exists, if it doesn't then
    a default signal module is returned.
    """
    try:
        trigger_signal = "{signals_module}.{signal_name}".format(
            signals_module=OPENEDX_HOOKS_TRIGGER_MODULE,
            signal_name=signal_name,
        )
        module = import_module(OPENEDX_HOOKS_TRIGGER_MODULE)
        getattr(module, signal_name)
    except (ImportError, AttributeError):
        trigger_signal = EOX_HOOKS_DEFAULT_TRIGGER

    return trigger_signal


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
        },
        'signals_config': {
            'lms.djangoapp': {
                'relative_path': 'receivers',
                'receivers': [
                    {
                        'receiver_func_name': 'hooks_handler',
                        'signal_path': get_signal_module("pre_enrollment"),
                        'dispatch_uid': 'eox-hooks:pre_enrollment',
                    },
                ],
            }
        },
    }
