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
