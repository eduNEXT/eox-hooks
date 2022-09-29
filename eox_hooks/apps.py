"""
App configuration for eox_hooks.
"""


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
        trigger_signal = f"{OPENEDX_HOOKS_TRIGGER_MODULE}.{signal_name}"
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
                        # pylint: disable=C0301
                        'signal_path': 'openedx_events.learning.signals.STUDENT_REGISTRATION_COMPLETED',
                        'dispatch_uid': 'eox-hooks:post_register',
                    },
                    {
                        'receiver_func_name': 'hooks_handler',
                        'signal_path': 'openedx_events.learning.signals.SESSION_LOGIN_COMPLETED',
                        'dispatch_uid': 'eox-hooks:post_session_login',
                    },
                    {
                        'receiver_func_name': 'hooks_handler',
                        'signal_path': 'openedx_events.learning.signals.COURSE_ENROLLMENT_CREATED',
                        'dispatch_uid': 'eox-hooks:post_enrollment',
                    },
                    {
                        'receiver_func_name': 'hooks_handler',
                        'signal_path': 'openedx_events.learning.signals.COURSE_ENROLLMENT_CHANGED',
                        'dispatch_uid': 'eox-hooks:post_enrollment_change',
                    },
                    {
                        'receiver_func_name': 'hooks_handler',
                        # pylint: disable=C0301
                        'signal_path': 'openedx_events.learning.signals.COURSE_UNENROLLMENT_COMPLETED',
                        'dispatch_uid': 'eox-hooks:post_unenrollment',
                    },
                    {
                        'receiver_func_name': 'hooks_handler',
                        'signal_path': 'openedx_events.learning.signals.CERTIFICATE_CREATED',
                        'dispatch_uid': 'eox-hooks:post_certificate_creation',
                    },
                    {
                        'receiver_func_name': 'hooks_handler',
                        'signal_path': 'openedx_events.learning.signals.CERTIFICATE_CHANGED',
                        'dispatch_uid': 'eox-hooks:post_certificate_change',
                    },
                    {
                        'receiver_func_name': 'hooks_handler',
                        'signal_path': 'openedx_events.learning.signals.CERTIFICATE_REVOKED',
                        'dispatch_uid': 'eox-hooks:post_certificate_revoke',
                    },
                    {
                        'receiver_func_name': 'hooks_handler',
                        'signal_path': 'openedx_events.learning.signals.COHORT_MEMBERSHIP_CHANGED',
                        'dispatch_uid': 'eox-hooks:post_cohort_change',
                    },
                ],
            }
        },
    }

    # pylint: disable=import-outside-toplevel
    def ready(self):
        """
        Make sure tasks are registered.
        """
        from eox_hooks import tasks  # pylint: disable=unused-import
