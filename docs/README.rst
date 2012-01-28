===================================
Click2Sell.eu integration for Plone
===================================

A Plone add-on that integrates `Click2Sell <http://click2sell.eu>`_ digital
products retailer system with `Plone <http://plone.org>`_ to enable paid
memberships on your site.

* `Source code @ GitHub <https://github.com/niteoweb/niteoweb.click2sell>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/niteoweb.click2sell>`_
* `Sphinx docs @ ReadTheDocs <http://readthedocs.org/docs/niteowebclick2sell>`_


How it works
============

#. Visitor comes to ``yoursite.com/order`` (or similar) and clicks `Order` link.
#. Visitor is sent to Click2Sell's order form (on ``http://click2sell.eu``),
   where he enters his personal information and performs payment.
#. Click2sell calls-back a special view on your plone site (``/@@click2sell``),
   which reads POST data from Click2Sell, verifies it against your
   ``Secret Key`` and creates a new member.
#. The following information is stored in member data for later use:

    ``product_id``
        Click2Sell's `Product ID` of the purchased item.

    ``product_name``
        Click2Sell's `Product Name` of the purchased item.

    ``affiliate``
        Affiliate who referred the buyer.

    ``last_purchase_id``
        Click2Sell's `Receipt ID` of the last purchase. This field gets updated
        on every recurring payment.

    ``last_purchase_timestamp``
        Exact timestamp of the last purchase. This field gets updated on every
        recurring payment.

#. Upon creating a new member, Plone sends an email with login password.
#. An ``IMemberCreateEvent`` is emitted upon creating a new member.
#. The new member can now login and use the site.

.. note::

    If a member already exists in Plone, then the ``@@click2sell`` view simply
    updates ``last_purchase_id`` and ``last_purchase_timestamp`` member fields.


Demo
====

You can see this product in action at
`BigContentSearch <http://bigcontentsearch.com/>`_.


Installation
============

To install ``niteoweb.click2sell`` you simply add
``niteoweb.click2sell`` to the list of eggs in your buildout, run
buildout and restart Plone. Then, install `niteoweb.click2sell` using the
Add-ons control panel.


Configuration
=============

Click2Sell
----------

Go to `Click2Sell.eu <http://click2sell.eu>`_ and use ``For Merchant`` ->
``Add Product`` to add a new `Product`.

Then click on your new Product and select ``API Settings``. For `URL to notify`
set ``http://yoursite.com/@@click2sell`` and also choose a `Secret Key`.
Check ``Enable/Disable remote server's notification`` to enable server
notifications and consequently member auto-registering.


Plone
-----

Go to ``Site Setup`` -> ``click2sell`` control panel form and configure the
following fields:

    Secret Key
       Paste the `Secret Key` you defined above.

Test it
=======

You are now ready to do a test buy! Go back to ``My Products`` and click
``Test BUY``. Before you finish the transaction, you need to set up your Plone
site to receive Click2Sell server notifications.

Confirm by logging-in to `Click2Sell <http://click2sell.eu>`_ and checking to
see if there were any purchases. Also check if your receive an email with
username and password for accessing your site and try to login with them.


Known issues
============

The following known issues exist:

* If members stop paying for monthly or yearly subscriptions, you have to
  manually delete them from your Plone site.

* The same as above goes for any chargebacks or refunds. You have to manage
  them manually.

