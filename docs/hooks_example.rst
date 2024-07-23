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
        "post_session_login":
        {
            "action": "post_to_webhook_url",
            "config":
            {
                "fields": { "recipient_email": "user.pii.email" },
                "url": "https://webhook.site/",
            },
            "fail_silently": True,
            "module": "eox_hooks.actions",
        },
        "post_enrollment":
        {
            "action": "post_to_webhook_url",
            "config":
            {
                "fields": { "recipient_email": "user.pii.email" },
                "url": "https://webhook.site/",
            },
            "fail_silently": True,
            "module": "eox_hooks.actions",
        },
    }
