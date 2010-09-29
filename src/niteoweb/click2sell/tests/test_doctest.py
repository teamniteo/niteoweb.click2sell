import unittest
import doctest

from Testing import ZopeTestCase as ztc

from niteoweb.click2sell.tests import Click2SellControlPanelTestCase


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
