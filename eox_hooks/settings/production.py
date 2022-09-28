"""
Production Django settings for eox_hooks project.
"""


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info:
    https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.EOX_HOOKS_ENROLLMENTS_BACKEND = getattr(settings, "ENV_TOKENS", {}).get(
        "EOX_HOOKS_ENROLLMENTS_BACKEND",
        settings.EOX_HOOKS_ENROLLMENTS_BACKEND
    )
    settings.EOX_HOOKS_COURSES_BACKEND = getattr(settings, "ENV_TOKENS", {}).get(
        "EOX_HOOKS_COURSES_BACKEND",
        settings.EOX_HOOKS_COURSES_BACKEND
    )
    settings.EOX_HOOKS_COURSE_MODES_BACKEND = getattr(settings, "ENV_TOKENS", {}).get(
        "EOX_HOOKS_COURSE_MODES_BACKEND",
        settings.EOX_HOOKS_COURSE_MODES_BACKEND
    )
