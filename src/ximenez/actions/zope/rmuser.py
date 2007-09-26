"""Define ``ZopeUserRemover``, a plug-in which connects to Zope
instances via XML-RPC and tries to remove an user.

$Id$
"""

from ximenez.actions.action import Action
from ximenez.shared.zope import ZopeInstance


def getInstance():
    """Return an instance of ZopeUserRemover."""
    return ZopeUserRemover()


class ZopeUserRemover(Action):
    """An action which removes an user from a collection of Zope
    instances, via XML-RPC.
    """

    _input_info = ()

    def getInput(self, cl_input=None):
        """Get input from the user."""
        if cl_input:
            ## Default handling of command line input.
            Action.getInput(self, cl_input)
            return

        ask = self.askForInput
        self._input.update(ask(({'name': 'userid',
                                 'prompt': 'User id to remove: ',
                                 'required': True
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
        """Change the password of an user on each item of ``instances``.

        ``instances`` is supposed to be a sequence of ``ZopeInstance``
        instances or ``<host>:<port>`` strings.
        """
        manager = self._input['manager']
        manager_pwd = self._input['manager_pwd']
        userid = self._input['userid']

        for instance in instances:
            if not isinstance(instance, ZopeInstance):
                host, port = instance.split(":")
                instance = ZopeInstance(host, port)
            try:
                instance.removeUser(userid, manager, manager_pwd)
                self.log('Removed "%s" from "%s".' % (userid,
                                                      instance))
            except:
                msg = 'ERROR: Could not remove "%s" from "%s" '\
                    'because of an unexpected exception. '% (userid,
                                                             instance)
                self.log(msg)
                self.logLastTraceback()
            self.endLogSection()
