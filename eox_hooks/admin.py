"""
Admin class.
"""
from django.contrib import admin

from eox_hooks.models import HookExecutionAudit


class HookExecutionAuditAdmin(admin.ModelAdmin):
    """Audit admin."""

    list_display = [
        "key",
        "status",
        "trigger_event",
        "action_name",
        "tenant_domain",
    ]


admin.site.register(HookExecutionAudit, HookExecutionAuditAdmin)
