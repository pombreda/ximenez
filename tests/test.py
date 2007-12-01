"""Ximenez test runner.

$Id$
"""

import os
import doctest
import unittest


test_cases = [path[:-3] for path in os.listdir(os.curdir) \
              if path.startswith('test_') and path.endswith('.py')]
doctests = ['fakeinput', 'fakelogger']


def test_suite():
    suite = unittest.TestSuite()
    for test in test_cases:
        module = __import__(test)
        if hasattr(module, 'test_suite'):
            suite.addTests(module.test_suite())
    for test in doctests:
        module = __import__(test)
        suite.addTest(doctest.DocTestSuite(module))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
