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
#. Visitor is sent to click2sell's order form (on click2sell.eu), 
    where he enters his personal information and performs payment.
#. click2sell calls-back a special view on your plone site (/@@click2sell),
    which reads POST data from click2sell, verifies it with your *Secret Key*
    and creates a new member.
#. The following information is stored in member data for later use:

    *product_id*
        Click2Sell's Product ID of the purchased item.

    *product_name*
        Click2Sell's Product Name of the purchased item.
        
    *affiliate*
        Affiliate who referred the buyer.
        
    *last_purchase_id*
        Click2Sell receipt ID of the last purchase. This field gets updated on
        every recurring payment.

    *last_purchase_timestamp*
        Exact timestamp of the last purchase. This field gets updated on
        every recurring payment.    
    
#. Upon creating a new member, Plone sends an email with login password.
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

Go to click2sell.eu and use For Merchant -> Add Product to add a new Product.

Then click on your new Product and select API Settings. For 'URL to notify' set
*http://yoursite.com/@@click2sell* and also choose a *Secret Key*. Check 'Enable/Disable
remote server's notification' to enable server notifications and consequently
member auto-registering.


Plone
-----

#. Go to *Site Setup* -> *click2sell* control panel form and configure the following fields:

    Secret Key
       Paste the Secret Key you defined above.

Test it
=======

You are now ready to do a test buy! Go back to 'My Products' and click 'Test BUY'. Before
you finish the transaction, you need to set up your Plone site to receive Click2Sell 
server notifications. Read below.

Confirm by logging-in to click2sell and checking to see if there were any purchases. 
Also check if your receive an email with username and password for accessing your site and
login with them.
    

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
    $ bin/python setup.py upload_docs


API
===

Views & Controllers
---------------------------------------------------

.. automodule:: niteoweb.click2sell.browser.click2sell

    .. autoclass:: niteoweb.click2sell.browser.click2sell.Click2SellView
        :members: __call__, _verify_POST, _parse_POST, _create_or_update_member, _email_password, _generate_password

.. automodule:: niteoweb.click2sell.browser.configure_click2sell
    :members:


Utilities
---------------------------------

.. automodule:: niteoweb.click2sell.click2sell_settings
    :members:

.. automodule:: niteoweb.click2sell.interfaces
    :members:

    .. autointerface:: niteoweb.click2sell.interfaces.IClick2SellSettings


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


.. _click2sell: http://www.click2sell.eu/
.. _Plone: http://plone.org/
