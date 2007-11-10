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

"""Define ``ZopeInstancesReadlines``, which can collect Zope instances
that are listed in a file.

$Id$
"""

from ximenez.collectors.collector import Collector
from ximenez.shared.zope import ZopeInstance


def getInstance():
    """Return an instance of ``ZopeInstancesReadlines``."""
    return ZopeInstancesReadlines()


## FIXME: This class should sub-class 'collectors.misc.Readlines'.
## This would simplify the implementation.
class ZopeInstancesReadlines(Collector):
    """A collector which returns instances of Zope servers that are
    listed in a file.

    It asks for the pathname of the file whose lines should have the
    following format::

        <host>:<port>

    Returns a tuple of ``ZopeInstance`` instances.
    """

    _input_info = ({'name': 'path',
                    'prompt': 'File: ',
                    'required': True},
                   )
    _multiple_input = False


    def getInput(self, cl_input=None):
        """Get input from the user if what was provided in the command
        line (available in ``cl_input``) was not sufficient.

        If a value is given in the command line (``cl_input``), we
        suppose it is the path of the file.
        """
        if cl_input:
            self._input['path'] = cl_input
        else:
            ## Back to the default implementation
            Collector.getInput(self, cl_input)


    def collect(self):
        """Return a tuple of ``ZopeInstance`` objects."""
        lines = open(self._input['path']).readlines()
        instances = []
        for line in lines:
            host, port = line.split(':')
            port = port.strip()
            instances.append(ZopeInstance(host, port))
        return instances
