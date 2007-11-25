"""Tests for miscellaneous collectors.

$Id$
"""

from base import XimenezPluginTestCase
from base import getCompletePathOfTestFile

from ximenez.input import xim_raw_input
from ximenez.collectors.misc.readlines import getInstance


class ReadLinesTestCase(XimenezPluginTestCase):
    """Test ``collectors.misc.readlines``."""

    def test_input(self):
        plugin = getInstance()

        ## Manual input
        path = '/path/to/file'
        plugin.getInput(cl_input=path)
        self.failUnless(plugin._input['path'] == path)

        ## User input
        xim_raw_input.initializeLines((path, ))
        plugin.getInput()
        self.failUnless(plugin._input['path'] == path)
        self.failUnless(xim_raw_input.hasFinished())
        xim_raw_input.resetLines()


    def test_collect(self):
        plugin = getInstance()
        path = getCompletePathOfTestFile('lines.txt')
        self.setInput(plugin, path=path)
        collected = plugin.collect()
        self.failUnless(collected == ['first', 'second', 'third'])


def test_suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ReadLinesTestCase))
    return suite


if __name__ == '__main__':
    import unittest
    unittest.main()
