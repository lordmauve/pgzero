import pygame
pygame.init()

import os.path
import sys
from optparse import OptionParser
from types import ModuleType

from .game import PGZeroGame
from .loaders import ImageLoaderModule, SoundLoaderModule
from . import builtins


def main():
    parser = OptionParser()
    options, args = parser.parse_args()

    if len(args) != 1:
        parser.error("You must specify which module to run.")

    path = args[0]
    with open(path) as f:
        src = f.read()

    root = os.path.dirname(os.path.abspath(path))
    sys.modules['images'] = ImageLoaderModule(os.path.join(root, 'images'))
    sys.modules['sounds'] = SoundLoaderModule(os.path.join(root, 'sounds'))

    name, _ = os.path.splitext(os.path.basename(path))
    mod = ModuleType(name)
    mod.__file__ = path
    mod.__name__ = name
    mod.__dict__.update(builtins.__dict__)
    sys.modules[name] = mod
    exec(src, mod.__dict__)
    PGZeroGame(mod).run()
