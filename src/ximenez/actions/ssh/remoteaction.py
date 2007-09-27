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

"""Define SSHRemoteAction, a plug-in which can execute a command on a
remote host via SSH.

$Id$
"""

from ximenez.actions.action import Action


def getInstance():
    """Return an instance of SSHRemoteAction."""
    return SSHRemoteAction()


class SSHRemoteAction(Action):
    """Connect to remote hosts via SSH, execute a command and return
    its output.
    """

    _input_info = ({'name': 'command',
                    'prompt': 'Command: ',
                    'required': True}, )


    def getInput(self, cl_input=None):
        """Get input from the user if what was provided in the command
        line (available in ``cl_input``) was not sufficient.

        If a value is given in the command line (``cl_input``), we
        suppose it is the command to execute.
        """
        if cl_input:
            self._input['command'] = cl_input
        else:
            ## Back to the default implementation
            Action.getInput(self, cl_input)


    def execute(self, sequence):
        """Connect to each host of ``sequence`` and execute a
        command.
        """
        command = self._input['command']
        for item in sequence:
            self.log('Executing "%s" on "%s"\n' % (command, item))
            self.log(item.execute(command), no_date=True)
            self.endLogSection()
