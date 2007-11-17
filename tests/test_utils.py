"""Tests for ``ximenez.utils`` module.

$Id$
"""

from base import XimenezTestCase


class UtilsTestCase(XimenezTestCase):

    def test_getPluginInstance(self):
        pass ## FIXME


def test_suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UtilsTestCase))
    return suite


if __name__ == '__main__':
    import unittest
    unittest.main()
