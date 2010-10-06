# -*- coding: utf-8 -*-
"""
test_setup.py - test installation of niteoweb.click2sell into Plone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

import unittest

from zope.component import getUtility, getMultiAdapter
from zope.component.interfaces import ComponentLookupError

from Products.CMFCore.utils import getToolByName

from niteoweb.click2sell.interfaces import IClick2SellSettings
from niteoweb.click2sell.tests import Click2SellIntegrationTestCase


class TestInstall(Click2SellIntegrationTestCase):
    """Test installation of niteoweb.click2sell into Plone."""
        
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

class TestUninstall(Click2SellIntegrationTestCase):
    """Test un-installation of niteoweb.click2sell from Plone."""
        
    def afterSetUp(self):
        """ Grab the skins, css and js tools and uninstall NuPlone. """
        quickinstaller = getToolByName(self.portal, 'portal_quickinstaller')
        quickinstaller.uninstallProducts(products=["niteoweb.click2sell"])

    def test_product_uninstalled(self):
        """Test if the product was uninstalled."""
        quickinstaller = getToolByName(self.portal, 'portal_quickinstaller')
        self.failIf(quickinstaller.isProductInstalled("niteoweb.click2sell"))

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
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestInstall))
    suite.addTest(unittest.makeSuite(TestUninstall))
    return suite
