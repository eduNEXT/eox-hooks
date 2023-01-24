=========
Eox-hooks
=========

.. |build-status| image:: https://circleci.com/gh/eduNEXT/eox-hooks.svg?style=svg

Eox-hooks (A.K.A. Edunext Open extensions) is an `openedx plugin`_, for the `edx-platform`_ that allows extending
edx-platform through Django configurations and Open edX Events.

Compatibility Notes
--------------------

+-------------------+----------------+
| Open edX Release  |  Version       |
+===================+================+
|       Juniper     |   <= 1.0       |
+-------------------+----------------+
|        Koa        |    > 1.0       |
+-------------------+----------------+
|       Lilac       |    > 1.0 < 2.0 |
+-------------------+----------------+
|       Maple       |   >= 2.0 < 3.0 |
+-------------------+----------------+
|       Nutmeg      |   >= 3.0       |
+-------------------+----------------+
|       Olive       |   >= 4.0       |
+-------------------+----------------+

The following changes to the plugin settings are necessary. If the release you are looking for is
not listed, then the accumulation of changes from previous releases is enough.


**Juniper**

.. code-block:: yaml

   EOX_HOOKS_ENROLLMENTS_BACKEND: "eox_hooks.edxapp_wrapper.backends.enrollments_l_v1"
   EOX_HOOKS_COURSES_BACKEND: "eox_hooks.edxapp_wrapper.backends.courses_l_v1"
   EOX_HOOKS_COURSE_MODES_BACKEND: "eox_hooks.edxapp_wrapper.backends.course_modes_l_v1"
   EOX_HOOKS_MODELS_BACKEND: "eox_hooks.edxapp_wrapper.backends.models_l_v1"

**Koa**

.. code-block:: yaml

   EOX_HOOKS_ENROLLMENTS_BACKEND: "eox_hooks.edxapp_wrapper.backends.enrollments_l_v1"
   EOX_HOOKS_COURSES_BACKEND: "eox_hooks.edxapp_wrapper.backends.courses_l_v1"
   EOX_HOOKS_COURSE_MODES_BACKEND: "eox_hooks.edxapp_wrapper.backends.course_modes_l_v1"
   EOX_HOOKS_MODELS_BACKEND: "eox_hooks.edxapp_wrapper.backends.models_l_v1"

**Lilac**

.. code-block:: yaml

   EOX_HOOKS_ENROLLMENTS_BACKEND: "eox_hooks.edxapp_wrapper.backends.enrollments_l_v1"
   EOX_HOOKS_COURSES_BACKEND: "eox_hooks.edxapp_wrapper.backends.courses_l_v1"
   EOX_HOOKS_COURSE_MODES_BACKEND: "eox_hooks.edxapp_wrapper.backends.course_modes_l_v1"
   EOX_HOOKS_MODELS_BACKEND: "eox_hooks.edxapp_wrapper.backends.models_l_v1"

**Maple**

.. code-block:: yaml

   EOX_HOOKS_ENROLLMENTS_BACKEND: "eox_hooks.edxapp_wrapper.backends.enrollments_l_v1"
   EOX_HOOKS_COURSES_BACKEND: "eox_hooks.edxapp_wrapper.backends.courses_l_v1"
   EOX_HOOKS_COURSE_MODES_BACKEND: "eox_hooks.edxapp_wrapper.backends.course_modes_l_v1"
   EOX_HOOKS_MODELS_BACKEND: "eox_hooks.edxapp_wrapper.backends.models_l_v1"

**Nutmeg**

.. code-block:: yaml

   EOX_HOOKS_ENROLLMENTS_BACKEND: "eox_hooks.edxapp_wrapper.backends.enrollments_l_v1"
   EOX_HOOKS_COURSES_BACKEND: "eox_hooks.edxapp_wrapper.backends.courses_l_v1"
   EOX_HOOKS_COURSE_MODES_BACKEND: "eox_hooks.edxapp_wrapper.backends.course_modes_l_v1"
   EOX_HOOKS_MODELS_BACKEND: "eox_hooks.edxapp_wrapper.backends.models_l_v1"

**Olive**

.. code-block:: yaml

   EOX_HOOKS_ENROLLMENTS_BACKEND: "eox_hooks.edxapp_wrapper.backends.enrollments_l_v1"
   EOX_HOOKS_COURSES_BACKEND: "eox_hooks.edxapp_wrapper.backends.courses_l_v1"
   EOX_HOOKS_COURSE_MODES_BACKEND: "eox_hooks.edxapp_wrapper.backends.course_modes_l_v1"
   EOX_HOOKS_MODELS_BACKEND: "eox_hooks.edxapp_wrapper.backends.models_l_v1"


These settings can be changed in ``eox_hooks/settings/common.py`` or, for example, in ansible configurations.

**NOTE**:


- The current ``common.py`` works with Open edX Lilac version.
- Koa and Lilac work with PR (backports) 28266 and 28640 from Maple release.

Open edX devstack
*****************

- Clone this repo in the src folder of your devstack.
- Open a new Lms/Devstack shell.
- Install the plugin as follows: pip install -e /path/to/your/src/folder
- Restart Lms/Studio services.

Usage
#####

Before using eox-hooks, this plugin must be configured using EOX_HOOKS_DEFINITIONS:

.. code-block:: python

        {
            "trigger_event": {
                "module": "path_to_module",
                "action": "action_name",
                "fail_silently": True,
            },
        }

Where:

- trigger_event: is the name of the event sent by the platform. For example: pre_enrollment_trigger.
- module: path to the module where the action to be executed is defined. For example: eox_hooks.tests.tests_utils.
- action: name of the action to be executed. For example: custom_action.
- fail_silently: defines what happens if an exception raises while executing the action. If False, then the exception is raised.

Examples
########

.. code-block:: json

        "EOX_HOOKS_DEFINITIONS": {
            "post_certificate_creation": {
                "action": "post_to_webhook_url",
                "config": {
                    "send_certificate_data": true,
                    "url": "https://webhook.site"
                },
                "fail_silently": true,
                "module": "eox_hooks.actions"
            }
        }

.. code-block:: json

        "EOX_HOOKS_DEFINITIONS": {
            "post_register": {
                "action": "post_to_webhook_url",
                "fail_silently": true,
                "module": "eox_hooks.actions",
                "config" : {
                    "send_certificate_data": false,
                    "url": "https://webhook.site",
                    "fields": {
                            "recipient_email": "user.pii.email"
                    }
                }
            }
        }

.. code-block:: json

        "EOX_HOOKS_DEFINITIONS": {
            "post_certificate_creation": {
                "action": "trigger_grades_assignment",
                "fail_silently": true,
                "module": "eox_hooks.actions"
            }
        }

.. code-block:: json

        "EOX_HOOKS_DEFINITIONS": {
            "post_enrollment": {
                "action": "trigger_enrollments_creation",
                "fail_silently": false,
                "module": "eox_hooks.actions"
            }
        }


How to Contribute
#################

Contributions are welcome! See our `CONTRIBUTING`_ file for more
information – it also contains guidelines for how to maintain high code
quality, which will make your contribution more likely to be accepted.

.. _CONTRIBUTING: https://github.com/eduNEXT/eox-hooks/blob/master/CONTRIBUTING.rst
.. _edx-platform: https://github.com/edx/edx-platform/
.. _openedx plugin: https://github.com/edx/edx-platform/tree/master/openedx/core/djangoapps/plugins
