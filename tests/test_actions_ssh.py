"""Tests for SSH-related actions.

$Id$
"""

from base import XimenezPluginTestCase

from ximenez.shared.ssh import SSHRemoteHost
from ximenez.actions.ssh.remoteaction import getInstance
from ximenez.input import xim_raw_input


class SSHRemoteActionTestCase(XimenezPluginTestCase):
    """Test ``actions.ssh.remoteaction``."""

    def test_input(self):
        command = 'command'

        ## Manual input
        plugin = getInstance()
        plugin.getInput(cl_input=command)
        self.failUnlessEqual(plugin._input['command'], command)

        ## User input
        xim_raw_input.initializeLines((command, ))
        plugin = getInstance()
        plugin.getInput()
        self.failUnlessEqual(plugin._input['command'], command)
        self.failUnless(xim_raw_input.hasFinished())
        xim_raw_input.resetLines()


    def test_execute(self):
        plugin = getInstance()
        hosts = (SSHRemoteHost('localhost'),
                 SSHRemoteHost('127.0.0.1'),
                 SSHRemoteHost('nonexistent'))
        command = 'echo foo'
        self.setPluginInput(plugin, command=command)
        plugin.execute(hosts)
        expected = ['Executing "%s" on "%s":\n'\
                    'foo' % (command, str(hosts[0])),
                    'Executing "%s" on "%s":\n'\
                    'foo' % (command, str(hosts[1])),
                    'Could not connect to "%s".' % hosts[2]]
        self.failUnlessLogEqual(expected)
        self.clearLog()


def test_suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SSHRemoteActionTestCase))
    return suite


if __name__ == '__main__':
    import unittest
    unittest.main()
