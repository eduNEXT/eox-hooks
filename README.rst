========
EoxHooks
========


Features
########


Installation
############

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

- trigger_event: is the name of the signal sent by the platform. For example: pre_enrollment_trigger.
- module: path to the module where the action to be executed is defined. For example: eox_hooks.tests.tests_utils.
- action: name of the action to be executed. For example: custom_action.
- fail_silently: defines what happens if an exception raises while executing the action. If False, then the exception is raised.


Contributing
############

Add your contribution policy. (If required)
