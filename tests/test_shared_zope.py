"""Tests for ``ximenez.shared.zope`` module.

$Id$
"""

from base import XimenezTestCase

from ximenez.shared import zope


class ZopeTestCase(XimenezTestCase):
    """A test case for ``ximenez.shared.zope`` module."""

    def test_getUserDomains(self):
        pass ## FIXME


    def test_getUserRoles(self):
        pass ## FIXME


def test_suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ZopeTestCase))
    return suite

if __name__ == '__main__':
    import unittest
    unittest.main()
