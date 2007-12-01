"""Tests for SSH-related collectors.

$Id$
"""

from base import XimenezPluginTestCase
from base import getCompletePathOfTestFile

from ximenez.input import xim_raw_input
from ximenez.shared.ssh import SSHRemoteHost
from ximenez.collectors.ssh import instances
from ximenez.collectors.ssh import readlines


class SSHInstancesTestCase(XimenezPluginTestCase):
    """Test ``collectors.ssh.instances``."""

    def test_input(self):
        hosts = [{'host': 'host1',
                  'port': '22'},
                 {'host': 'host2',
                  'port': '222'}]

        plugin = instances.getInstance()
        xim_raw_input.initializeLines(('host1', '22',
                                       'host2', '222',
                                       KeyboardInterrupt))
        plugin.getInput()
        self.failUnlessEqual(plugin._input, hosts)
        self.failUnless(xim_raw_input.hasFinished())
        xim_raw_input.resetLines()


    def test_collect(self):
        plugin = instances.getInstance()
        self.setPluginInput(plugin,
                            {'host': 'host1',
                             'port': '22'},
                            {'host': 'host2',
                             'port': '222'})
        collected = plugin.collect()
        self.failUnlessEqual(len(collected), 2)
        self.failUnless(isinstance(collected[0], SSHRemoteHost))
        self.failUnlessEqual(str(collected[0]), 'host1:22')
        self.failUnless(isinstance(collected[1], SSHRemoteHost))
        self.failUnlessEqual(str(collected[1]), 'host2:222')


class SSHRemoteHostsReadlinesTestCase(XimenezPluginTestCase):
    """Test ``collectors.ssh.readlines``."""

    def test_input(self):
        plugin = readlines.getInstance()

        ## Manual input
        path = '/path/to/file'
        plugin.getInput(cl_input=path)
        self.failUnlessEqual(plugin._input['path'], path)

        ## User input
        xim_raw_input.initializeLines((path, ))
        plugin.getInput()
        self.failUnlessEqual(plugin._input['path'], path)
        self.failUnless(xim_raw_input.hasFinished())
        xim_raw_input.resetLines()


    def test_collect(self):
        plugin = readlines.getInstance()
        path = getCompletePathOfTestFile('hosts.txt')
        self.setPluginInput(plugin, path=path)
        collected = plugin.collect()
        self.failUnlessEqual(len(collected), 2)
        self.failUnless(isinstance(collected[0], SSHRemoteHost))
        self.failUnlessEqual(str(collected[0]), 'localhost:22')
        self.failUnless(isinstance(collected[1], SSHRemoteHost))
        self.failUnlessEqual(str(collected[1]), '127.0.0.1:22')


def test_suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SSHInstancesTestCase))
    suite.addTest(unittest.makeSuite(SSHRemoteHostsReadlinesTestCase))
    return suite


if __name__ == '__main__':
    import unittest
    unittest.main()
