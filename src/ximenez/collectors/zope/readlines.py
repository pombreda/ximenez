"""Define ZopeInstancesReadlinesCollector collector, which can
collect Zope instances that are listed in a file.

$Id$
"""

from ximenez.collectors.collector import Collector
from ximenez.shared.zope import ZopeInstance


def getInstance():
    """Return an instance of ZopeInstancesReadlinesCollector."""
    return ZopeInstancesReadlinesCollector()


class ZopeInstancesReadlinesCollector(Collector):
    """A collector which returns instances of Zope servers that are listed
    in a file.

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
        """Return a tuple of ``ZopeInstance`` objects."""
        lines = open(self._input['path']).readlines()
        instances = []
        for line in lines:
            host, port = line.split(':')
            port = port.strip()
            instances.append(ZopeInstance(host, port))
        return instances
