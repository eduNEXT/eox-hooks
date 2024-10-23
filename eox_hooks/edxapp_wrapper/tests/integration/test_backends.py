"""
This module contains tests for the backends of the edxapp_wrapper.
"""


# pylint: disable=import-outside-toplevel,unused-import
def test_current_settings_code_imports():
    """
    Running this imports means that our backends import the right signature
    """
    import eox_hooks.edxapp_wrapper.backends.course_modes_l_v1
    import eox_hooks.edxapp_wrapper.backends.courses_p_v1
    import eox_hooks.edxapp_wrapper.backends.enrollments_l_v1
    import eox_hooks.edxapp_wrapper.backends.models_l_v1
