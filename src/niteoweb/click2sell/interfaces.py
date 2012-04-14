# -*- coding: utf-8 -*-
"""Where all interfaces, events and exceptions live."""

from niteoweb.click2sell import Click2SellMessageFactory as _
from zope import schema
from zope.interface import Attribute
from zope.interface import implements
from zope.interface import Interface
from niteoweb.click2sell import parse_mapping


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

    mapping = schema.List(
        title=_(u"Product ID to Group mapping"),
        description=_(u"help_secretkey",
            default=u"Optionally, you can set Product ID to Group mapping. " \
            "This is used to automatically add a new member to a certain " \
            "group based on which Click2Sell product was purchased. Format: " \
            "'PRODUCT_ID|GROUP_ID'. Example: '1|premium_members'. One " \
            "mapping per line."),
        required=False,
        value_type=schema.ASCIILine(),
        constraint=parse_mapping,
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
