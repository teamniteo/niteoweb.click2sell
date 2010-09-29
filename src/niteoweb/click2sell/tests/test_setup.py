# -*- coding: utf-8 -*-
"""
test_setup.py - test installation of niteoweb.click2sell into Plone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

import unittest

from Products.CMFCore.utils import getToolByName

from niteoweb.click2sell.tests import Click2SellIntegrationTestCase

class TestSetup(Click2SellIntegrationTestCase):
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
          
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
