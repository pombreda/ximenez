"""Define various utility functions.

$Id$
"""

import imp
import os.path


def getPluginInstance(plugin, kind=None):
    """Retrieve a plug-in instance from ``plugin``.

    ``plugin`` may be:

    - the path (file path) to a Python module which defines a plug-in.

    - a (possibly dotted) module name from the set of built-in Ximenez
    plug-ins. In this case, ``kind`` must be either ``actions`` or
    ``collectors` (because these are the names of the related
    sub-packages in Ximenez).
    """
    if os.path.exists(plugin):
        module = imp.load_source('plugin', plugin)
    else:
        module_path = '.'.join(('ximenez', kind, plugin))
        module = __import__(module_path)
        for component in module_path.split('.')[1:]:
            module = getattr(module, component)

    return module.getInstance()
