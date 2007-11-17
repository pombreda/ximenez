"""Tests for Zope-related actions.

$Id$
"""

from base import XimenezPluginTestCase


class ZopeUserAdderTestCase(XimenezPluginTestCase):
    """Test ``actions.zope.adduser``."""
    pass ## FIXME


class ZopeUserRemoverTestCase(XimenezPluginTestCase):
    """Test ``actions.zope.rmuser``."""
    pass ## FIXME


class ZopeUserPasswordModifierTestCase(XimenezPluginTestCase):
    """Test ``actions.zope.chpwduser``."""
    pass ## FIXME


def test_suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ZopeUserAdderTestCase))
    suite.addTest(unittest.makeSuite(ZopeUserRemoverTestCase))
    suite.addTest(unittest.makeSuite(ZopeUserPasswordModifierTestCase))
    return suite


if __name__ == '__main__':
    import unittest
    unittest.main()
