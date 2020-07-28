"""This module defines the handlers for the actions triggered by a signal received by eox-hooks."""
import logging
from importlib import import_module

from django.conf import settings

from eox_hooks.constants import Status
from eox_hooks.models import HookExecutionAudit
from eox_hooks.tests.test_utils import custom_action_mock

log = logging.getLogger(__name__)


def action_handler(trigger_event, configuration, **kwargs):
    """
    Function that executes actions given a specific configuration.
    """
    action = action_lookup(
        module_name=configuration.get("module", "missing_module"),
        action=configuration.get("action", ""),
    )

    action_information = {}

    try:
        action(**kwargs)
        action_information["status"] = Status.SUCCESS

    except Exception as exception:  # pylint: disable=broad-except
        action_information["status"] = Status.FAIL
        if not configuration.get("fail_silently"):
            raise exception

    finally:
        if configuration.get("use_audit", True):
            action_information.update(
                {
                    "trigger_event": trigger_event,
                    "action": action,
                })
            audit_action_execution(**action_information)


def action_lookup(module_name, action):
    """
    Function that returns a function defined in path, if the path is not find then a default action is
    returned.
    The path must look like: eox_hooks.actions.default_logging
    Where eox_hooks.actions is module_name and action_name is default_logging
    """
    try:
        module = import_module(module_name)
        return getattr(module, action)
    except ImportError:
        message = "The module {} with the action {} does not exist. A default action will be used.".format(
            module_name,
            action,
        )
    except AttributeError:
        message = "The action {} does not exist in the module {}. A default action will be used.".format(
            action,
            module_name,
        )

    log.warning("EOX_HOOKS | {}".format(message))
    return custom_action_mock


def audit_action_execution(status, trigger_event, action):
    """Function that creates an audit entry for the current action execution."""
    audit_entry = HookExecutionAudit.objects.create(
        status=status,
        trigger_event=trigger_event,
        action_name=getattr(action, "__name__", str(action)),
        tenant_domain=getattr(settings, "EDNX_TENANT_DOMAIN", "default_tenant_domain"),
    )

    if status == Status.FAIL:
        message = "EOX_HOOKS | {}".format(str(audit_entry))
        log.error(message)
