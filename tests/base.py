"""Base classes and utility classes and methods for Ximenez tests.

$Id$
"""

import os.path
import unittest
import logging
from logging import getLogger

## Monkey-patch input methods
from fakeinput import FakeInput
fake_input = FakeInput()
import ximenez.input
ximenez.input.xim_raw_input = fake_input
ximenez.input.xim_getpass = fake_input

## Monkey-patch logger
import fakelogger
fakelogger.patchLogging()

## Set logging settings(as it is set in the program itself)
from ximenez.xim import LOGGING_LEVEL
logging.basicConfig(level=LOGGING_LEVEL)


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

    def setPluginInput(self, plugin, *args, **kwargs):
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
