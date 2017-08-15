# -*- coding: utf-8 -*-

import errno
import subprocess
from rjsmin import jsmin

from jac.compat import file, u, utf8_encode
from jac.exceptions import InvalidCompressorError


class BabelCompressor(object):
    """Compressor for text/babel mimetype (see https://babeljs.io/docs/setup/#installation).

    Uses the babel command line program to generate JavaScript, then
    uses rjsmin for minification.

    TODO does babel have it's own minification?
    """

    binary = 'babel'

    """
    to fix error Couldn't find preset "xxxxx" relative to directory ...
    define here any path inside the folder containing "node_modules" with babel executable
    """
    cwd_for_presets_search = None
    presets = ['es2015', 'stage-0', 'react']
    extra_args = []

    @classmethod
    def compile(cls, what, mimetype='text/babel', cwd=None, uri_cwd=None,
                debug=None):
        args = ['--presets=' + ",".join(cls.presets)]

        if cls.extra_args:
            args.extend(cls.extra_args)

        args.insert(0, cls.binary)

        try:
            handler = subprocess.Popen(args, stdout=subprocess.PIPE,
                                       stdin=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       cwd=cls.cwd_for_presets_search)
        except OSError as e:
            msg = '{0} encountered an error when executing {1}: {2}'.format(
                cls.__name__,
                cls.binary,
                u(e),
            )
            if e.errno == errno.ENOENT:
                msg += ' Make sure {0} is in your PATH.'.format(cls.binary)
            raise InvalidCompressorError(msg)

        if isinstance(what, file):
            what = what.read()

        (stdout, stderr) = handler.communicate(input=utf8_encode(what))
        stdout = u(stdout)

        if not debug:
            stdout = jsmin(stdout)

        if handler.returncode == 0:
            return stdout
        else:
            raise RuntimeError('Test this :S %s' % stderr)
