"""Tests for miscellaneous actions.

$Id$
"""

from base import XimenezPluginTestCase

from ximenez.actions.misc import log

class LogTestCase(XimenezPluginTestCase):
    """Test ``actions.misc.log``."""

    def test_execute(self):
        plugin = log.getInstance()
        items = ['first', 'second', 'third']
        plugin.execute(items)
        self.failUnlessLogEqual(items)
        self.clearLog()


def test_suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LogTestCase))
    return suite


if __name__ == '__main__':
    import unittest
    unittest.main()
