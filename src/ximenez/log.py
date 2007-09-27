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

"""Define ``Logger`` class and ``LogAware`` mixin.

$Id$
"""

import os
import traceback
from time import strftime


PREFIX = '%s -- '
DEFAULT_DATE_FORMAT = '%d/%m/%Y %H:%M:%S'


class LoggerAware:
    """Mixin class which defines log-related methods through a
    registered ``Logger`` instance.
    """

    def setLogger(self, logger):
        """Set a logger for ``self``."""
        self._logger = logger


    def log(self, *args, **kwargs):
        """Log a message through the registered logger."""
        self._logger.log(*args, **kwargs)


    def logLastTraceback(self):
        """Log last traceback."""
        self._logger.logLastTraceback()


    def endLogSection(self, msg=None):
        """End log section."""
        self._logger.endSection(msg)


class Logger(object):
    """A class which provides logging-related features."""

    def __init__(self, output, date_format=DEFAULT_DATE_FORMAT):
        """Initialize the logger by registering the output and setting
        a date format string.

        ``output`` should be a file descriptor.
        """
        self._output = output
        self._date_format = date_format


    def getDateAsString(self):
        """Return the current date as a string, conforming to the
        ``_date_format`` attribute.
        """
        return strftime(self._date_format)


    def log(self, msg, no_date=False):
        """Write ``msg`` to the registered output.

        It adds the date to the first line of ``msg``, and pad the
        following lines with spaces.
        """
        if no_date:
            msg = msg + os.linesep
            self._output.write(msg)
        else:
            ## FIXME: this piece of code has to be tested. (Damien)
            date = self.getDateAsString()
            prefix = PREFIX % date
            blank_prefix = PREFIX % (' ' * len(date))
            prefixed_msg = []
            first_line = True
            for line in msg.splitlines():
                prefixed_line = line + os.linesep
                if first_line:
                    prefixed_line = prefix + prefixed_line
                    first_line = False
                else:
                    prefixed_line = blank_prefix + prefixed_line
                prefixed_msg.append(prefixed_line)
            prefixed_msg = os.linesep.join(prefixed_msg)
            self._output.write(prefixed_msg)


    def logLastTraceback(self):
        """Write last traceback to the registered output."""
        traceback.print_exc(file=self._output)


    def endSection(self, msg=None):
        """Write a line of ``-``."""
        write = self._output.write
        write('-' * 60)
        write('\n')
