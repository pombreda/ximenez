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

"""Define ``PrintAction``, a plug-in which simply logs items of a
given sequence.

$Id$
"""

from ximenez.actions.action import Action


def getInstance():
    """Return an instance of ``PrintAction``."""
    return PrintAction()


class PrintAction(Action):
    """A very simple action, which logs each item returned by the
    collector.
    """

    _input_info = ()

    def execute(self, sequence):
        """Log each item of ``sequence``."""
        for item in sequence:
            self.log(str(item), no_date=True)
