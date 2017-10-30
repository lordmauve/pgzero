"""Magic runner system for Pygame Zero.

By importing this module, the current program becomes a Pygame Zero program
even when run with the standard Python interpreter.

When run with Pgzrun, this is a no-op.

"""

import sys
import os
from pgzero.runner import prepare_mod, run_mod


mod = sys.modules['__main__']
if not getattr(sys, '_pgzrun', None):
    prepare_mod(mod)


def go():
    if not getattr(sys, '_pgzrun', None):
        run_mod(mod)
