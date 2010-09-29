# -*- coding: utf-8 -*-
"""
interfaces.py - where all interfaces, events and exceptions live
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

from zope.interface import Interface, Attribute, implements
from zope import schema

from niteoweb.click2sell import click2sellMessageFactory


_ = click2sellMessageFactory

# control panel schema
class Iclick2sellSettings(Interface):
    """This interface defines fields for click2sell plone_control_panel configlet."""

    secret_key = schema.Password(title=_(u"click2sell Secret Key"),
                                  required=True) 

# exceptions
class click2sellError(Exception):
    """Exception class for niteoweb.click2sell project"""

class POSTVerificationFailedError(click2sellError):
    """Exception that is raised when we cannot verify a POST from click2sell."""
    
class MemberCreationFailedError(click2sellError):
    """Exception that is raised when there is a problem with creating a new member."""
    
class MemberUpdateFailedError(click2sellError):
    """Exception that is raised when there is a problem with updating member's fields."""
    
# events
class Iclick2sellEvent(Interface):
    """Base interface for niteoweb.click2sell events."""

class IMemberCreatedEvent(Iclick2sellEvent):
    """Interface for MemberCreatedEvent."""
    context = Attribute("A member was created by @@click2sell.")

class MemberCreatedEvent(object):
    """Emmited when a new member is created by click2sell post-back service calling @@click2sell."""
    implements(IMemberCreatedEvent)

    def __init__(self, context, username):
        self.context = context
        self.username = username