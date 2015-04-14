import pygame
pygame.init()


import os.path
import sys
from optparse import OptionParser
from types import ModuleType

from .game import PGZeroGame, DISPLAY_FLAGS
from . import loaders
from . import builtins


def main():
    parser = OptionParser()
    options, args = parser.parse_args()

    if len(args) != 1:
        parser.error("You must specify which module to run.")

    path = args[0]
    with open(path) as f:
        src = f.read()

    loaders.root = os.path.dirname(os.path.abspath(path))
    sys.modules['images'] = loaders.LoaderModule(loaders.images)
    sys.modules['sounds'] = loaders.LoaderModule(loaders.sounds)

    pygame.display.set_mode((100, 100), DISPLAY_FLAGS)
    name, _ = os.path.splitext(os.path.basename(path))
    mod = ModuleType(name)
    mod.__file__ = path
    mod.__name__ = name
    mod.__dict__.update(builtins.__dict__)
    sys.modules[name] = mod
    exec(src, mod.__dict__)
    PGZeroGame(mod).run()
