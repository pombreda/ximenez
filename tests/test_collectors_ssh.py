"""Tests for SSH-related collectors.

$Id$
"""

from base import XimenezPluginTestCase, getCompletePathOfTestFile

from ximenez.shared.ssh import SSHRemoteHost
from ximenez.collectors.ssh import instances
from ximenez.collectors.ssh import readlines


class SSHInstancesTestCase(XimenezPluginTestCase):
    """Test ``collectors.ssh.instances``."""

    def test_collect(self):
        plugin = instances.getInstance()
        self.setInput(plugin,
                      {'host': 'host1',
                       'port': '22'},
                      {'host': 'host2',
                       'port': '222'})
        collected = plugin.collect()
        self.failUnless(len(collected) == 2)
        self.failUnless(isinstance(collected[0], SSHRemoteHost))
        self.failUnless(str(collected[0]) == 'host1:22')
        self.failUnless(isinstance(collected[1], SSHRemoteHost))
        self.failUnless(str(collected[1]) == 'host2:222')


class SSHRemoteHostsReadlinesTestCase(XimenezPluginTestCase):
    """Test ``collectors.ssh.readlines``."""

    def test_input(self):
        plugin = readlines.getInstance()
        path = '/path/to/file'
        plugin.getInput(cl_input=path)
        self.failUnless(plugin._input['path'] == path)


    def test_collect(self):
        plugin = readlines.getInstance()
        path = getCompletePathOfTestFile('hosts.txt')
        self.setInput(plugin, path=path)
        collected = plugin.collect()
        self.failUnless(len(collected) == 2)
        self.failUnless(str(collected[0]) == 'localhost:22')
        self.failUnless(str(collected[1]) == '127.0.0.1:22')


if __name__ == '__main__':
    import unittest
    unittest.main()
