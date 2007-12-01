"""Define various constants used in Zope-related test cases.

$Id$
"""

MANAGER = 'ximenez'
PASSWORD = 'ximenez'
## ``DOMAINS`` and ``ROLES`` are only used for non-PAS user folders
DOMAINS = ['localhost', '123.123.123.123']
ROLES = ['Manager']
DUMMY_USER = 'ximenez_dummy'
HOST = 'localhost'
PORTS_NO_PAS = (8081, )   ## Zope instances with standard user folders
PORTS_PAS = (8091, 8101)  ## Zope instances with PAS user folders
PORTS_NO_LISTEN = (111, ) ## Ports that no server listens on
