"""Ximenez test runner.

$Id$
"""

import os
import unittest


tests = [path[:-3] for path in os.listdir(os.curdir) \
         if path.startswith('test_') and path.endswith('.py')]

def test_suite():
    suite = unittest.TestSuite()
    for test in tests:
        module = __import__(test)
        if hasattr(module, 'test_suite'):
            suite.addTests(module.test_suite())
    return suite

if __name__ == '__main__': 
    ## FIXME: this is broken (an error is raised in 'unittest')
    unittest.main(defaultTest='test_suite')
