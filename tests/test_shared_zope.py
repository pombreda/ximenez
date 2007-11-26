"""Tests for ``ximenez.shared.zope`` module.

$Id$
"""

from base import XimenezTestCase
from base import getCompletePathOfTestFile

from ximenez.shared import zope


MANAGER = 'ximenez'
PASSWORD = 'ximenez'
## ``DOMAINS`` and ``ROLES`` are only used for non-PAS user folders
DOMAINS = ['localhost', '123.123.123.123']
ROLES = ['Manager']
DUMMY_USER = 'ximenez_dummy'
HOST = 'localhost'
PORTS_NO_PAS = (8081, )
PORTS_PAS = (8091, 8101)

class ZopeTestCase(XimenezTestCase):
    """A test case for ``ximenez.shared.zope`` module.

    Some of these presume that there are Zope servers listening on the
    local host, with a specific user. See some of the constants
    defined above.
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
            if instance.usesPAS(MANAGER, PASSWORD):
                ## Standard (non-PAS) user folders do _not_ raise any
                ## exception when we try to add an user that already
                ## exists. In this case, it simply replaces it.
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
            self.failUnless(html == expected)


    def test_getUserDomains(self):
        for port in PORTS_NO_PAS:
            instance = zope.ZopeInstance(HOST, port)
            domains = instance.getUserDomains(MANAGER,
                                              MANAGER, PASSWORD)
            self.failUnless(domains == DOMAINS)

            html = getCompletePathOfTestFile('edit_form.html')
            html = open(html).read()
            domains = instance.getUserDomains('', '', '', html)
            self.failUnless(domains == DOMAINS)


    def test_getUserRoles(self):
        for port in PORTS_NO_PAS:
            instance = zope.ZopeInstance(HOST, port)
            roles = instance.getUserRoles(MANAGER,
                                          MANAGER, PASSWORD)
            self.failUnless(roles == ROLES)

            html = getCompletePathOfTestFile('edit_form.html')
            html = open(html).read()
            roles = instance.getUserRoles('', '', '', html)
            self.failUnless(roles == ROLES)


def test_suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ZopeTestCase))
    return suite

if __name__ == '__main__':
    import unittest
    unittest.main()
