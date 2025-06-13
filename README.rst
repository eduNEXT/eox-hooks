=========
EOX Hooks
=========

|Maintainance Badge| |Test Badge| |PyPI Badge|

.. |Maintainance Badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
   :alt: Maintainance Status
.. |Test Badge| image:: https://img.shields.io/github/actions/workflow/status/edunext/eox-hooks/.github%2Fworkflows%2Ftests.yml?label=Test
   :alt: GitHub Actions Workflow Test Status
.. |PyPI Badge| image:: https://img.shields.io/pypi/v/eox-hooks?label=PyPI
   :alt: PyPI - Version

This plugin extends and customizes the `edx-platform`_ by leveraging Open edX and Django events to trigger specific actions. Key features include:

- **Post to Webhook URL:** Sends data to a specified URL based on the eox-hooks settings.
- **Get Extended Certificate Data:** Adds comprehensive certificate information to the webhook request.
- **Trigger Enrollments Creation:** Initiates an asynchronous task to enroll users in a list of courses.
- **Trigger Grades Assignment:** Propagates grades to a specified course component.
- **Create Enrollments for Program:** Enroll users in a predefined list of courses constituting a Course Program.


Installation
=============

#. Add this plugin in your Tutor ``config.yml`` with the ``OPENEDX_EXTRA_PIP_REQUIREMENTS`` setting.

   .. code-block:: yaml
      
      OPENEDX_EXTRA_PIP_REQUIREMENTS:
         - eox-hooks=={{version}}
         
#. Save the configuration with ``tutor config save``.
#. Build the image and launch your platform with ``tutor local launch``.


Usage
======

Before using eox-hooks, you need to set ``USE_EOX_HOOKS`` in ``True`` and configure ``EOX_HOOKS_DEFINITIONS`` in each tenant or site configuration that wants to use the plugin as follows:

.. code-block:: yaml

    USE_EOX_HOOKS: True
    EOX_HOOKS_DEFINITIONS:
    {
        "<trigger_event>":
        {
            "action": "<action_name>",
            "config":
            {
                "url": "https://webhook.site",
            },
            "fail_silently": False,
            "module": "<path_to_module>",
        },
    }

Where:

- **trigger_event:** The name of the event the platform sends and eox-hooks listen, such as ``post_enrollment``. For a detailed list, visit the `trigger events examples file <docs/trigger_event_examples.rst>`_.
- **action_name:** Specify the name of the action to execute. For example: ``custom_action``. To see the available actions in eox-hooks, visit the `default hook actions file <docs/default_hook_actions.rst>`_.
- **config:** Adds more information to the action.
- **fail_silently:** Defines what happens if an exception arises while executing the action. If ``False``, then the exception is raised.
- **path_to_module:** Path to the module defining the action to execute. For example: ``eox_hooks.actions``.

Example
########

.. code-block:: yaml

    EOX_HOOKS_DEFINITIONS:
    {
        "post_register":
        {
            "action": "post_to_webhook_url",
            "config":
            {
                "fields": { "recipient_email": "user.pii.email" },
                "send_certificate_data": False,
                "url": "https://webhook.site",
            },
            "fail_silently": True,
            "module": "eox_hooks.actions",
        },
    }

For more examples visit, the `hooks settings example file <docs/hooks_example.rst>`_.


Compatibility Notes
====================

+---------------------+----------------+
|  Open edX Release   |  Version       |
+=====================+================+
|  Juniper            |  <= 1.0        |
+---------------------+----------------+
|  Koa                |  > 1.0 < 2.0   |
+---------------------+----------------+
|  Lilac              |  > 1.0 < 2.0   |
+---------------------+----------------+
|  Maple              |  >= 2.0 < 3.0  |
+---------------------+----------------+
|  Nutmeg             |  >= 3.0 < 7.0  |
+---------------------+----------------+
|  Olive              |  >= 4.0 < 7.0  |
+---------------------+----------------+
|  Palm               |  >= 5.0 < 7.0  |
+---------------------+----------------+
|  Quince             |  >= 6.0 < 8.0  |
+---------------------+----------------+
|  Redwood            |  >= 6.3.0      |
+---------------------+----------------+
|  Sumac              |  >= 8.0.0      |
+---------------------+----------------+
|  Teak               |  >= 8.1.0      |
+---------------------+----------------+

The plugin is configured for the latest release (Teak). The following changes in the plugin settings should be applied to be used for previous releases.
Those settings can be changed in ``eox_hooks/settings/common.py`` or, for example, in the instance configurations.


🚨 If the release you are looking for is not listed, please note:

- If the Open edX release is compatible with the current eox-hooks version (see `Compatibility Notes <https://github.com/eduNEXT/eox-hooks?tab=readme-ov-file#compatibility-notes>`_), the default configuration is sufficient.
- If incompatible, you can refer to the README from the relevant version tag for configuration details (e.g., `v5.1.0 README <https://github.com/eduNEXT/eox-hooks/blob/v5.1.0/README.rst>`_).

How to Contribute
==================

Contributions are welcome! See our `CONTRIBUTING`_ file for more
information – it also contains guidelines for how to maintain high code
quality, which will make your contribution more likely to be accepted.

.. _CONTRIBUTING: https://github.com/eduNEXT/eox-hooks/blob/master/CONTRIBUTING.rst
.. _edx-platform: https://github.com/openedx/edx-platform/


License
=======

This project is licensed under the AGPL-3.0 License. See the `LICENSE <LICENSE.txt>`_ file for details.
