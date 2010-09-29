.. niteoweb.click2sell documentation master file, created by
   sphinx-quickstart on Thu Jul 15 14:38:10 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to niteoweb.click2sell's documentation!
==============================================

:Project title: niteoweb.click2sell
:Latest version: |release|
:Author: NiteoWeb Ltd.
:Generated: |today|
:License: GPLv2
:URL: http://pypi.python.org/pypi/niteoweb.click2sell
:Docs: http://packages.python.org/niteoweb.click2sell
:Source: http://svn.plone.org/svn/collective/niteoweb.click2sell
:Browse source: http://dev.plone.org/collective/browser/niteoweb.click2sell

""""""""""""""""""""""""""""""""

.. topic:: Summary

    Integrates `click2sell`_ digital products retailer system with `Plone`_ to enable paid memberships on your Plone site.


How it works
============

#. Visitor comes to yoursite.com/order (or similar) and clicks Order link.
#. Visitor is sent to click2sell's order form (on click2sell.com), 
    where he enters his personal information and performs payment.
#. click2sell calls-back a special view on your plone site (/@@click2sell),
    which reads POST data from click2sell, verifies it with your *Secret Key*
    and creates a new member.
#. The following information is stored in member data for later use:
    *product_id*
        click2sell's Product ID of the purchased item.
        
    *affiliate*
        Affiliate who referred the buyer.
        
    *last_purchase_id*
        click2sell receipt ID of the last purchase. This field gets updated on
        every recurring payment.

    *last_purchase_timestamp*
        Exact timestamp of the last purchase. This field gets updated on
        every recurring payment.    
    
#. Upon creating a new member, Plone send an email with login password.
#. An IMemberCreateEvent is emitted upon creating a new member.
#. New member can now login and use the site.

.. note::

    If a member already exists in Plone, then the @@click2sell view simply updates
    *last_purchase_id* and *last_purchase_timestamp* member fields.


Demo
====

You can see this product in action at http://bigcontentsearch.com/order.


Installation
============

To install in your own buildout just add it to your buildout's eggs and zcml listing as normal::

    eggs =
      Plone
      niteoweb.click2sell
      ...
      
    zcml = 
      niteoweb.click2sell
      ...


Configuration
=============

click2sell
---------

Go to click2sell and create a Vendor account. Add a test Product of type *Membership*.
Then set the following:

Secret Key
    Choose a strong password here.
    
Thank your page
    Enter a url for your *Thank You* page, normally *http://yoursite.com/thank-you*.
    
Hoplink destination url.
    Enter a url to a site with an order link, normally *http://yoursite.com/order*.

Test credit card.
    Create *Test Credit Card* so you can do test buys.


Plone
-----

#. Go to *Site Setup* -> *click2sell* control panel form and configure the following fields:

    Secret Key
       Paste the Secret Key you defined above.

#. Create a Page *Order*. Insert the following markup, replacing capitalized strings::

    <a href="http://PRODUCT_ID.VENDOR_ID.pay.click2sell.net">Order a subscription to this site!</a>

#. Create a Page *Thank You*. Insert the following text::

    Thank you for your order!
    Your credit card or bank statement will show a charge by click2sell or CLKBANK*COM.
    If you have any questions let us know on info@yoursite.com"


Test it
=======

Fire up your browser and point it to your *Order* page. Click on *Order a subscription to this site!*,
fill in your Test Credit Card info with your personal email and purchase the subscription.
Confirm by logging-in to click2sell and checking to see if there were any purchases. You should also
receive an email with username and password for accessing your site.
    

Known issues
============

The following known issues exist:

    * If members stop paying for monthly or yearly subscriptions, 
        you have to manually delete them from your Plone site.

    * The same as above goes for any chargebacks or refunds. 
        You have to manage them manually.


Running tests
=============

Open up a console and run the following::

    $ cd <workspace>/niteoweb.click2sell
    
    # run a specific test
    $ bin/test -s niteoweb.click2sell -t test_setup

    # run all tests
    $ bin/test -s niteoweb.click2sell

    # calculate code test coverage
    $ bin/coverage-test -s niteoweb.click2sell


Releasing
=========

Open up a console and run the following::

    $ cd <workspace>/niteoweb.click2sell
    
    # use zest.releaser to make an egg distribution and upload it to PyPI
    $ fullrelease
    
    # build sphinx docs and upload them to packages.python.org
    $ bin/sphinxbuilder
    $ python setup.py upload_docs


API
===

Views & Controllers
---------------------------------------------------

.. automodule:: niteoweb.click2sell.browser.click2sell

    .. autoclass:: niteoweb.click2sell.browser.click2sell.click2sellView
        :members: __call__, _verify_POST, _parse_POST, _create_or_update_member, _email_password, _generate_password

.. automodule:: niteoweb.click2sell.browser.configure_click2sell
    :members:


Utilities
---------------------------------

.. automodule:: niteoweb.click2sell.click2sell_settings
    :members:

.. automodule:: niteoweb.click2sell.interfaces
    :members:

    .. autointerface:: niteoweb.click2sell.interfaces.Iclick2sellSettings


Tests
-----------------------------------

.. automodule:: niteoweb.click2sell.tests
    :members: 

.. automodule:: niteoweb.click2sell.tests.test_setup
    :members: 

.. automodule:: niteoweb.click2sell.tests.test_click2sell
    :members:


.. include:: ../HISTORY.txt    

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _click2sell: http://www.click2sell.com/
.. _Plone: http://plone.org/
