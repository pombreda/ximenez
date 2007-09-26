"""Define various classes and functions related to SSH.

$Id$
"""

from popen2 import popen3


DEFAULT_PORT = '22'

class SSHRemoteHost(object):
    """A class which represents an SSH remote host."""
    def __init__(self, host, port=None, user=None):
        self.host = host
        self.port = port or DEFAULT_PORT
        self.user = user


    def __repr__(self):
        representation = ':'.join((self.host, self.port))
        if self.user:
            representation = '%s@%s' % (self.user, representation)
        return representation


    ## FIXME: is this really useful?
    def setUser(self, user):
        """Set user for a future connection."""
        self.user = user


    def execute(self, command):
        """Execute ``command`` on the remote host via SSH and returns
        the output.

        This method takes care of escaping ``command`` if needed.
        """
        host = self.host
        if self.user:
            host = '%s@%s' % (self.user, host)
        command = escapeShellCommand(command)
        cmd = 'ssh -p %s %s %s' % (self.port, host, command)
        stdout, stdin, stderr = popen3(cmd)
        output = stdout.read() + stderr.read()
        output = output.strip()
        return output


def escapeShellCommand(command,
                       special_chars=""";&|!><~*{}[]?()$\\`"""):
    """Escape special shell characters from ``command``.

    >>> f = escapeShellCommand
    >>> print f('ls')
    ls
    >>> print f('cd /var ; ls')
    cd /var \; ls
    >>> print f('cd && ls')
    cd \&\& ls
    >>> print f('cd || ls')
    cd \|\| ls
    >>> print f('ls &')
    ls \&
    >>> print f('ls | grep foo')
    ls \| grep foo
    >>> print f('echo Foo!')
    echo Foo\!
    >>> print f('echo !!')
    echo \!\!
    >>> print f('ls > foo')
    ls \\> foo
    >>> print f('ls < foo')
    ls \< foo
    >>> print f('ls ~')
    ls \~
    >>> print f('ls *')
    ls \*
    >>> print f('ls {foo,bar}.txt')
    ls \{foo,bar\}.txt
    >>> print f('ls [fb]oo')
    ls \[fb\]oo
    >>> print f('ls ?oo')
    ls \?oo
    >>> print f('(ls)')
    \(ls\)
    >>> print f('echo US$380')
    echo US\$380
    >>> print f('echo 1\\2')
    echo 1\2
    >>> print f('echo `foo`')
    echo \`foo\`

    The following code will test each command of the previous tests in
    a real use-case, with the 'echo' built-in/program.

    >>> from popen2 import popen3
    >>> docstring = escapeShellCommand.__doc__
    >>> lines = docstring.splitlines()
    >>> tests_ok = True
    >>> for i in range(3, len(lines), 2):
    ...     line = lines[i]
    ...     if not line: break
    ...     command = line[line.find("'") + 1:line.rfind("'")]
    ...     stdout, _, _ = popen3('echo %s' % escapeShellCommand(command))
    ...     tests_ok &= stdout.read().strip() == command
    >>> tests_ok
    True
    """
    ## This is probaly slower than using a regexp, but definitely more
    ## readable.
    escaped = ''
    for c in command:
        if c in special_chars:
            escaped += "\\"
        escaped += c
    return escaped


def _test():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    _test()
