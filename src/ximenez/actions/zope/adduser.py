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

"""Define ``ZopeUserAdder``, a plug-in which connects to Zope
instances via XML-RPC and tries to create a Manager user.

$Id$
"""

import logging

from ximenez.actions.action import Action
from ximenez.shared.zope import ZopeInstance
from ximenez.shared.zope import UnauthorizedException
from ximenez.shared.zope import UserAlreadyExistException


def getInstance():
    """Return an instance of ZopeUserAdder."""
    return ZopeUserAdder()


class ZopeUserAdder(Action):
    """An action which adds an user to a collection of Zope instances
    via XML-RPC.
    """

    _input_info = ()

    def getInput(self, cl_input=None):
        """Get input from the user."""
        if cl_input:
            ## Default handling of command line input.
            Action.getInput(self, cl_input)
            return

        ask = self.askForInput
        self._input.update(ask(({'name': 'user',
                                 'prompt': 'User id to create: ',
                                 'required': True
                                 },
                                {'name': 'user_pwd',
                                 'prompt': 'Password of the new user: ',
                                 'required': True,
                                 'hidden': True
                                 },)
                               ))

        self._input.update(ask(({'name': 'manager',
                                 'prompt': 'Manager username: ',
                                 'required': True
                                 },
                                {'name': 'manager_pwd',
                                 'prompt': 'Manager password: ',
                                 'required': True,
                                 'hidden': True
                                 },)
                                ))


    def execute(self, instances):
        """Create an user on each item of ``instances``.

        ``instances`` is supposed to be a sequence of ``ZopeInstance``
        instances or ``<host>:<port>`` strings.
        """
        manager = self._input['manager']
        manager_pwd = self._input['manager_pwd']
        user = self._input['user']
        user_pwd = self._input['user_pwd']

        for instance in instances:
            if not isinstance(instance, ZopeInstance):
                host, port = instance.split(":")
                instance = ZopeInstance(host, port)
            try:
                instance.addUser(user, user_pwd, manager, manager_pwd)
            except UnauthorizedException:
                msg = '"%s" is not authorized to add user '\
                    'on "%s".'
                logging.error(msg, manager, instance)
            except UserAlreadyExistException:
                msg = '"%s" already exists on "%s".'
                logging.error(msg, user, instance)
            except:
                logging.error('Could not add "%s" to "%s" '\
                              'because of an unexpected exception: ',
                              user, instance, exc_info=True)
