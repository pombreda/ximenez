"""Define SSHRemoteHostsReadlinesCollector, which can collect SSH
remote hosts instances which are listed in a file.

$Id$
"""

from ximenez.collectors.collector import Collector
from ximenez.shared.ssh import SSHRemoteHost


def getInstance():
    """Return an instance of ``SSHRemoteHostsReadlinesCollector``."""
    return SSHRemoteHostsReadlinesCollector()


class SSHRemoteHostsReadlinesCollector(Collector):
    """A collector which returns instances of SSH remote hosts which
    are listed in a file.

    It asks for the pathname of the file, whose lines should have the
    following format::

        <host>[:<port>]

    ``<port>`` is optional. If not given, it is supposed to be the
    default SSH port (22).

    Returns a tuple of ``SSHRemoteHost`` instances.
    """

    _input_info = ({'name': 'path',
                    'prompt': 'File: ',
                    'required': True},
                   )
    _multiple_input = False


    def getInput(self, cl_input=None):
        """Get input from the user if what was provided in the command line
        (available in ``cl_input``) was not sufficient.

        If a value is given in the command line (``cl_input``), we
        suppose it is the path of the file.
        """
        if cl_input:
            self._input['path'] = cl_input
        else:
            ## Back to the default implementation
            Collector.getInput(self, cl_input)


    def collect(self):
        """Return a tuple of ``ZopeInstance`` instances."""
        lines = open(self._input['path']).readlines()
        instances = []
        for line in lines:
            if ':' not in line:
                host = line.strip()
                port = None
            else:
                host, port = line.split(':')
                port = port.strip()
            instances.append(SSHRemoteHost(host, port))
        return instances
