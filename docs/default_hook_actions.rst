Default Hooks Actions
======================

The actions in the hooks configuration could live in any route, but some actions are already available in ``eox-hooks``, and there are:

- ``post_to_webhook_url``: Send data to a webhook url specified in the hook settings.
- ``trigger_enrollments_creation``: starts an async task that enrolls a user in a list of courses.
- ``trigger_grades_assignment``: propagates grades to a course component.

For more information, you can see the code in `actions.py <https://github.com/eduNEXT/eox-hooks/blob/v5.1.0/eox_hooks/actions.py>`_.
