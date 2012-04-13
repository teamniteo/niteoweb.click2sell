# -*- coding: utf-8 -*-
"""Where all interfaces, events and exceptions live."""

from niteoweb.click2sell import Click2SellMessageFactory
from zope import schema
from zope.interface import Attribute
from zope.interface import implements
from zope.interface import Interface

_ = Click2SellMessageFactory


# control panel schema
class IClick2SellSettings(Interface):
    """Global Click2Sell settings.

    This interface describes records stored in the configuration registry and
    obtainable via plone.registry.
    configlet.
    """

    secretkey = schema.Password(
        title=_(u"click2sell Secret Key"),
        description=_(u"help_secretkey",
            default=u"Enter the Secret Key you got from Click2Sell to access " \
                     "their API."),
        required=True,
    )


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
    """Emmited when a new member is created by click2sell post-back service
    calling @@click2sell.
    """
    implements(IMemberCreatedEvent)

    def __init__(self, context, username):
        self.context = context
        self.username = username
