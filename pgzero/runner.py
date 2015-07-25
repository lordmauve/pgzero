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


def main():
    print(sys.executable)

    os.execv('')
    assert 5 == 6


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
