"""Define ZopeUserAdder, a plug-in which connects to Zope instances
via XML-RPC and tries to create a Manager user.

$Id$
"""

from ximenez.actions.action import Action
from ximenez.shared.zope import ZopeInstance


def getInstance():
    """Return an instance of ZopeUserAdder."""
    return ZopeUserAdder()


class ZopeUserAdder(Action):
    """An action which removes an user from a collection of Zope
    instances, via XML-RPC."""

    _input_info = ()

    def getInput(self, cl_input=None):
        """Get input from the user."""
        if cl_input:
            ## Default handling of command line input.
            Action.getInput(self, cl_input)
            return

        ask = self.askForInput
        self._input.update(ask(({'name': 'userid',
                                 'prompt': 'User id to create: ',
                                 'required': True
                                 },
                                {'name': 'pwd',
                                 'prompt': 'Password of the new user: ',
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
        """Create an user on each item of ``instances``.

        ``instances`` is supposed to be a sequence of ``ZopeInstance``
        instances or ``<host>:<port>`` strings.
        """
        manager = self._input['manager']
        manager_pwd = self._input['manager_pwd']
        userid = self._input['userid']
        pwd = self._input['pwd']

        for instance in instances:
            if not isinstance(instance, ZopeInstance):
                host, port = instance.split(":")
                instance = ZopeInstance(host, port)
            try:
                instance.addUser(userid, pwd, manager, manager_pwd)
                self.log('Added "%s" to "%s".' % (userid,
                                                      instance))
            except:
                ## FIXME: this should work (and should be used):
                ##      self.log('mlklmk', userid, instance)
                msg = 'ERROR: Could not add "%s" to "%s" '\
                    'because of an unexpected exception. '% (userid,
                                                             instance)
                self.log(msg)
                self.logLastTraceback()
            self.endLogSection()
