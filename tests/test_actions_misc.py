"""Tests for miscellaneous actions.

$Id$
"""

from base import XimenezPluginTestCase


class PrintTestCase(XimenezPluginTestCase):
    """Test ``actions.misc.print``."""
    pass ## FIXME


def test_suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PrintTestCase))
    return suite


if __name__ == '__main__':
    import unittest
    unittest.main()
