## Copyright (c) 2007 Damien Baty
##
## This file is part of Ximenez.
##
## Ximenez is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## Ximenez is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see
## <http://www.gnu.org/licenses/>.

"""Define various classes and functions related to Zope.

$Id$
"""

import re
import logging
import urllib2
from xmlrpclib import Fault
from xmlrpclib import ServerProxy

ROLES_REGEXP = re.compile('''<OPTION VALUE="(?:(.*))"(?:(.*))>''')
DOMAINS_REGEXP = re.compile('''<INPUT TYPE="TEXT" '''\
                            '''NAME="domains:tokens" '''\
                            '''SIZE="30"(?:\n|\r\n|\r)'''\
                            '''  VALUE="(.*?)"''')


class ZopeInstance(object):
    """Represent an instance of a Zope server."""
    def __init__(self, host, port):
        self.host = host
        self.port = port


    def __repr__(self):
        return ':'.join((self.host, self.port))


    def usesPAS(self, manager, manager_pwd):
        """Return ``True`` iff the server uses PAS (Pluggable Authentication
        Service) as its user folder (and not a standard user folder).

        We do that by trying an XML-RPC request on a method which the
        standard user folder does not implemente, whereas PAS does.
        """
        server = ServerProxy('http://%s:%s@%s:%s/acl_users' % (manager,
                                                               manager_pwd,
                                                               self.host,
                                                               self.port))
        try:
            server.searchPrincipals()
        except Fault, exc:
            if 'NotFound' in str(exc):
                return False
            logging.error('Could not guess whether the server uses '\
                          'PAS or not, because of an unexpected '\
                          'XML-RPC error:', exc_info=True)

        ## No error. That means the server does use PAS.
        return True


    def performCall(self, manager, manager_pwd, path, method, args):
        """Perform XML-RPC call on the current Zope instance."""
        server = ServerProxy('http://%s:%s@%s:%s/%s' % (manager,
                                                        manager_pwd,
                                                        self.host,
                                                        self.port,
                                                        path),
                             allow_none=True)
        return getattr(server, method)(*args)


    def addUser(self, userid, pwd, manager, manager_pwd):
        """Add ``userid``."""
        pas = self.usesPAS(manager, manager_pwd)

        if pas:
            path = 'acl_users/users'
            method = 'manage_addUser'
            args = (userid, userid, pwd, pwd, None)
        else:
            path = 'acl_users'
            method = 'userFolderAddUser'
            args = (userid, pwd, ['Manager'], [])

        ## FIXME: catch exception when the user already exists and
        ## raise our own exception that will be caught in the plug-in.
        ## With PAS, we get this:
        ## KeyError: 'Duplicate user ID: <userid>'
        self.performCall(manager, manager_pwd, path, method, args)

        if pas:
            # For PAS we must give the role manually
            path = 'acl_users/roles'
            method = 'assignRoleToPrincipal'
            args = ('Manager', userid,)
            self.performCall(manager, manager_pwd, path, method, args)


    def modifyUserPassword(self, userid, password,
                           manager, manager_pwd):
        """Set password of ``userid`` as ``password``."""
        if self.usesPAS(manager, manager_pwd):
            path = 'acl_users/users'
            method = 'manage_updateUserPassword'
            args = (userid, password, password, None)
        else:
            path = 'acl_users'
            method = 'userFolderEditUser'
            ## FIXME: call 'downloadUserEditForm()' and then pass over
            ## the result to 'getUser{Roles,Domains}()'. This will
            ## save one HTTP call.
            roles = self.getUserRoles(userid,
                                      manager, manager_pwd)
            domains = self.getUserDomains(userid,
                                          manager, manager_pwd)
            args = (userid, password, roles, domains)

        ## FIXME: catch exception when the user does not exist and
        ## raise our own exception that will be caught in the plug-in.
        ## With PAS, we get this:
        ## KeyError, Invalid user ID: <userid>
        self.performCall(manager, manager_pwd, path, method, args)


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

        ## FIXME: catch exception when the user does not exist and
        ## raise our own exception that will be caught in the plug-in.
        ## With PAS, we get this:
        ## KeyError, Invalid user ID: <userid>
        self.performCall(manager, manager_pwd, path, method, args)


    def downloadUserEditForm(self, userid, manager, manager_pwd):
        """Return HTML code of the edit form of the user.

        **Warning:** this only works for standard user folder, not
        PAS.
        """
        auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password('Zope',
                                  'http://%s:%s' % (self.host,
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
                     manager, manager_pwd, html=None):
        """Return roles of ``userid``.

        **Warning:** this only works for standard user folder, not
        PAS.
        """
        if html is None:
            html = self.downloadUserEditForm(userid,
                                             manager, manager_pwd)
        found = ROLES_REGEXP.findall(html)
        roles = [r for (r, selected) in found if selected]
        return roles


    def getUserDomains(self, userid, manager, manager_pwd, html=None):
        """Return domains of ``userid``.

        If ``html`` is not None, then we use it instead of trying to
        download the edit form.

        **Warning:** this only works for standard user folder, not
        PAS.
        """
        if html is None:
            html = self.downloadUserEditForm(userid,
                                             manager, manager_pwd)
        found = DOMAINS_REGEXP.search(html)
        domains = found.groups()[0].strip()
        domains = domains.split(' ')
        domains = [d.strip() for d in domains]
        return domains
