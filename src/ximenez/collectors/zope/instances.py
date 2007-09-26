"""Define ZopeInstances collector, which can collect Zope instances.

$Id$
"""

from ximenez.collectors.collector import Collector
from ximenez.shared.zope import ZopeInstance


def getInstance():
    """Return an instance of ZopeInstancesCollector."""
    return ZopeInstancesCollector()


class ZopeInstancesCollector(Collector):
    """A collector which returns instances of Zope servers.

    It asks for the location of the host (which can be its IP or its
    name) and the port which it listens HTTP connections on.

    Returns a tuple of ``ZopeInstance`` instances.
    """

    _input_info = ({'name': 'host',
                    'prompt': 'Host: ',
                    'required': True},
                   {'name': 'port',
                    'prompt': 'HTTP port: ',
                    'required': True},
                   )
    _multiple_input = True


    def collect(self):
        """Return a tuple of ``ZopeInstance`` instances."""
        return [ZopeInstance(item['host'],
                             item['port']) for item in self._input]
