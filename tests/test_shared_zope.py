"""Tests for ``ximenez.shared.zope`` module.

$Id$
"""

from base import XimenezTestCase
from base import getCompletePathOfTestFile
from zopetestsbase import MANAGER
from zopetestsbase import PASSWORD
from zopetestsbase import DOMAINS
from zopetestsbase import ROLES
from zopetestsbase import DUMMY_USER
from zopetestsbase import HOST
from zopetestsbase import PORTS_NO_PAS
from zopetestsbase import PORTS_PAS

from ximenez.shared import zope


class ZopeTestCase(XimenezTestCase):
    """A test case for ``ximenez.shared.zope`` module.

    Some of these tests presume that there are Zope servers listening
    on the local host, with a specific user. See some of the constants
    defined in the ``zopetestsbase`` module for further details.
    """

    def test_usesPAS(self):
        for port in PORTS_PAS:
            instance = zope.ZopeInstance(HOST, port)
            self.failUnless(instance.usesPAS(MANAGER, PASSWORD))
        for port in PORTS_NO_PAS:
            instance = zope.ZopeInstance(HOST, port)
            self.failUnless(not instance.usesPAS(MANAGER, PASSWORD))


    def test_userManagement(self):
        ## WARNING: this test tries to add, modify and then remove an
        ## user in all Zope test instances. If this test fails, it
        ## will probably leave remnants in some user folders.
        for port in PORTS_NO_PAS + PORTS_PAS:
            instance = zope.ZopeInstance(HOST, port)

            ## Add user
            self.failUnlessRaises(zope.UnauthorizedException,
                                  instance.addUser,
                                  DUMMY_USER, 'password',
                                  MANAGER, 'wrong-password')
            self.failUnlessRaises(zope.UserAlreadyExistException,
                                  instance.addUser,
                                  MANAGER,  'password',
                                  MANAGER, PASSWORD)
            instance.addUser(DUMMY_USER, 'password',
                             MANAGER, PASSWORD)
            ## We do not test anything, here. If the user was not
            ## added, we will have an error later, anyway.

            ## Modify user password
            NEW_PASSWORD = 'new-password'
            self.failUnlessRaises(zope.UnauthorizedException,
                                  instance.modifyUserPassword,
                                  DUMMY_USER, NEW_PASSWORD,
                                  MANAGER, 'wrong-password')
            self.failUnlessRaises(zope.UserDoNoExistException,
                                  instance.modifyUserPassword,
                                  'nonexistent-user', NEW_PASSWORD,
                                  MANAGER, PASSWORD)
            instance.modifyUserPassword(DUMMY_USER, NEW_PASSWORD,
                                        MANAGER, PASSWORD)
            ## To test the new password, we try to change our dummy
            ## users's password with the dummy user itself. If we do
            ## not get any error, then the password has effectively
            ## been changed.
            instance.modifyUserPassword(DUMMY_USER, 'more-secret',
                                        DUMMY_USER, NEW_PASSWORD)

            ## Remove user
            self.failUnlessRaises(zope.UnauthorizedException,
                                  instance.removeUser,
                                  DUMMY_USER,
                                  MANAGER, 'wrong-password')
            instance.removeUser(DUMMY_USER, MANAGER, PASSWORD)
            self.failUnlessRaises(zope.UserDoNoExistException,
                                  instance.removeUser,
                                  DUMMY_USER,
                                  MANAGER, PASSWORD)


    def test_downloadUserEditForm(self):
        for port in PORTS_NO_PAS:
            instance = zope.ZopeInstance(HOST, port)
            html = instance.downloadUserEditForm(MANAGER,
                                                 MANAGER, PASSWORD)
            expected = open(getCompletePathOfTestFile('edit_form.html')).read()
            self.failUnlessEqual(html, expected)


    def test_getUserDomains(self):
        for port in PORTS_NO_PAS:
            instance = zope.ZopeInstance(HOST, port)
            domains = instance.getUserDomains(MANAGER,
                                              MANAGER, PASSWORD)
            self.failUnlessEqual(domains, DOMAINS)

            html = getCompletePathOfTestFile('edit_form.html')
            html = open(html).read()
            domains = instance.getUserDomains('', '', '', html)
            self.failUnlessEqual(domains, DOMAINS)


    def test_getUserRoles(self):
        for port in PORTS_NO_PAS:
            instance = zope.ZopeInstance(HOST, port)
            roles = instance.getUserRoles(MANAGER,
                                          MANAGER, PASSWORD)
            self.failUnlessEqual(roles, ROLES)

            html = getCompletePathOfTestFile('edit_form.html')
            html = open(html).read()
            roles = instance.getUserRoles('', '', '', html)
            self.failUnlessEqual(roles, ROLES)


def test_suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ZopeTestCase))
    return suite

if __name__ == '__main__':
    import unittest
    unittest.main()
