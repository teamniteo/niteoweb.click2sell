# -*- coding: utf-8 -*-
"""
__init__.py - where all TestCases live
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

import os
from Acquisition import aq_base
from Products.Five.testbrowser import Browser
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.setup import portal_owner, default_password
from plone.app.controlpanel.tests import ControlPanelTestCase
from zope.component import getSiteManager
from Products.MailHost.interfaces import IMailHost
from Products.CMFPlone.tests.utils import MockMailHost


PloneTestCase.installProduct('niteoweb.click2sell')
PloneTestCase.setupPloneSite(products=('niteoweb.click2sell',))

class Click2SellIntegrationTestCase(PloneTestCase.PloneTestCase):
    """We use this base class for all integration tests in this package. 
    These tests are integration "unit" test. They use PloneTestCase, to have
    a full Plone site to play with but they interact with Plone on a low level,
    below user UI.
    """

class Click2SellFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    """We use this base class for all functional tests in this package. 
    These tests are full-blown functional test. The emphasis is on testing what
    the user may input and see, and the system is largely tested as a black box.
    We use PloneTestCase to set up this test as well, so we have a full Plone site
    to play with. We use zope.testbrowser to test end-to-end functionality, 
    including the UI. For testing stuff on the lower levels use integration or
    unit tests.
    """

    def afterSetUp(self):
        """Prepare a testbrowser instance and a debugging environment."""
        
        # run afterSetUp of it's parent class
        super(Click2SellFunctionalTestCase, self).afterSetUp()

        # create testbrowser instance
        self.browser = Browser()

        # display full errors
        self.browser.handleErrors = False

        # this lets us see all error messages in the error_log.
        self.portal.error_log._ignored_exceptions = ()

        # by default we are managers
        self.loginAsPortalOwner()

        # delete unneeded content
        self.portal.manage_delObjects(['front-page', 'news', 'events', 'Members'])

    def login_with_browser(self, browser, username=None, password=None):
        """Login to site with testbrowser."""

        if not username:
            username = portal_owner
        if not password:
            password = default_password

        # open site
        browser.open(self.portal.absolute_url() + '/login')

        # login using the login portlet
        browser.getControl(name='__ac_name').value = username
        browser.getControl(name='__ac_password').value = password
        browser.getControl(name='submit').click()

        # did we get the logged-in message?
        self.failUnless("You are now logged in" in browser.contents)

    def start_server(self):
        """Start ZServer so we can inspect site state with normal browser."""
        from Testing.ZopeTestCase.utils import startZServer
        echo = startZServer()
        print echo

    def open_html(self):
        """Dumps self.browser.contents (HTML) to a file and opens it with a normal browser."""
        file = open('/tmp/niteoweb.click2sell.testbrowser.html', 'w')
        file.write(self.browser.contents)
        os.system('open /tmp/niteoweb.click2sell.testbrowser.html')
        
class Click2SellControlPanelTestCase(Click2SellFunctionalTestCase, ControlPanelTestCase):
    """Test case used for control panel tests, with some convenience 
    methods from plone.app.controlpanel. """
    
    
class MockMailHostTestCase(PloneTestCase.PloneTestCase):
    """Test case used for testing emails sent out by this product."""
    
    def afterSetUp(self):
        
        # run afterSetUp of it's parent class
        super(MockMailHostTestCase, self).afterSetUp()
                
        self.portal._original_MailHost = self.portal.MailHost
        self.portal.MailHost = mailhost = MockMailHost('MailHost')
        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)

    def beforeTearDown(self):
        self.portal.MailHost = self.portal._original_MailHost
        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(aq_base(self.portal._original_MailHost), provided=IMailHost)
