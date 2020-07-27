"""Constants file for eox-hooks plugin."""
from enum import IntEnum


class Status(IntEnum):
    """
    Class that defines status for the execution of the hook.
    """
    SUCCESS = 1
    FAIL = 0

    @classmethod
    def choices(cls):
        """Returns choices for the class"""
        return [(key.value, key.name) for key in cls]  # pylint: disable=not-an-iterable, useless-suppression
