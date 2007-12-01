"""Tests for Zope-related actions.

$Id$
"""

from base import XimenezPluginTestCase
from zopetestsbase import MANAGER
from zopetestsbase import PASSWORD
from zopetestsbase import DUMMY_USER
from zopetestsbase import HOST
from zopetestsbase import PORTS_NO_PAS
from zopetestsbase import PORTS_PAS

from ximenez.input import xim_raw_input
from ximenez.actions.zope import adduser
from ximenez.actions.zope import rmuser
from ximenez.actions.zope import chpwduser
from ximenez.shared.zope import ZopeInstance
from ximenez.shared.zope import UnauthorizedException
from ximenez.shared.zope import UserDoNoExistException
from ximenez.shared.zope import UserAlreadyExistException


class ZopeUserAdderTestCase(XimenezPluginTestCase):
    """Test ``actions.zope.adduser``."""

    def test_input(self):
        ## Manual input
        plugin = adduser.getInstance()
        cl_input_data = {'user': 'new_user',
                         'user_pwd': 'password',
                         'manager': 'manager',
                         'manager_pwd': 'secret'}
        cl_input = ';;'.join(['='.join((key, value)) \
                              for key, value in cl_input_data.items()])
        plugin.getInput(cl_input=cl_input)
        for key, value in cl_input_data.items():
            self.failUnlessEqual(plugin._input[key], value)

        ## User input
        xim_raw_input.initializeLines(('new_user', 'password',
                                       'manager', 'secret'))
        plugin = adduser.getInstance()
        plugin.getInput()
        for key, value in cl_input_data.items():
            self.failUnlessEqual(plugin._input[key], value)
        self.failUnless(xim_raw_input.hasFinished())
        xim_raw_input.resetLines()


    def test_execute(self):
        password = 'password'
        instances = []
        for port in PORTS_NO_PAS + PORTS_PAS:
            instances.append(ZopeInstance(HOST, port))

        ## Try with a wrong manager password
        plugin = adduser.getInstance()
        self.setPluginInput(plugin,
                            user=DUMMY_USER,
                            user_pwd=password,
                            manager=MANAGER,
                            manager_pwd='wrong-password')
        plugin.execute(instances)
        expected = []
        for instance in instances:
            expected.append('"%s" is not authorized to add user '\
                            'on "%s".' % (MANAGER, instance))
        self.failUnlessLogEqual(expected)
        self.clearLog()

        ## Try with an user that already exists
        plugin = adduser.getInstance()
        self.setPluginInput(plugin,
                            user=MANAGER,
                            user_pwd=password,
                            manager=MANAGER,
                            manager_pwd=PASSWORD)
        plugin.execute(instances)
        expected = []
        for instance in instances:
            expected.append('"%s" already exists on "%s".' %\
                            (MANAGER, instance))
        self.failUnlessLogEqual(expected)
        self.clearLog()

        ## At last, do it for real
        plugin = adduser.getInstance()
        self.setPluginInput(plugin,
                            user=DUMMY_USER,
                            user_pwd=password,
                            manager=MANAGER,
                            manager_pwd=PASSWORD)
        plugin.execute(instances)
        expected = []
        for instance in instances:
            expected.append('Added "%s" on "%s".' % (DUMMY_USER, instance))
        self.failUnlessLogEqual(expected)
        self.clearLog()

        ## Check that the user has been added by trying to change its
        ## own password: if no exception is raised, then everything is
        ## alright.
        ## We also remove the user for other tests.
        for instance in instances:
            instance.modifyUserPassword(DUMMY_USER, 'new-password',
                                        DUMMY_USER, password)
            instance.removeUser(DUMMY_USER, MANAGER, PASSWORD)


class ZopeUserRemoverTestCase(XimenezPluginTestCase):
    """Test ``actions.zope.rmuser``."""

    def test_input(self):
        ## Manual input
        plugin = rmuser.getInstance()
        cl_input_data = {'user': 'user',
                         'manager': 'manager',
                         'manager_pwd': 'secret'}
        cl_input = ';;'.join(['='.join((key, value)) \
                              for key, value in cl_input_data.items()])
        plugin.getInput(cl_input=cl_input)
        for key, value in cl_input_data.items():
            self.failUnlessEqual(plugin._input[key], value)

        ## User input
        xim_raw_input.initializeLines(('user', 'manager', 'secret'))
        plugin = rmuser.getInstance()
        plugin.getInput()
        for key, value in cl_input_data.items():
            self.failUnlessEqual(plugin._input[key], value)
        self.failUnless(xim_raw_input.hasFinished())
        xim_raw_input.resetLines()


    def test_execute(self):
        instances = []
        for port in PORTS_NO_PAS + PORTS_PAS:
            instances.append(ZopeInstance(HOST, port))

        ## Try with a wrong manager password
        plugin = rmuser.getInstance()
        self.setPluginInput(plugin,
                            user=DUMMY_USER,
                            manager=MANAGER,
                            manager_pwd='wrong-password')
        plugin.execute(instances)
        expected = []
        for instance in instances:
            expected.append('"%s" is not authorized to remove user '\
                            'on "%s".' % (MANAGER, instance))
        self.failUnlessLogEqual(expected)
        self.clearLog()

        ## Try with an user that does not exist
        plugin = rmuser.getInstance()
        self.setPluginInput(plugin,
                            user='nonexistent-user',
                            manager=MANAGER,
                            manager_pwd=PASSWORD)
        plugin.execute(instances)
        expected = []
        for instance in instances:
            expected.append('"%s" does not exist on "%s".' %\
                            ('nonexistent-user', instance))
        self.failUnlessLogEqual(expected)
        self.clearLog()

        ## At last, add a dummy user and remove it
        for instance in instances:
            instance.addUser(DUMMY_USER, 'pwd', MANAGER, PASSWORD)
        plugin = rmuser.getInstance()
        self.setPluginInput(plugin,
                            user=DUMMY_USER,
                            manager=MANAGER,
                            manager_pwd=PASSWORD)
        plugin.execute(instances)
        expected = []
        for instance in instances:
            expected.append('Removed "%s" on "%s".' % \
                            (DUMMY_USER, instance))
        self.failUnlessLogEqual(expected)
        self.clearLog()

        ## Check that the user has been removed by trying to change
        ## its own password.
        for instance in instances:
            self.failUnlessRaises(UserDoNoExistException,
                                  instance.modifyUserPassword,
                                  DUMMY_USER, 'new-password',
                                  MANAGER, PASSWORD)


class ZopeUserPasswordModifierTestCase(XimenezPluginTestCase):
    """Test ``actions.zope.chpwduser``."""

    def test_input(self):
        ## Manual input
        plugin = chpwduser.getInstance()
        cl_input_data = {'user': 'new_user',
                         'user_pwd': 'password',
                         'manager': 'manager',
                         'manager_pwd': 'secret'}
        cl_input = ';;'.join(['='.join((key, value)) \
                              for key, value in cl_input_data.items()])
        plugin.getInput(cl_input=cl_input)
        for key, value in cl_input_data.items():
            self.failUnlessEqual(plugin._input[key], value)

        ## User input
        xim_raw_input.initializeLines(('new_user', 'password',
                                       'manager', 'secret'))
        plugin = chpwduser.getInstance()
        plugin.getInput()
        for key, value in cl_input_data.items():
            self.failUnlessEqual(plugin._input[key], value)
        self.failUnless(xim_raw_input.hasFinished())
        xim_raw_input.resetLines()


    def test_execute(self):
        password = 'password'
        instances = []
        for port in PORTS_NO_PAS + PORTS_PAS:
            instances.append(ZopeInstance(HOST, port))

        ## Try with a wrong manager password
        plugin = chpwduser.getInstance()
        self.setPluginInput(plugin,
                            user=DUMMY_USER,
                            user_pwd=password,
                            manager=MANAGER,
                            manager_pwd='wrong-password')
        plugin.execute(instances)
        expected = []
        for instance in instances:
            expected.append('"%s" is not authorized to change user\'s '\
                            'password on "%s".' % (MANAGER, instance))
        self.failUnlessLogEqual(expected)
        self.clearLog()

        ## Try with an user that already exists
        plugin = chpwduser.getInstance()
        self.setPluginInput(plugin,
                            user='nonexistent-user',
                            user_pwd=password,
                            manager=MANAGER,
                            manager_pwd=PASSWORD)
        plugin.execute(instances)
        expected = []
        for instance in instances:
            expected.append('"%s" does not exist on "%s".' %\
                            ('nonexistent-user', instance))
        self.failUnlessLogEqual(expected)
        self.clearLog()

        ## At last, add a dummy user and modify its password for real
        for instance in instances:
            instance.addUser(DUMMY_USER, 'dummy', MANAGER, PASSWORD)
        plugin = chpwduser.getInstance()
        self.setPluginInput(plugin,
                            user=DUMMY_USER,
                            user_pwd=password,
                            manager=MANAGER,
                            manager_pwd=PASSWORD)
        plugin.execute(instances)
        expected = []
        for instance in instances:
            expected.append('Changed password of "%s" on "%s".' %\
                            (DUMMY_USER, instance))
        self.failUnlessLogEqual(expected)
        self.clearLog()

        ## Check that the user has been added by trying to change its
        ## own password: if no exception is raised, then everything is
        ## alright.
        ## We also remove the user for other tests.
        for instance in instances:
            instance.modifyUserPassword(DUMMY_USER, 'new-password',
                                        DUMMY_USER, password)
            instance.removeUser(DUMMY_USER, MANAGER, PASSWORD)


def test_suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ZopeUserAdderTestCase))
    suite.addTest(unittest.makeSuite(ZopeUserRemoverTestCase))
    suite.addTest(unittest.makeSuite(ZopeUserPasswordModifierTestCase))
    return suite


if __name__ == '__main__':
    import unittest
    unittest.main()
