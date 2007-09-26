"""Define various classes and functions related to Zope.

$Id$
"""

import re
import sys
import urllib2
import traceback
from xmlrpclib import ServerProxy, Fault

ROLES_REGEXP = re.compile('''<OPTION VALUE="(?:(.*))"(?:(.*))>''')
DOMAINS_REGEXP = re.compile('''<INPUT TYPE="TEXT" NAME="domains:tokens" SIZE="30"
  VALUE="(.*?)"''')


class ZopeInstance(object):
    """Represent an instance of a Zope server."""
    def __init__(self, host, port, version=None):
        self.host = host
        self.port = port
        self.version = version


    def __repr__(self):
        return ':'.join((self.host, self.port))


    def usesPAS(self, manager, manager_pwd):
        """Return ``True`` iff the server uses PAS (Pluggable Authentication
        Service) as its user folder (and not a standard user folder).

        We do that by trying an XML-RPC request on a method which the
        standard user folder does not implemente, whereas PAS does.
        """
        s = ServerProxy('http://%s:%s@%s:%s/acl_users' % (manager,
                                                          manager_pwd,
                                                          self.host,
                                                          self.port))
        try:
            s.searchPrincipals()
        except Fault, exc:
            if 'NotFound' in str(exc):
                return False
            print '---\n%s\n---\n' % exc
            ## We have got an error which was not expected.
            print 'Could not guess whether the server uses PAS or '\
                'not, because of an unexpected XML-RPC error.'
            traceback.print_exception(*sys.exc_info())

        ## No error. That means the server does use PAS.
        return True


    def performCall(self, manager, manager_pwd, path, method, args):
        server = ServerProxy('http://%s:%s@%s:%s/%s' % (manager,
                                                        manager_pwd,
                                                        self.host,
                                                        self.port,
                                                        path),
                             allow_none=True)
        return getattr(server, method)(*args)

    def removeUser(self, userid, manager, manager_pwd):
        """Remove ``userid``."""
        if self.usesPAS(manager, manager_pwd):
            path = 'acl_users/users'
            method = 'manage_removeUsers'
            args = ((userid, ), None)
        else:
            path = 'acl_users'
            method = 'userFolderDelUsers'
            args = ((userid, ), )

        ## FIXME: a 500 (internal server) error will probably be
        ## raised if the user does not exist.
        self.performCall(manager, manager_pwd, path, method, args)

    def addUser(self, userid, pwd, manager, manager_pwd):
        """Remove ``userid``."""
        pas = self.usesPAS(manager, manager_pwd)
        
        if pas:
            path = 'acl_users/users'
            method = 'manage_addUser'
            args = (userid, userid, pwd, pwd, None)
        else:
            path = 'acl_users'
            method = 'userFolderAddUser'
            args = (userid, pwd, [ 'Manager' ], None)

        self.performCall(manager, manager_pwd, path, method, args)

        if pas:
            # For PAS we must give the role manually
            path = 'acl_users/roles'
            method = 'assignRoleToPrincipal'
            args = ('Manager', userid,)
        self.performCall(manager, manager_pwd, path, method, args)            


    def modifyUserPassword(self, manager, manager_pwd,
                           userid, password):
        """Set password of ``userid`` as ``password``."""
        if self.usesPAS(manager, manager_pwd):
            path = 'acl_users/users'
            method = 'manage_updateUserPassword'
            args = (userid, password, password, None)
        else:
            path = 'acl_users'
            method = 'userFolderEditUser'
            roles = self.getUserRoles(userid,
                                      manager, manager_pwd)
            domains = self.getUserDomains(userid,
                                          manager, manager_pwd)
            args = (userid, password, roles, domains)

        self.performCall(manager, manager_pwd, path, method, args)


    def downloadUserEditForm(self, userid, manager, manager_pwd):
        """Return HTML code of the edit form of the user.

        **Warning:** this only works for standard user folder, not PAS.
        """
        auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password('Zope',
                                  '%s:%s' % (self.host,
                                             self.port),
                                  manager, manager_pwd)
        opener = urllib2.build_opener(auth_handler)
        url = 'http://%s:%s/acl_users/manage_users' % (self.host,
                                                       self.port)
        page = opener.open(url, data='name=%s&submit=Edit' % userid)
        html = page.read()
        page.close()
        return html


    def getUserRoles(self, userid,
                     manager, manager_pwd):
        """Return roles of ``userid``.

        **Warning:** this only works for standard user folder, not PAS.
        """
        html = self.downloadUserEditForm(userid,
                                         manager, manager_pwd)
        found = ROLES_REGEXP.findall(html)
        roles = [r for (r, selected) in found if selected]
        return roles


    def getUserDomains(self, userid, manager, manager_pwd):
        """Return domains of ``userid``.

        **Warning:** this only works for standard user folder, not PAS.
        """
        html = self.downloadUserEditForm(userid,
                                         manager, manager_pwd)
        found = DOMAINS_REGEXP.search(html)
        domains = found.groups()[0].split(' ')
        domains = [d.strip() for d in domains]
        return domains
