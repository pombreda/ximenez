"""Tests for ``ximenez.input`` module.

$Id$
"""

from base import XimenezTestCase


class InputTestCase(XimenezTestCase):
    pass ## FIXME


def test_suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InputTestCase))
    return suite


if __name__ == '__main__':
    import unittest
    unittest.main()
