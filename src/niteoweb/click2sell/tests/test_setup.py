# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from niteoweb.click2sell.interfaces import IClick2SellSettings
from niteoweb.click2sell.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.interfaces import ComponentLookupError

import unittest2 as unittest


class TestInstall(IntegrationTestCase):
    """Test installation of niteoweb.click2sell into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_installed(self):
        """Test if niteoweb.click2sell is installed with portal_quickinstaller."""
        self.failUnless(self.installer.isProductInstalled('niteoweb.click2sell'))

    def test_disable_registration_for_anonymous(self):
        """Test if anonymous visitors are prevented to register to the site."""
        # The API of the permissionsOfRole() function sucks - it is bound too
        # closely up in the permission management screen's user interface
        self.failIf('Add portal member' in [r['name'] for r in
                                self.portal.permissionsOfRole('Anonymous') if r['selected']])

    def test_click2sell_fields_added(self):
        """Test if click2sell-specific fields were added to memberdata."""
        properties = self.portal.portal_memberdata.propertyIds()
        self.failUnless('product_id' in properties)
        self.failUnless('product_name' in properties)
        self.failUnless('affiliate' in properties)
        self.failUnless('last_purchase_id' in properties)
        self.failUnless('last_purchase_timestamp' in properties)

    def test_use_email_as_login(self):
        """Test if email is indeed used as username."""
        site_properties = self.portal.portal_properties.site_properties
        self.failUnless(site_properties.getProperty('use_email_as_login') == True)


class TestUninstall(IntegrationTestCase):
    """Test un-installation of niteoweb.click2sell from Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.installer.uninstallProducts(products=["niteoweb.click2sell"])

    def test_product_uninstalled(self):
        """Test if the product was uninstalled."""
        self.failIf(self.installer.isProductInstalled("niteoweb.click2sell"))

    def test_local_utility_removed(self):
        """Test if the IClick2SellSettings local utility was removed."""
        try:
            getUtility(IClick2SellSettings)
        except ComponentLookupError:
            pass

    def test_control_panel_configlet_removed(self):
        """Test if the 'Configure ClickBank' control panel configlet was removed."""
        view = getMultiAdapter((self.portal, self.portal.REQUEST), name="configure-click2sell")
        view = view.__of__(self.portal)
        try:
            self.failIf(view())
        except TypeError:
            pass


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
