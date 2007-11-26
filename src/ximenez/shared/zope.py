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
from xmlrpclib import ProtocolError


ROLES_REGEXP = re.compile('''<OPTION VALUE="(?:(.*))"(?:(.*))>''')
DOMAINS_REGEXP = re.compile('''<INPUT TYPE="TEXT" '''\
                            '''NAME="domains:tokens" '''\
                            '''SIZE="30"(?:\n|\r\n|\r)'''\
                            '''  VALUE="(.*?)"''')

class UnauthorizedException(Exception):
    """User has not been authorized to do that."""

class UserAlreadyExistException(Exception):
    """User already exists."""

class UserDoNoExistException(Exception):
    """User does not exist."""


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
        try:
            self.performCall(manager, manager_pwd,
                             'acl_users', 'searchPrincipals')
        except Fault, exc:
            not_found = 'Unexpected Zope exception: zExceptions.NotFound'
            if exc.faultString.startswith(not_found):
                return False
            raise ## Re-raise original exception

        ## No error. That means the server does use PAS.
        return True


    def performCall(self, manager, manager_pwd, path, method, args=()):
        """Perform XML-RPC on the current Zope instance.

        This method might raise various exceptions, notably
        ``ProtocolError`` and ``Fault`` (both from ``xmlrpclib``), and
        also ``UnauthorizedException`` (which is actually a
        ``ProtocolError`` exception with a specific message, which we
        are able to detect).
        """
        url = 'http://%s:%s@%s:%s/%s' % (manager,
                                         manager_pwd,
                                         self.host,
                                         self.port,
                                         path)
        server = ServerProxy(url, allow_none=True)
        try:
            result = getattr(server, method)(*args)
        except ProtocolError, exc:
            if exc.errmsg == 'Unauthorized':
                raise UnauthorizedException()
            raise ## Re-raise original exception
        return result


    def addUser(self, userid, pwd, manager, manager_pwd):
        """Add ``userid``.

        This method may raise the following exceptions:

        - ``UnauthorizedException``;

        - ``UserAlreadyExistException``.

        Note that standard (non-PAS) user folder do **not** raise any
        exception when we try to add an user that already exists.
        Therefore, with this kind of user folder, this method actually
        **replaces** the user if it already exists, or add it
        otherwise.
        """
        pas = self.usesPAS(manager, manager_pwd)

        if pas:
            path = 'acl_users/users'
            method = 'manage_addUser'
            args = (userid, userid, pwd, pwd, None)
        else:
            path = 'acl_users'
            method = 'userFolderAddUser'
            args = (userid, pwd, ['Manager'], [])

        try:
            self.performCall(manager, manager_pwd, path, method, args)
        except Fault, exc:
            error = exc.faultString
            if error.find("'Duplicate user ID: %s'" % userid):
                raise UserAlreadyExistException()
            raise ## Re-raise original exception

        if pas:
            ## With a PAS user folder, we must give the role in a
            ## second step.
            path = 'acl_users/roles'
            method = 'assignRoleToPrincipal'
            args = ('Manager', userid,)
            self.performCall(manager, manager_pwd, path, method, args)


    def modifyUserPassword(self, userid, password,
                           manager, manager_pwd):
        """Set password of ``userid`` as ``password``.

        This method may raise the following exceptions:

        - ``UnauthorizedException``;

        - ``UserDoNoExistException``.
        """
        if self.usesPAS(manager, manager_pwd):
            path = 'acl_users/users'
            method = 'manage_updateUserPassword'
            args = (userid, password, password, None)
        else:
            path = 'acl_users'
            method = 'userFolderEditUser'
            edit_form = self.downloadUserEditForm(userid,
                                                  manager,
                                                  manager_pwd)

            roles = self.getUserRoles('', '', '', edit_form)
            domains = self.getUserDomains('', '', '', edit_form)
            args = (userid, password, roles, domains)

        try:
            self.performCall(manager, manager_pwd, path, method, args)
        except Fault, exc:
            error = exc.faultString
            if error.find("'Invalid user ID: %s'" % userid):
                raise UserDoNoExistException()
            raise ## Re-raise original exception


    def removeUser(self, userid, manager, manager_pwd):
        """Remove ``userid``.

        This method may raise the following exceptions:

        - ``UnauthorizedException``;

        - ``UserDoNoExistException``.
        """
        if self.usesPAS(manager, manager_pwd):
            path = 'acl_users/users'
            method = 'manage_removeUsers'
            args = ((userid, ), None)
        else:
            path = 'acl_users'
            method = 'userFolderDelUsers'
            args = ((userid, ), )

        try:
            self.performCall(manager, manager_pwd, path, method, args)
        except Fault, exc:
            error = exc.faultString
            if error.endswith("exceptions.KeyError - '%s'" % userid):
                raise UserDoNoExistException()
            if error.find("'Invalid user ID: %s'" % userid):
                raise UserDoNoExistException()
            raise ## Re-raise original exception


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
        try:
            page = opener.open(url, data='name=%s&submit=Edit' % userid)
        except urllib2.HTTPError, exc:
            if exc.msg == 'Unauthorized':
                raise UnauthorizedException()
            if exc.msg == 'Internal Server Error' and \
                    exc.hdrs.get('bobo-exception-type') == 'AttributeError':
                raise UserDoNoExistException()
            raise ## Re-raise original exception

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
        domains = found.groups()[0]
        domains = domains.split(' ')
        domains = [d for d in domains if d]
        return domains
