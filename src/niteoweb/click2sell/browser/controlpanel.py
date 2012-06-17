# -*- coding: utf-8 -*-
"""
Click2Sell control panel configlet
----------------------------------
"""

from niteoweb.click2sell import Click2SellMessageFactory as _
from niteoweb.click2sell.interfaces import IClick2SellSettings
from plone.app.registry.browser import controlpanel


class Click2SellSettingsEditForm(controlpanel.RegistryEditForm):
    """Form for configuring niteoweb.click2sell."""

    schema = IClick2SellSettings
    label = _(u"Click2Sell settings")
    description = _(u"""Configure integration with Click2Sell API.""")


class Click2SellSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = Click2SellSettingsEditForm
