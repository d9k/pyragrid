#!env python

__requires__ = 'pyramid'
import sys
import os
from pkg_resources import load_entry_point

print(sys.version)

# import pdb; pdb.set_trace()

if __name__ == '__main__':
    script_path = os.path.dirname(os.path.realpath(__file__))
    ini_path = os.path.join(script_path, 'development.ini')
    print("using config at \"{0}\"".format([ini_path]))

    print('ini_path:')
    print(ini_path)
    
    if (len(sys.argv) == 1):
        sys.argv.append(ini_path)
        sys.argv.append('--reload')

    print('sys.argv:')
    print(sys.argv)

    sys.exit(
        load_entry_point('pyramid', 'console_scripts', 'pserve')()
    )

