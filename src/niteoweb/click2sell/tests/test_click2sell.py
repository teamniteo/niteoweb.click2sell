# -*- coding: utf-8 -*-
"""
test_click2sell.py - test all aspects of @@click2sell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

import unittest
from DateTime import DateTime
from mocker import Mocker, ARGS, KWARGS

from Products.CMFCore.utils import getToolByName

from niteoweb.click2sell.tests import Click2SellIntegrationTestCase, MockMailHostTestCase


class TestClick2Sell(Click2SellIntegrationTestCase, MockMailHostTestCase):
    """Test all aspects of @@Click2Sell."""

    def afterSetUp(self):
        """Prepare testing environment."""
        super(TestClick2Sell, self).afterSetUp()
        self.view = self.portal.restrictedTraverse('click2sell')
        self.mailhost = self.portal.MailHost
        self.registration = getToolByName(self.portal, 'portal_registration')

    def test_call_with_no_POST(self):
        """Test @@clicbank's response when POST is empty."""
        html = self.view()
        self.failUnless('No POST request.' in html)

    def test_call_with_invalid_POST(self):
        """Test @@clicbank's response when POST cannot be verified."""

        # put something into self.request.form so it's not empty
        self.portal.REQUEST.form = dict(value='non empty value')
        
        # mock return from _verify_POST
        mocker = Mocker()
        mock_view = mocker.patch(self.view)
        mock_view._verify_POST(ARGS, KWARGS)
        mocker.result(False)
        mocker.replay()
        
        # test
        html = self.view()
        self.failUnless('POST verification failed.' in html)
        mocker.restore()

    def test_call_with_valid_POST(self):
        """Test @@clicbank's response when POST is valid."""

        # put something into self.request.form so it's not empty
        self.portal.REQUEST.form = dict(value='non empty value')
        
        # mock return from _verify_POST
        mocker = Mocker()
        mock_view = mocker.patch(self.view)
        mock_view._verify_POST(ARGS, KWARGS)
        mocker.result(True)

        # mock return from _parse_POST
        mock_view._parse_POST(ARGS, KWARGS)
        mocker.result(dict(username='username'))

        # mock return from create_or_update_member
        mock_view.create_or_update_member(ARGS, KWARGS)
        mocker.result(True)
        mocker.replay()
                
        # test
        html = self.view()
        self.failUnless('POST successfully parsed.' in html)
        mocker.restore()

    def test_generate_password(self):
        """Test password generation."""
        password = self.view._generate_password(8)
        self.assertEqual(len(password), 8)

    def test_verify_POST(self):
        """Test POST verification process."""
        params = dict(
                    secretkey= 'secret',
                    acquirer_transaction_id='123',
                    checksum='B457E9433F98EF22AA9DD9BA4A5E2B16',
                    )
        verified = self.view._verify_POST(params)
        self.failUnless(verified)

    def test_parse_POST(self):
        """Test that POST parameters are correctly mirrored into member fields."""
        params = dict(
                    buyer_name = 'full',
                    buyer_surname = 'name',
                    buyer_email = 'email',
                    c2s_transaction_id = 'last_purchase_id',
                    product_id = 'product_id',
                    product_name = 'product_name',
                    affiliate_username= 'affiliate',
                    purchase_date = '2010-01-01',
                    purchase_time = '00:00:00',
                    )

        expected = dict(
                        fullname = u'full name',
                        username = 'email',
                        email = 'email',
                        product_id = 'product_id',
                        product_name = 'product_name',
                        affiliate = 'affiliate',
                        last_purchase_id = 'last_purchase_id',
                        last_purchase_timestamp = DateTime('2010-01-01 00:00:00'),
                        )

        result = self.view._parse_POST(params)
        self.assertEqual(result, expected)

    def test_create_member(self):
        """Test creating a new member out of POST parameters."""

        test_data = dict(
                    username = 'john@smith.name',
                    password = 'secret123',
                    email = 'john@smith.name',
                    fullname = 'John Smith',
                    product_id = '1',
                    product_name = 'product_name',
                    affiliate = 'Jane Affiliate',
                    last_purchase_id = 'invoice_1',
                    last_purchase_timestamp = DateTime('2010/01/01'),
                    )

        # set From SMTP header
        self.portal.email_from_address = "mail@plone.test"
        
        # mock return from _generate_password
        mocker = Mocker()
        mock_view = mocker.patch(self.view)
        mock_view._generate_password(ARGS, KWARGS)
        mocker.result(test_data['password'])
        mocker.count(2)
        mocker.replay()
        
        # run method
        self.view.create_or_update_member(test_data['username'], test_data)
        
        # test member
        member = self.portal.portal_membership.getMemberById(test_data['username'])
        self.assertEqual(member.getProperty('email'), test_data['email'])
        self.assertEqual(member.getProperty('fullname'), test_data['fullname'])
        self.assertEqual(member.getProperty('product_id'), test_data['product_id'])
        self.assertEqual(member.getProperty('product_name'), test_data['product_name'])
        self.assertEqual(member.getProperty('affiliate'), test_data['affiliate'])
        self.assertEqual(member.getProperty('last_purchase_id'), test_data['last_purchase_id'])
        self.assertEqual(member.getProperty('last_purchase_timestamp'), test_data['last_purchase_timestamp'])
        
        # test email
        self.assertEqual(len(self.mailhost.messages), 1)
        msg = self.mailhost.messages[0]
        self.failUnless('To: %s' %test_data['email'] in msg)
        self.failUnless('Subject: =?utf-8?q?Your_Plone_site_login_credentials' in msg)
        self.failUnless('u: %s' %test_data['username'] in msg)
        self.failUnless('p: %s' %test_data['password'] in msg)

        # test that we created group
        self.assertTrue('click2sell' in self.portal.portal_groups.getGroupIds())
        self.assertTrue('click2sell' in member.getGroups())

        # now test that if a request for same member is posted this member gets updated
        test_data['username'] = 'john@smith.name'
        test_data['last_purchase_id'] = 'invoice_2'
        test_data['last_purchase_timestamp'] = DateTime('2010/02/02')

        # run method
        self.view.create_or_update_member(test_data['username'], test_data)

        # test that product_id was updated member
        member = self.portal.portal_membership.getMemberById(test_data['username'])
        self.assertEqual(member.getProperty('last_purchase_id'), 'invoice_2')
        self.assertEqual(member.getProperty('last_purchase_timestamp'), DateTime('2010/02/02'))


    def test_update_member(self):
        """Test updating an existing member with POST parameters."""

        old_data = dict(
                            username = 'john@smith.name',
                            email = 'john@smith.name',
                            last_purchase_id = 'invoice_1',
                            last_purchase_timestamp = DateTime('2010/01/01'),
                            )
        new_data = old_data
        new_data['last_purchase_id'] = 'invoice_2'
        new_data['last_purchase_timestamp'] = DateTime('2010/02/02')
        
        # create a member in advance so POST parameters will perform UPDATE instead of CREATE
        self.registration.addMember(old_data['username'], 'test_password', properties=old_data)
                        
        # run method
        self.view.create_or_update_member(new_data['username'], new_data)
        
        # test member
        member = self.portal.acl_users.getUserById(new_data['username'])
        self.assertEqual(member.getProperty('last_purchase_id'), new_data['last_purchase_id'])
        self.assertEqual(member.getProperty('last_purchase_timestamp'), new_data['last_purchase_timestamp'])
        
        # test email
        self.assertEqual(len(self.mailhost.messages), 0)

    def test_email_password(self):
        """Test headers and text of email that is sent to newly created member."""
        
        test_data = dict(
                    username = 'john@smith.name',
                    password = 'secret123',
                    email = 'john@smith.name',
                    fullname = 'John Smith',
                    )

        # set portal properties
        self.portal.title = u'Click2Sell Integration Site'
        self.portal.email_from_address = "mail@plone.test"
        
        # run method
        self.view._email_password(test_data['username'], test_data['password'], test_data)
        
        # test email
        self.assertEqual(len(self.mailhost.messages), 1)
        msg = self.mailhost.messages[0]

        # test email headers
        self.failUnless('To: %s' %test_data['email'] in msg)
        self.failUnless('From: %s' %self.portal.email_from_address in msg)
        self.failUnless('Subject: =?utf-8?q?Your_Click2Sell_Integration_Site_login_credentials' in msg)
        
        # test email body text
        self.failUnless('Hello %s,' %test_data['fullname'] in msg)
        self.failUnless('u: %s' %test_data['username'] in msg)
        self.failUnless('p: %s' %test_data['password'] in msg)
        self.failUnless('You can now login at http://nohost/plone/login_form'in msg)
        self.failUnless('let us know on %s' %self.portal.email_from_address in msg)
        self.failUnless('Best wishes,\n%s Team' %self.portal.title in msg)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestClick2Sell))
    return suite
