"""Monkey-patch ``raw_input`` and ``getpass.getpass`` so that they can
be tested against a predefined scenario.

Basic usage
===========

Suppose that we want to test this method::

    >>> from getpass import getpass
    >>> getpass = raw_input ## Only necessary for this doctest.
    >>> def askForUserIdAndPassword():
    ...     userid = raw_input('User id: ')
    ...     password = getpass('Password: ')
    ...     return userid, password

First, we define a sequence of what would be typed by the user. These
are lines::

    >>> raw_input.initializeLines(('jsmith', 'secret'))

Then call your method and check that it works as expected::

    >>> userid, password = askForUserIdAndPassword()
    >>> userid
    'jsmith'
    >>> password
    'secret'


Advanced usage
==============

Checking number of calls
------------------------

We can also test that our method does not ask more than it should::

    >>> def askForFirstname():
    ...     raw_input('Lastname') ## This is a bug that we would like to catch
    ...     return raw_input('Firstname')
    >>> raw_input.initializeLines(('Joe', ))
    >>> firstname, lastname = askForFirstname()
    ... #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    FakeInputNoMoreLineException

On the other hand, we would also like to test that our method does not
ask less that it should::

    >>> def getName():
    ...     return raw_input('Firstname')
    >>> raw_input.initializeLines(('Joe', 'Smith'))
    >>> getName() # doctest: +ELLIPSIS
    '...'
    >>> raw_input.hasFinished()
    False

This means that we expected our method to ask more than it had.


Dealing with exceptions
-----------------------

Suppose that we want our user to input a list of items. When (s)he has
finished typing, the user would typically press ``^C`` and our program
would catch this (as a ``KeyboardInterrupt`` exception):

    >>> def getItems():
    ...     items = []
    ...     while 1:
    ...         try:
    ...             items.append(raw_input('Item: '))
    ...         except KeyboardInterrupt:
    ...             break
    ...     return items

You can fake it, too:

    >>> raw_input.initializeLines(('first', 'second',
    ...                            KeyboardInterrupt))
    >>> getItems()
    ['first', 'second']


$Id$
"""


from types import StringType
try:
    BaseException
except NameError:
    ## ``BaseException`` did not exist before Python 2.5.
    BaseException = Exception


class FakeInputNoMoreLineException(Exception):
    """No more line."""


class FakeInput:
    """A class that can mimic ``raw_input()`` calls."""

    def initializeLines(self, lines):
        """Initialize lines."""
        self._lines = list(lines[:])
        self._lines.reverse()


    def resetLines(self):
        """Reset lines."""
        self._lines = []


    def hasFinished(self):
 	return len(self._lines) == 0


    def __call__(self, prompt=None):
        if not len(self._lines):
            raise FakeInputNoMoreLineException
        line = self._lines.pop()
        if type(line) != StringType:
            if issubclass(line, BaseException):
                raise line()
        return line


raw_input = FakeInput()
from getpass import getpass
getpass = raw_input


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
