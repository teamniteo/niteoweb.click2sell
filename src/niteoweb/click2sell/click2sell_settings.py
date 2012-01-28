# -*- coding: utf-8 -*-
"""Store click2sell add-on settings."""

from niteoweb.click2sell.interfaces import IClick2SellSettings
from persistent import Persistent
from zope.interface import implements


class Click2SellSettings(Persistent):
    """A ZCA local utility for storing information from click2sell configuration
    configlet.
    """
    implements(IClick2SellSettings)

    secretkey = ''
