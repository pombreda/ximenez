"""Tests for Zope-related collectors.

$Id$
"""

from base import XimenezPluginTestCase, getCompletePathOfTestFile

from ximenez.collectors.zope import instances
from ximenez.collectors.zope import readlines


class ZopeInstancesTestCase(XimenezPluginTestCase):
    """Test ``collectors.zope.instances``."""

    def test_collect(self):
        plugin = instances.getInstance()
        self.setInput(plugin,
                      {'host': 'host1',
                       'port': '8080'},
                      {'host': 'host2',
                       'port': '8082'})
        collected = plugin.collect()
        self.failUnless(len(collected) == 2)
        self.failUnless(str(collected[0]) == 'host1:8080')
        self.failUnless(str(collected[1]) == 'host2:8082')


class ZopeInstancesReadlinesTestCase(XimenezPluginTestCase):
    """Test ``collectors.zope.readlines``."""

    def test_input(self):
        plugin = readlines.getInstance()
        path = '/path/to/file'
        plugin.getInput(cl_input=path)
        self.failUnless(plugin._input['path'] == path)


    def test_collect(self):
        plugin = readlines.getInstance()
        path = getCompletePathOfTestFile('zope-instances.txt')
        self.setInput(plugin, path=path)
        collected = plugin.collect()
        self.failUnless(len(collected) == 3)
        self.failUnless(str(collected[0]) == 'localhost:8081')
        self.failUnless(str(collected[1]) == 'localhost:8091')
        self.failUnless(str(collected[2]) == 'localhost:8101')


if __name__ == '__main__':
    import unittest
    unittest.main()
