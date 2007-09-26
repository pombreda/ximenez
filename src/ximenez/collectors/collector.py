"""Define ``Collector`` abstract class.

$Id$
"""

from ximenez.log import LoggerAware
from ximenez.input import InputAware


class Collector(object, InputAware, LoggerAware):
    """The purpose of a collector is to collect information.

    ``Collector`` is an abstract class which real collector plug-ins
    should subclass.
    """

    def collect(self):
        """Collect informations and return a tuple of items (the type
        of these items depends on the purpose of this collector).

        This method **must** be implemented.
        """
        raise NotImplementedError
