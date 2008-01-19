"""Ximenez test runner.

$Id$
"""

import os
import doctest
import unittest


test_cases = [path[:-3] for path in os.listdir(os.curdir) \
              if path.startswith('test_') and path.endswith('.py')]
doctest_modules = ['fakeinput', 'fakelogger']
doctest_files = ['../doc/develop-plugins.txt']

def test_suite():
    suite = unittest.TestSuite()
    for test in test_cases:
        module = __import__(test)
        if hasattr(module, 'test_suite'):
            suite.addTests(module.test_suite())
    for test in doctest_modules:
        module = __import__(test)
        suite.addTest(doctest.DocTestSuite(module))
    for f in doctest_files:
        suite.addTest(doctest.DocFileSuite(f, module_relative=False))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
