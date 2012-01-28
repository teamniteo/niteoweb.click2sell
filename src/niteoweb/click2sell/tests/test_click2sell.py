# -*- coding: utf-8 -*-
"""Test all aspects of @@click2sell BrowserView."""

from DateTime import DateTime
from niteoweb.click2sell.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName

import mock
import unittest2 as unittest


class TestClick2Sell(IntegrationTestCase):
    """Test all aspects of @@Click2Sell."""

    def setUp(self):
        """Prepare testing environment."""
        self.portal = self.layer['portal']
        self.view = self.portal.restrictedTraverse('click2sell')
        self.registration = getToolByName(self.portal, 'portal_registration')
        self.membership = getToolByName(self.portal, 'portal_membership')
        self.mailhost = getToolByName(self.portal, 'MailHost')
        self.mailhost.reset()

    def test_call_with_no_POST(self):
        """Test @@clicbank's response when POST is empty."""
        html = self.view()
        self.failUnless('No POST request.' in html)

    @mock.patch('niteoweb.click2sell.browser.click2sell.Click2SellView._verify_POST')
    def test_call_with_invalid_POST(self, verify_post):
        """Test @@clicbank's response when POST cannot be verified."""

        # put something into self.request.form so it's not empty
        self.portal.REQUEST.form = dict(value='non empty value')

        # mock return from _verify_POST
        verify_post.return_value = False

        # test
        html = self.view()
        self.assertIn('POST verification failed.', html)

    @mock.patch('niteoweb.click2sell.browser.click2sell.Click2SellView._verify_POST')
    @mock.patch('niteoweb.click2sell.browser.click2sell.Click2SellView._parse_POST')
    @mock.patch('niteoweb.click2sell.browser.click2sell.Click2SellView.create_or_update_member')
    def test_call_with_valid_POST(self, create_or_update_member, parse_post, verify_post):
        """Test @@clicbank's response when POST is valid."""

        # put something into self.request.form so it's not empty
        self.portal.REQUEST.form = dict(value='non empty value')

        # mock post handling
        verify_post.return_value = True
        parse_post.return_value = dict(username='username')
        create_or_update_member.return_value = True

        # test
        html = self.view()
        self.assertIn('POST successfully parsed.', html)

    def test_generate_password(self):
        """Test password generation."""
        password = self.view._generate_password(8)
        self.assertEqual(len(password), 8)

    def test_verify_POST(self):
        """Test POST verification process."""
        params = dict(
            secretkey='secret',
            acquirer_transaction_id='123',
            checksum='B457E9433F98EF22AA9DD9BA4A5E2B16',
        )
        verified = self.view._verify_POST(params)
        self.failUnless(verified)

    def test_parse_POST(self):
        """Test that POST parameters are correctly mirrored into member fields."""
        params = dict(
            buyer_name='full',
            buyer_surname='name',
            buyer_email='email',
            c2s_transaction_id='last_purchase_id',
            product_id='product_id',
            product_name='product_name',
            affiliate_username='affiliate',
            purchase_date='2010-01-01',
            purchase_time='00:00:00',
        )

        expected = dict(
            fullname=u'full name',
            username='email',
            email='email',
            product_id='product_id',
            product_name='product_name',
            affiliate='affiliate',
            last_purchase_id='last_purchase_id',
            last_purchase_timestamp=DateTime('2010-01-01 00:00:00'),
        )

        result = self.view._parse_POST(params)
        self.assertEqual(result, expected)

    @mock.patch('niteoweb.click2sell.browser.click2sell.Click2SellView._generate_password')
    def test_create_member(self, generate_password):
        """Test creating a new member out of POST parameters."""
        generate_password.return_value = 'secret123'

        test_data = dict(
            username='john@smith.name',
            password='secret123',
            email='john@smith.name',
            fullname='John Smith',
            product_id='1',
            product_name='product_name',
            affiliate='Jane Affiliate',
            last_purchase_id='invoice_1',
            last_purchase_timestamp=DateTime('2010/01/01'),
        )

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
        self.assertIn('To: %(email)s' % test_data, msg)
        self.assertIn('Subject: =?utf-8?q?Your_Plone_site_login_credentials', msg)
        self.assertIn('u: %(username)s' % test_data, msg)
        self.assertIn('p: %(password)s' % test_data, msg)

        # test that we created group
        self.assertIn('click2sell', self.portal.portal_groups.getGroupIds())
        self.assertIn('click2sell', member.getGroups())

        # now test that if a request for same member is posted this member gets
        # updated
        test_data['username'] = 'john@smith.name'
        test_data['last_purchase_id'] = 'invoice_2'
        test_data['last_purchase_timestamp'] = DateTime('2010/02/02')

        # run method
        self.view.create_or_update_member(test_data['username'], test_data)

        # test that product_id was updated member
        member = self.membership.getMemberById(test_data['username'])
        self.assertEqual(member.getProperty('last_purchase_id'), 'invoice_2')
        self.assertEqual(member.getProperty('last_purchase_timestamp'), DateTime('2010/02/02'))

    def test_update_member(self):
        """Test updating an existing member with POST parameters."""

        old_data = dict(
            username='john@smith.name',
            email='john@smith.name',
            last_purchase_id='invoice_1',
            last_purchase_timestamp=DateTime('2010/01/01'),
        )

        new_data = old_data
        new_data['last_purchase_id'] = 'invoice_2'
        new_data['last_purchase_timestamp'] = DateTime('2010/02/02')

        # create a member in advance so POST parameters will perform UPDATE
        # instead of CREATE
        self.registration.addMember(
            old_data['username'],
            'test_password',
            properties=old_data
        )

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
            username='john@smith.name',
            password='secret123',
            email='john@smith.name',
            fullname='John Smith',
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
        self.failUnless('To: %(email)s' % test_data in msg)
        self.failUnless('From: %s' % self.portal.email_from_address in msg)
        self.failUnless('Subject: =?utf-8?q?Your_Click2Sell_Integration_Site_login_credentials' in msg)

        # test email body text
        self.failUnless('Hello %(fullname)s,' % test_data in msg)
        self.failUnless('u: %(username)s' % test_data in msg)
        self.failUnless('p: %(password)s' % test_data in msg)
        self.failUnless('You can now login at http://nohost/plone/login_form'in msg)
        self.failUnless('let us know on %s' % self.portal.email_from_address in msg)
        self.failUnless('Best wishes,\n%s Team' % self.portal.title in msg)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
