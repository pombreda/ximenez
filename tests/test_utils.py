"""Tests for ``ximenez.utils`` module.

$Id$
"""

import os.path

from base import XimenezTestCase

from ximenez import utils


class UtilsTestCase(XimenezTestCase):

    def test_getPluginInstance(self):
        m = utils.getPluginInstance

        ## Get module by dotted name
        self.failUnless(m('misc.readlines', 'collectors'))
        self.failUnless(m('misc.print', 'actions'))
        self.failUnlessRaises(ImportError,
                              m, 'misc.print', 'collectors')
        self.failUnlessRaises(ImportError,
                              m, 'misc.print', 'bogus_kind')
        self.failUnlessRaises(ImportError, m, 'misc.readlines')

        ## Get module by path
        base_dir = os.path.dirname(utils.__file__)
        path = os.path.join(base_dir, 'collectors', 'misc', 'readlines.py')
        self.failUnless(m(path))
        path = os.path.join(base_dir, 'actions', 'misc', 'print.py')
        self.failUnless(m(path))
        path = os.path.join(base_dir, 'collectors', 'misc', 'print.py')
        self.failUnlessRaises(ImportError, m, path)


def test_suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UtilsTestCase))
    return suite


if __name__ == '__main__':
    import unittest
    unittest.main()
