EOX_HOOKS Settings Example
===========================

.. code-block:: yaml

    USE_EOX_HOOKS: True
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
            "fail_silently": False,
            "module": "eox_hooks.actions",
        },
        "post_certificate_creation": {
            "action": "trigger_grades_assignment",
            "fail_silently": True,
            "module": "eox_hooks.actions"
        },
        "post_enrollment": {
            "action": "trigger_enrollments_creation",
            "fail_silently": False,
            "module": "eox_hooks.actions"
        }
    }
