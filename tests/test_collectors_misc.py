"""Tests for miscellaneous collectors.

$Id$
"""

from base import XimenezPluginTestCase, getCompletePathOfTestFile

from ximenez.collectors.misc.readlines import getInstance


class ReadLinesTestCase(XimenezPluginTestCase):
    """Test ``collectors.misc.readlines``."""

    def test_input(self):
        plugin = getInstance()
        path = '/path/to/file'
        plugin.getInput(cl_input=path)
        self.failUnless(plugin._input['path'] == path)


    def test_collect(self):
        plugin = getInstance()
        path = getCompletePathOfTestFile('lines.txt')
        self.setInput(plugin, path=path)
        collected = plugin.collect()
        self.failUnless(collected == ['first', 'second', 'third'])


if __name__ == '__main__':
    import unittest
    unittest.main()
