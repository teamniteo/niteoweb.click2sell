# -*- coding: utf-8 -*-
"""
click2sell_settings.py - store click2sell add-on settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

from persistent import Persistent
from zope.interface import implements

from niteoweb.click2sell.interfaces import Iclick2sellSettings


class click2sellSettings(Persistent):
    """A ZCA local utility for storing information from click2sell configuration configlet."""
    implements(Iclick2sellSettings)

    secret_key = ''