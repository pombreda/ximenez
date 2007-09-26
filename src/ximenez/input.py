"""Define ``InputAware`` mixin.

$Id$
"""

try:
    import readline
except:
    pass ## No support for 'readline'.
    ## FIXME: auto-completion features will not work. We have to take
    ## care of this.
from getpass import getpass
from types import StringType


## FIXME: would be nice to better format text (e.g. print errors in
## bold red).
class InputAware:
    """Mixin class which defines input-related methods."""
    _input = {}
    _input_info = ()
    _multiple_input = False


    def getInput(self, cl_input=None):
        """Get input from the user or from the command line argument
        if ``cl_input`` is not empty.

        The default handling of ``cl_input`` supposes that it is
        composed by a ';;'-separated list of ``key=value``
        pairs. E.g.::

            path=file.txt;;userid=bob

        will result in the following ``_input`` mapping::

            {'path': 'file.txt',
             'userid': 'bob'}

        Errors are not catched and will therefore raise exceptions.
        """
        if cl_input:
            for pair in cl_input.split(';;'):
                key, value = pair.split('=')
                self._input[key] = value
        else:
            if self._multiple_input:
                self._input = self.askForMultipleInput()
            else:
                self._input = self.askForInput()


    def getInputInfo(self):
        """Return a tuple of mappings which describes information
        needed by the collector.

        The mappings looks like::

            {'name': <string>,
             'prompt': <string>,
             'required': <boolean>,
             'hidden': <boolean>,
             'validators': <sequence of strings or callables>,
            }

        where:

        - ``name`` is the name of the argument;

        - ``prompt`` is the string which will be displayed to the
          user;

        - ``required`` is an optional boolean which tells whether or
          not the user input is required. Default is ``False``;

        - ``hidden`` is an optional boolean which tells whether the
          user input has to be hidden (e.g. for a password). Default
          is ``False``;

        - validators is an optional sequence of validators. Each
          validator may be either a string (which should be method of
          the plug-in) or a callable (a function, a lambda expression,
          etc.)

        FIXME: we may want to add an optional key (``constraint``)
        which is a function (or a string that would be evaluated)
        which would be used to check the user input.

        FIXME: we could also have a 'vocabulary' key which would:
        - enforce the value to be in a restricted set of values
        - provide completion feature
        """
        return self._input_info


    def askForInput(self, input_info=None):
        """Ask user for input, based on the needed informations which
        are in ``input_info`` or returned by ``getInputInfo()`` if the
        former is ``None``.

        **WARNING:** this method does **not** store the user input in
        the object. It only returns it.
        """

        def _validate(validators, value):
            for validator in validators:
                error = False
                if type(validator) == StringType:
                    validate = getattr(self, validator, None)
                    if validate is None:
                        error = True
                    elif not validate(value):
                        return False
                elif callable(validator):
                    if not validator(value):
                        return False
                if error:
                    print 'Could not infer what to do with this '\
                        'validator: %s' % validator
                    sys.exit(1)
            return True

        if input_info is None:
            input_info = self.getInputInfo()
        input = {}
        for info in input_info:
            while 1:
                ask = raw_input
                if info.get('hidden'):
                    ask = getpass
                value = ask(info['prompt'])                    
                if value or not info.get('required'):
                    if _validate(info.get('validators', ()), value):
                        input[info['name']] = value
                        break
        return input


    def askForMultipleInput(self):
        """Ask user for more than one input, until (s)he presses
         ``^C``.
        """
        input = []
        while True:
            try:
                input.append(self.askForInput())
            except KeyboardInterrupt:
                break
        return input
