# -*- coding: utf-8 -*-
"""
configure_click2sell.py - configure click2sell add-on
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

from zope.component import getUtility
from zope.formlib import form

from plone.app.controlpanel.form import ControlPanelForm

from niteoweb.click2sell import click2sellMessageFactory
from niteoweb.click2sell.interfaces import IClick2SellSettings


_ = click2sellMessageFactory

def configure_click2sell(context):
    return getUtility(IClick2SellSettings)

class Configureclick2sellForm(ControlPanelForm):
    """A ControlPanelForm BrowserView for click2sell configuration configlet."""
    form_fields = form.Fields(IClick2SellSettings)
    form_name = _("Configure click2sell")
    label = _(u"Configure click2sell add-on")
    description = _(u"Enter your click2sell settings.")