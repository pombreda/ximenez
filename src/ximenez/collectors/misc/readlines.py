"""Define ``Readlines`` collector, which read lines from a file.

$Id$
"""

import os.path

from collectors.collector import Collector


def getInstance():
    """Return an instance of ReadLinesCollector."""
    return ReadLinesCollector()


class ReadLinesCollector(Collector):
    """A very simple collector which asks for the path of a file and
    returns a tuple containing each line of this file.
    """

    _input_info = ({'name': 'path',
                    'prompt': 'Path of the file: ',
                    'required': True
                    },
                   )


    def getInput(self, cl_input=None):
        """Get input from the user if what was provided in the command line
        (available in ``cl_input``) was not sufficient.

        If a value is given in the command line (``cl_input``), we
        suppose it is the path of the file.
        """
        if cl_input:
            self._input['path'] = cl_input
        else:
            ## Back to the default implementation
            Collector.getInput(self, cl_input)


    def collect(self):
        """Return lines of the file at ``path``, as a tuple."""
        path = self._input['path']
        lines = open(path, 'r').readlines()
        return [line.rstrip('\n\r') for line in lines]
