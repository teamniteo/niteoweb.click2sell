# -*- coding: utf-8 -*-
"""Init and utils."""

from zope.i18nmessageid import MessageFactory


click2sellMessageFactory = MessageFactory('niteoweb.click2sell')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
