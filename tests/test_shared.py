"""Tests for ``ximenez.shared`` sub-package.

$Id$
"""

from base import XimenezTestCase

from ximenez.shared import ssh, zope


class ZopeTestCase(XimenezTestCase):
    """A test case for ``ximenez.shared.zope`` module."""

    def test_getUserDomains(self):
        pass ## FIXME


    def test_getUserRoles(self):
        pass ## FIXME


class SSHTestCase(XimenezTestCase):
    """A test case for ``ximenez.shared.ssh`` module."""

    def test_escapeShellCommand(self):
        commands = ('ls',
                    'cd /var ; ls',
                    'cd && ls',
                    'cd || ls',
                    'ls &',
                    'ls | grep foo',
                    'echo Foo!',
                    'echo !!',
                    'ls > foo',
                    'ls < foo',
                    'ls ~',
                    'ls *',
                    'ls {foo,bar}.txt',
                    'ls [fb]oo',
                    'ls ?oo',
                    '(ls)',
                    'echo US$380',
                    'echo 1\\2',
                    'echo `foo`')
        from popen2 import popen3
        for command in commands:
            escaped = ssh.escapeShellCommand(command)
            stdout, _, _ = popen3('echo %s' % escaped)
            self.failUnlessEqual(stdout.read().strip(), command)


    def test_executeShellCommand(self):
        host = ssh.SSHRemoteHost('localhost')
        self.failUnlessEqual(host.execute('echo "foo"'), 'foo')
        self.failUnlessEqual(host.execute('ls /doesnotexist'),
                             'ls: /doesnotexist: No such file or directory')


def test_suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ZopeTestCase))
    suite.addTest(unittest.makeSuite(SSHTestCase))
    return suite

if __name__ == '__main__':
    import unittest
    unittest.main()
