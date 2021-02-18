"""
Init module for eox_hooks.
"""

from __future__ import unicode_literals

import django.dispatch

__version__ = '0.4.0'


dummy_signal = django.dispatch.Signal()
