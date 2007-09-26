"""Define ``ZopePasswordModifier``, a plug-in which connects to Zope
instances via XML-RPC and tries to change the password of an user.

$Id$
"""

from ximenez.actions.action import Action
from ximenez.shared.zope import ZopeInstance


def getInstance():
    """Return an instance of ZopePasswordModifier."""
    return ZopePasswordModifier()


class ZopePasswordModifier(Action):
    """An action which changes the password of an user from a
    collection of Zope instances, via XML-RPC.
    """

    _input_info = ()

    def getInput(self, cl_input=None):
        """Get input from the user."""
        if cl_input:
            ## Default handling of command line input.
            Action.getInput(self, cl_input)
            return

        ask = self.askForInput
        self._input = {}
        self._input.update(ask(({'name': 'userid',
                                 'prompt': 'User id to change: ',
                                 'required': True
                                 },
                                {'name': 'password',
                                 'prompt': 'New password: ',
                                 'required': True,
                                 'hidden': True
                                 },)
                               ))

        self._input.update(ask(({'name': 'manager',
                                 'prompt': 'Manager username: ',
                                 'required': True
                                 },
                                {'name': 'manager_pwd',
                                 'prompt': 'Manager password: ',
                                 'required': True,
                                 'hidden': True
                                 },)
                               ))


    def execute(self, instances):
        """Change the password of an user on each item of
        ``instances``.

        ``instances`` is supposed to be a sequence of ``ZopeInstance``
        instances or ``<host>:<port>`` strings.
        """
        manager = self._input['manager']
        manager_pwd = self._input['manager_pwd']
        userid = self._input['userid']
        password = self._input['password']

        for instance in instances:
            if not isinstance(instance, ZopeInstance):
                host, port = instance.split(":")
                instance = ZopeInstance(host, port)
            try:
                instance.modifyUserPassword(userid, password,
                                            manager, manager_pwd)
                self.log('Changed password of "%s" in '\
                         '"%s".' % (userid, instance))
            except:
                self.log('ERROR: Could not change password of "%s" '\
                         'in "%s" because of an unexpected '\
                         'exception. '% (userid,
                                         instance))
                self.logLastTraceback()
            self.endLogSection()