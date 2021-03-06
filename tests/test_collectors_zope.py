"""Tests for Zope-related collectors.

$Id$
"""

from base import XimenezPluginTestCase
from base import getCompletePathOfTestFile

from ximenez.input import xim_raw_input
from ximenez.shared.zope import ZopeInstance
from ximenez.collectors.zope import instances
from ximenez.collectors.zope import readlines


class ZopeInstancesTestCase(XimenezPluginTestCase):
    """Test ``collectors.zope.instances``."""


    def test_input(self):
        hosts = [{'host': 'host1',
                  'port': '8080'},
                 {'host': 'host2',
                  'port': '8082'}]

        plugin = instances.getInstance()
        xim_raw_input.initializeLines(('host1', '8080',
                                       'host2', '8082',
                                       KeyboardInterrupt))
        plugin.getInput()
        self.failUnlessEqual(plugin._input, hosts)
        self.failUnless(xim_raw_input.hasFinished())
        xim_raw_input.resetLines()


    def test_collect(self):
        plugin = instances.getInstance()
        self.setPluginInput(plugin,
                            {'host': 'host1',
                             'port': '8080'},
                            {'host': 'host2',
                             'port': '8082'})
        collected = plugin.collect()
        self.failUnlessEqual(len(collected), 2)
        self.failUnless(isinstance(collected[0], ZopeInstance))
        self.failUnlessEqual(str(collected[0]), 'host1:8080')
        self.failUnless(isinstance(collected[1], ZopeInstance))
        self.failUnlessEqual(str(collected[1]), 'host2:8082')


class ZopeInstancesReadlinesTestCase(XimenezPluginTestCase):
    """Test ``collectors.zope.readlines``."""

    def test_input(self):
        plugin = readlines.getInstance()

        ## Manual input
        path = '/path/to/file'
        plugin.getInput(cl_input=path)
        self.failUnless(plugin._input['path'] == path)

        ## User input
        xim_raw_input.initializeLines((path, ))
        plugin.getInput()
        self.failUnlessEqual(plugin._input['path'], path)
        self.failUnless(xim_raw_input.hasFinished())
        xim_raw_input.resetLines()


    def test_collect(self):
        plugin = readlines.getInstance()
        path = getCompletePathOfTestFile('zope-instances.txt')
        self.setPluginInput(plugin, path=path)
        collected = plugin.collect()
        self.failUnlessEqual(len(collected), 3)
        self.failUnless(isinstance(collected[0], ZopeInstance))
        self.failUnlessEqual(str(collected[0]), 'localhost:8081')
        self.failUnless(isinstance(collected[1], ZopeInstance))
        self.failUnlessEqual(str(collected[1]), 'localhost:8091')
        self.failUnless(isinstance(collected[2], ZopeInstance))
        self.failUnlessEqual(str(collected[2]), 'localhost:8101')


def test_suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ZopeInstancesTestCase))
    suite.addTest(unittest.makeSuite(ZopeInstancesReadlinesTestCase))
    return suite


if __name__ == '__main__':
    import unittest
    unittest.main()
