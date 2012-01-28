# -*- coding: utf-8 -*-
"""Doctest runner."""

from niteoweb.click2sell.tests.base import Click2SellControlPanelTestCase
from Testing import ZopeTestCase as ztc
import doctest
import unittest


def test_suite():
    return unittest.TestSuite([

        # Test the Click2Sell control panel
        ztc.ZopeDocFileSuite(
            'tests/control_panel.txt', package='niteoweb.click2sell',
            test_class=Click2SellControlPanelTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
