#!/usr/bin/env python
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

"""Main file for Ximenez.

$Id$
"""

import sys
import time
import getopt
import socket
import traceback

from ximenez.log import Logger
from ximenez.utils import getPluginInstance


USAGE = """\
Standard usage: %s -c <collector> -a <action>

-h, --help
  Display help and exit.

-v, --version
  Display version and exit.

-c <collector>
  Use <collector> plug-in.

--ci <input>
  Provide input to te collector plug-in.

-a <action>
  Use <action> plug-in.

--ai <input>
  Provide input to the action plug-in.

-o <output-file>, --outfile <output-file>
  Log to <output-file>.

See the documentation for further details.""" % sys.argv[0]

DEFAULT_TIMEOUT = 3
socket.setdefaulttimeout(DEFAULT_TIMEOUT)


def version():
    """Print version."""
    ## FIXME: this is not the right way to do it. 'VERSION.txt' will
    ## not be installed.
    f = open('VERSION.txt', 'r')
    print 'Ximenez %s' % f.read()
    f.close()


def main():
    """Collect informations and execute action."""
    try:
        options, args = getopt.getopt(sys.argv[1:],
                                      'hva:c:o:',
                                      ['help', 'version',
                                       'output=',
                                       'ai=', 'ci='])
    except getopt.GetoptError:
        print USAGE
        sys.exit(1)

    action = None
    collector = None
    action_input = None
    collector_input = None
    output_path = None
    for option, value in options:
        if option == '-a':
            action = value
        elif option == '-c':
            collector = value
        elif option == '--ai':
            action_input = value
        elif option == '--ci':
            collector_input = value
        elif option in ('-o', '--output'):
            output_path = value
        elif option in ('-h', '--help'):
            print USAGE
            sys.exit(0)
        elif option in ('-v', '--version'):
            version()
            sys.exit(0)

    ## A collector and an action are both required.
    if not action or not collector:
        print 'Error: wrong arguments.'
        print USAGE
        sys.exit(1)

    if output_path:
        output = open(output_path, 'a+')
    else:
        output = sys.__stdout__

    ## Retrieve an instance of the collector plug-in.
    try:
        collector = getPluginInstance(collector, 'collectors')
    except ImportError:
        print 'Error: could not import "%s" plug-in. '\
            'Got the following exception:' % collector
        traceback.print_exc()
        sys.exit(1)

    ## Retrieve an instance of the action plug-in.
    try:
        action = getPluginInstance(action, 'actions')        
    except ImportError:
        print 'Error: could not import "%s" plug-in. '\
            'Got the following exception:' % action
        traceback.print_exc()
        sys.exit(1)

    ## Set logger for each plug-in.
    logger = Logger(output)
    collector.setLogger(logger)
    action.setLogger(logger)

    ## Do the job.
    start_time = time.time()
    logger.log("Started 'ximenez' session: '%s'." % ' '.join(sys.argv[1:]))
    collector.getInput(collector_input)
    sequence = collector.collect()
    logger.log('Collected %d items.' % len(sequence))
    action.getInput(action_input)
    action.execute(sequence)
    end_time = time.time()
    elapsed = end_time - start_time
    logger.log('Executed action in %d seconds.' % (elapsed))
    logger.endSection()

    if output_path:
        output.close()

if __name__ == "__main__":
    main()
