"""Tests for ``ximenez.shared.zope`` module.

$Id$
"""

from base import XimenezTestCase
from base import getCompletePathOfTestFile

from ximenez.shared import zope


MANAGER = 'ximenez'
PASSWORD = 'ximenez'
DOMAINS = ['localhost', '123.123.123.123'] ## Only used for non-PAS
                                           ## user folders
ROLES = ['Manager']
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
        pass ## FIXME self.failUnless(False)


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
