.. --*- coding: utf-8 -*-

Ximenez : a multi-purpose action performer
==========================================

The purpose of Ximenez is to execute an action on a set of collected
items. Both the action and the way items are collected, are defined by
Python modules, which are called plug-ins. Its three FIXME... among
its FIXME are:

- execute a command (and retrieve its output) on a set of remote hosts
  (via SSH);

- perform various actions on a set of Zope servers (add an user,
  change his/her password, remove an user, etc.);

- any action that you are willing to write a Python plug-in for.

See the `Plugins`_ section below to know more about Ximenez built-in
plug-ins and how to develop your own ones.


Usage
-----

You can use Ximenez with the following command-line::

    ximenez -c <collector> -a <action>

``<collector>`` and ``<action>`` are both plug-ins. The former gives
Ximenez a set of items on which to act, and the latter is the action
to perform on each item of this set.

Hopefully, Ximenez comes with a number of useful plug-ins , e.g.::

    ximenez -c readlines -a print

Optional arguments are available. See ``usage.txt`` for further details.


Plug-ins
--------

The main characteristic of Ximenez is that it can be extended to just
do what you need to do, by using plug-ins. There are two kinds of
plug-ins: collectors and actions.

Ximenez ships with a set of built-in plug-ins.


Collectors
..........

Built-in collectors are:

``misc.readlines``
  Collect values from a file (the values are the content of each
  line).

``ssh.readlines``
  Collect a set of remote hosts from a file. Each line of the file
  should be of the form ``<host>[:<ssh-port>]``).

``zope.readlines``
  Collect a set of Zope instances from a file. Each line of the file
  should be of the form ``<host>[:<http-port>]``).

``zope.instances``
  Collect a set of Zope servers from an user's input.


Actions
.......

``misc.print``
  Logs (prints) each collected item. It can be quite useful when you
  are debugging a collector.

``ssh.remoteaction``
  Execute a command on the collected set of remote hosts (via SSH) and
  return its output.

``zope.adduser``
  Add a new user in the collected set of Zope instances.

``zope.chpwduser``
  Change password of an user in the collected set of Zope instances.

``zope.rmuser``
  Remove an user in the collected set of Zope instances.



Developing your own plug-ins
............................

An exhaustive guide to develop your own plug-ins can be found in
``plugins.txt``.


Requirements
------------

Ximenez should run under any OS, though some plug-ins may use
OS-specific features or require special Python packages.

Python 2.3 or above is required. This program may also work with prior
versions of Python, though it has not been tested.


Installation
------------

FIXME:

- python setup.py install

- easy_install [egg URL]


Credits
-------

Ximenez has been written by Damien Baty.

Gaël Le Mignot (Pilot Systems) and Sylvain Viollon (Infrae) have
provided several bug fixes.

`Pilot Systems`_ has partially sponsored the development of this
program.

.. _Pilot Systems: http://www.pilotsystems.net


Licence
-------

Ximenez is copyright 2008 by Damien Baty.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see the `section about licenses`_ of
the `GNU web site`_.

.. _section about licenses: http://www.gnu.org/licenses
.. _GNU web site: http://www.gnu.org
