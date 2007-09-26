"""Define ``Action`` abstract class.

$Id$
"""

from ximenez.log import LoggerAware
from ximenez.input import InputAware


class Action(object, InputAware, LoggerAware):
    """The purpose of action plug-ins is to... do things.

    ``Action`` is an abstract class which real action plug-ins should
    subclass.
    """

    def execute(self, sequence):
        """Execute an action on ``sequence`` (whose type of items depends on
        the collector being used).

        This method **must** be implemented.
        """
        raise NotImplementedError
