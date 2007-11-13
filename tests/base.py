"""Base classes and utility method for Ximenez tests.

$Id$
"""

import os.path
import unittest

## Monkey-patch ``logging`` so that we can test what is logged.
if True:
    import logging
    from logging import Logger, getLogger
    from ximenez.xim import LOGGING_LEVEL

    logging.basicConfig(level=LOGGING_LEVEL)

    def _log(self, level, msg, args, exc_info=None):
        """My own log() method"""
        stack = self.getStack()
        stack.append(msg % args)
        ## FIXME: this is a bit basic, for now:
        ## - what if exc_info is True?
        ## - do we want to check log records level (severity)?

    def getStack(self):
        if not hasattr(self, '_stack'):
            clearStack(self)
        return self._stack

    def clearStack(self): self._stack = []

    Logger._log = _log
    Logger.getStack = getStack
    Logger.clearStack = clearStack


class XimenezTestCase(unittest.TestCase):
    """Base class for Ximenez tests."""

    def failUnlessLogEqual(self, expr):
        """Fail unless we have logged something equal to ``expr``."""
        self.failUnlessEqual(getLogger().getStack(), expr)


    def clearLog(self):
        """Clear log stack."""
        getLogger().clearStack()


class XimenezPluginTestCase(XimenezTestCase):
    """Base class for Ximenez plug-ins tests."""

    def setInput(self, plugin, *args, **kwargs):
        """Set input information (found in ``kwargs``) of
        ``plugin``.
        """
        if plugin._multiple_input:
            plugin._input = args
        else:
            plugin._input = kwargs


def getCompletePathOfTestFile(basename):
    """Return path of the given test file."""
    return os.path.join(os.path.dirname(__file__), 'data', basename)
