## Copyright (c) 2007 Damien Baty
##
## This file is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation; either version 3 of the License,
## or (at your option) any later version.
##
## This file is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see
## <http://www.gnu.org/licenses/>.

"""Define ``FakeInput`` class which can be used to monkey-patch
``raw_input`` and ``getpass.getpass`` so that they can be tested
against a predefined scenario.

Basic usage
===========

Suppose that we want to test ``askForUserIdAndPassword`` defined
below::

    >>> def my_raw_input(prompt=None): raw_input(prompt)
    >>> from getpass import getpass
    >>> def my_getpass(prompt=None): getpass(prompt)
    >>>
    >>> def askForUserIdAndPassword():
    ...     userid = my_raw_input('User id: ')
    ...     password = my_getpass('Password: ')
    ...     return userid, password

We will first patch our input methods. Note that we cannot directly
patch ``raw_input``, because it is a Python built-in (that is why we
had to define a ``my_raw_input`` wrapper above)::

    >>> my_raw_input = FakeInput()
    >>> my_getpass = my_raw_input

Then we define a sequence of what would be typed by the user. These
are lines::

    >>> my_raw_input.initializeLines(('jsmith', 'secret'))

Then we call our method and check that it works as expected::

    >>> userid, password = askForUserIdAndPassword()
    >>> userid
    'jsmith'
    >>> password
    'secret'


Advanced usage
==============

Checking number of calls
------------------------

We can also test that our method does not ask more than it should. If
it does, our fake input method will raise an exception
(``FakeInputNoMoreLineException``)::

    >>> def askForFirstname():
    ...     my_raw_input('Lastname') ## This is a bug that we want to catch
    ...     return my_raw_input('Firstname')
    >>> my_raw_input.initializeLines(('Joe', ))
    >>> firstname, lastname = askForFirstname()
    ... #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    FakeInputNoMoreLineException

On the other hand, we would also like to test that our method does not
ask less that it should::

    >>> def getName():
    ...     return my_raw_input('Firstname')
    >>> my_raw_input.initializeLines(('Joe', 'Smith'))
    >>> getName() # doctest: +ELLIPSIS
    '...'
    >>> my_raw_input.hasFinished()
    False

This means that we expected our method to ask more than it had.


Dealing with exceptions
-----------------------

Suppose that we want our user to input a list of items. When (s)he has
finished typing, the user would typically press ``^C`` and our program
would catch this (as a ``KeyboardInterrupt`` exception)::

    >>> def getItems():
    ...     items = []
    ...     while 1:
    ...         try:
    ...             items.append(my_raw_input('Item: '))
    ...         except KeyboardInterrupt:
    ...             break
    ...     return items

We can fake it, too:

    >>> my_raw_input.initializeLines(('first', 'second',
    ...                                KeyboardInterrupt))
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
 	return len(getattr(self, '_lines')) == 0


    def __call__(self, prompt=None):
        if not len(getattr(self, '_lines', [])):
            raise FakeInputNoMoreLineException
        line = self._lines.pop()
        if type(line) != StringType:
            if issubclass(line, BaseException):
                raise line()
        return line


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
