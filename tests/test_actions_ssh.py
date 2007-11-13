"""Tests for SSH-related actions.

$Id$
"""

from base import XimenezPluginTestCase

from ximenez.shared.ssh import SSHRemoteHost
from ximenez.actions.ssh.remoteaction import getInstance


class SSHRemoteActionTestCase(XimenezPluginTestCase):
    """Test ``actions.ssh.remoteaction``."""

    def test_input(self):
        plugin = getInstance()
        command = 'command'
        plugin.getInput(cl_input=command)
        self.failUnless(plugin._input['command'] == command)


    def test_execute(self):
        plugin = getInstance()
        hosts = (SSHRemoteHost('localhost'),
                 SSHRemoteHost('127.0.0.1'))
        command = 'echo foo'
        self.setInput(plugin, command=command)
        plugin.execute(hosts)
        expected = ['Executing "%s" on "%s":\n'\
                    'foo' % (command, str(hosts[0])),
                    'Executing "%s" on "%s":\n'\
                    'foo' % (command, str(hosts[1]))]
        self.failUnlessLogEqual(expected)
        self.clearLog()


if __name__ == '__main__':
    import unittest
    unittest.main()
