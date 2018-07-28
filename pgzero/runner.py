import pygame
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2)
pygame.init()


import os
import sys
import warnings
from optparse import OptionParser
from types import ModuleType

from .game import PGZeroGame, DISPLAY_FLAGS
from . import loaders
from . import builtins


def _check_python_ok_for_pygame():
    """If we're on a Mac, is this a full Framework python?

    There is a problem with PyGame on Macs running in a virtual env.
    If the Python used is from the venv, it will not allow full window and
    keyboard interaction. Instead, we need the original framework Python
    to get PyGame working properly.

    The problem doesn't occur on Linux and Windows.
    """
    if sys.platform == 'darwin':  # This is a Mac
        return 'Library/Frameworks' in sys.executable
    else:
        return True


def _substitute_full_framework_python():
    """Need to change the OS/X Python executable to the full Mac version,
    while maintaining the virtualenv environment, so things still run
    in an encapsulated way.

    We do this by extract the paths that virtualenv has added to the system
    path, and prefixing them to the current PYTHONPATH.

    Then we use os.execv() to start a replacement process that uses the
    same environment as the previous one.
    """
    PYVER = '{}.{}'.format(*sys.version_info[:2])
    base_fw = '/Library/Frameworks/Python.framework/Versions/'
    framework_python = base_fw + '{pv}/bin/python{pv}'.format(pv=PYVER)
    venv_base = os.environ.get('VIRTUAL_ENV')
    if not venv_base or not os.path.exists(framework_python):
        # Do nothing if virtual env hasn't been set up or if we can't
        # find the framework Python interpreter
        return
    venv_paths = [p for p in sys.path if p.startswith(venv_base)]
    # Need to allow for PYTHONPATH not already existing in environment
    os.environ['PYTHONPATH'] = ':'.join(venv_paths + [
        os.environ.get('PYTHONPATH', '')]).rstrip(':')
    # Pass command line args to the new process
    os.execv(framework_python, ['python', '-m', 'pgzero'] + sys.argv[1:])


def main():

    # Pygame won't run from a normal virtualenv copy of Python on a Mac
    if not _check_python_ok_for_pygame():
        _substitute_full_framework_python()

    parser = OptionParser()
    parser.add_option(
        '--repl',
        action='store_true',
        help="Show a REPL for interacting with the game while it is running."
    )
    options, args = parser.parse_args()

    if len(args) != 1:
        parser.error("You must specify which module to run.")

    if __debug__:
        warnings.simplefilter('default', DeprecationWarning)
    path = args[0]

    with open(path) as f:
        src = f.read()

    code = compile(src, os.path.basename(path), 'exec', dont_inherit=True)

    name, _ = os.path.splitext(os.path.basename(path))
    mod = ModuleType(name)
    mod.__file__ = path
    mod.__name__ = name
    sys.modules[name] = mod

    # Indicate that we're running with the pgzrun runner
    # This disables the 'import pgzrun' module
    sys._pgzrun = True

    prepare_mod(mod)
    exec(code, mod.__dict__)
    run_mod(mod, repl=options.repl)


def prepare_mod(mod):
    """Prepare a module to run as a Pygame Zero program.

    mod is a loaded module object.

    This sets up things like screen, loaders and builtins, which need to be
    set before the module globals are run.

    """
    loaders.set_root(mod.__file__)
    PGZeroGame.show_default_icon()
    pygame.display.set_mode((100, 100), DISPLAY_FLAGS)
    mod.__dict__.update(builtins.__dict__)


def configure_repl(repl):
    """Configure the ptpython REPL."""
    from . import __version__ as pgzero_version
    try:
        import pkg_resources
    except ImportError:
        ptpython_version = '???'
    else:
        try:
            dist = pkg_resources.working_set.require('ptpython')[0]
        except (pkg_resources.DistributionNotFound, IndexError):
            ptpython_version = '???'
        else:
            ptpython_version = dist.version

    print(
        'Pygame Zero {} REPL (ptpython {})'.format(
            pgzero_version, ptpython_version
        )
    )
    repl.show_status_bar = False
    repl.confirm_exit = False


def run_mod(mod, repl=False):
    """Run the module.

    If `repl` is True, also run a REPL to interact with the module.

    """
    game = PGZeroGame(mod)
    if repl:
        import asyncio
        from ptpython.repl import embed
        loop = asyncio.get_event_loop()

        # Make sure the game runs
        # NB. if the game exits, the REPL will keep running, which allows
        # inspecting final state
        game_task = loop.create_task(game.run_as_coroutine())

        # Wait for the REPL to exit
        loop.run_until_complete(embed(
            globals=vars(mod),
            return_asyncio_coroutine=True,
            patch_stdout=True,
            title="Pygame Zero REPL",
            configure=configure_repl,
        ))

        # Ask game loop to shut down (if it has not) and wait for it
        if game.running:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            loop.run_until_complete(game_task)
    else:
        game.run()
