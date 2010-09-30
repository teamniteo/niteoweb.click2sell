# -*- coding: utf-8 -*-
"""
interfaces.py - where all interfaces, events and exceptions live
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

from zope.interface import Interface, Attribute, implements
from zope import schema

from niteoweb.click2sell import Click2SellMessageFactory


_ = Click2SellMessageFactory

# control panel schema
class IClick2SellSettings(Interface):
    """This interface defines fields for click2sell plone_control_panel configlet."""

    secretkey = schema.Password(title=_(u"click2sell Secret Key"),
                                  required=True) 

# exceptions
class Click2SellError(Exception):
    """Exception class for niteoweb.click2sell project"""

# events
class IClick2SellEvent(Interface):
    """Base interface for niteoweb.click2sell events."""

class IMemberCreatedEvent(IClick2SellEvent):
    """Interface for MemberCreatedEvent."""
    context = Attribute("A member was created by @@click2sell.")

class MemberCreatedEvent(object):
    """Emmited when a new member is created by click2sell post-back service calling @@click2sell."""
    implements(IMemberCreatedEvent)

    def __init__(self, context, username):
        self.context = context
        self.username = username
