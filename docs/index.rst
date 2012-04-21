.. include:: ../README.rst

Mocked request
==============

If you want to mock a request from Click2Sell in your local development
environment, run something along these lines::

    $ curl -d "buyer_email=test@niteoweb.com&buyer_name=John&buyer_surname=Smith&product_id=1&product_name=TestProduct&affiliate_username=affiliate@niteoweb.com&c2s_transaction_id=1&purchase_date=2012/01/01&purchase_time=00:00:00&secretkey=secret&acquirer_transaction_id=123&checksum=B457E9433F98EF22AA9DD9BA4A5E2B16" http://localhost:8080/Plone/@@click2sell

.. include:: HISTORY.rst
.. include:: LICENSE.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`