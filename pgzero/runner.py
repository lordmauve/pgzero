import pygame
pygame.init()


import os
import sys
import warnings
from optparse import OptionParser
from types import ModuleType

from .game import PGZeroGame, DISPLAY_FLAGS
from . import loaders
from . import builtins

import sys, os
os.environ


def main():
    print("sys.executable = {}".format(sys.executable))
    # if '.virtualenvs' in sys.executable: # TO-DO better test
    # Fix only for os 10

    if not 'Library/Frameworks' in sys.executable:
        print("***Changing the executable***")
        PYVER = '3.4'
        base_fw = '/Library/Frameworks/Python.framework/Versions/'
        real_python = base_fw + '{pv}/bin/python{pv}'.format(pv=PYVER)
        print(real_python)
        print(sys.argv)
        print(99)
        # old_python = '/Users/rcollin2/.virtualenvs/pgzero/bin/python'

        venv_paths = [p for p in sys.path
                      if p.startswith(os.environ['VIRTUAL_ENV'])]
        os.environ['PYTHONPATH'] = ':'.join(venv_paths + [
            os.environ['PYTHONPATH']])

        # from pkg_resources import load_entry_point
        # sys.exit(
        #     load_entry_point('pgzero==1.1rc1', 'console_scripts', 'pgzrun')()
        # )
        print('venv_paths')
        print(venv_paths)
        # os.execv(old_python, ['pgzrun'])  #sys.argv)
        # os.execv(real_python, ['python', '/Users/rcollin2/.virtualenvs/pgzero/bin/pgzrun'] + sys.argv[1:])  #sys.argv)
        os.execv(real_python, ['python', '-m', 'pgzero'] + sys.argv[1:])  #sys.argv)
        # os.execv(real_python, ['python', 'pgzrun'] + sys.argv[1:])  #sys.argv)
        assert 99 == 77
    # assert 5 == 6


    parser = OptionParser()
    options, args = parser.parse_args()

    if len(args) != 1:
        parser.error("You must specify which module to run.")

    if __debug__:
        warnings.simplefilter('default', DeprecationWarning)

    path = args[0]
    with open(path) as f:
        src = f.read()

    code = compile(src, os.path.basename(path), 'exec', dont_inherit=True)

    loaders.set_root(path)

    pygame.display.set_mode((100, 100), DISPLAY_FLAGS)
    name, _ = os.path.splitext(os.path.basename(path))
    mod = ModuleType(name)
    mod.__file__ = path
    mod.__name__ = name
    mod.__dict__.update(builtins.__dict__)
    sys.modules[name] = mod
    exec(code, mod.__dict__)
    PGZeroGame(mod).run()
