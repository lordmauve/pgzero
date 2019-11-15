from . import storage
from . import clock
from . import loaders
from .game import PGZeroGame, DISPLAY_FLAGS
from types import ModuleType
import argparse
import warnings
import sys
import os
import pygame
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2)
pygame.init()


# The base URL for Pygame Zero documentation
DOCS_URL = 'http://pygame-zero.readthedocs.io/en/stable'


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

    parser = argparse.ArgumentParser()
    try:
        import ptpython  # noqa: checking if this is importable
    except ImportError:
        replhelp = argparse.SUPPRESS
        have_repl = False
    else:
        replhelp = "Show a REPL for interacting with the game while it is running."
        have_repl = True
    parser.add_argument(
        '--repl',
        action='store_true',
        help=replhelp
    )
    parser.add_argument(
        'script',
        help='The name of the Pygame Zero game to run'
    )
    args = parser.parse_args()
    if args.repl and not have_repl:
        sys.exit(
            "Error: Pygame Zero was not installed with REPL support.\n"
            "\n"
            "Please read\n"
            "{}/installation.html#install-repl\n"
            "for instructions on how to install this feature.".format(DOCS_URL)
        )

    if __debug__:
        warnings.simplefilter('default', DeprecationWarning)
    path = args.script
    load_and_run(path, repl=args.repl)


def load_and_run(path, repl=False):
    """Load and run the given Python file as the main PGZero game module.

    Note that the 'import pgzrun' IDE mode doesn't pass through this entry
    point, as the module is already loaded.

    """
    with open(path, 'rb') as f:
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

    pygame.display.init()
    try:
        run_mod(mod, repl=repl)
    finally:
        # Clean some of the state we created, useful in testing
        pygame.display.quit()
        clock.clock.clear()
        del sys.modules[name]


def prepare_mod(mod):
    """Prepare to execute the module code for Pygame Zero.

    To allow the module to load assets, we configure the loader path to
    load relative to the module's __file__ path.

    When executing the module some things need to already exist:

    * Our extra builtins need to be defined (by copying them into Python's
      `builtins` module)
    * A screen needs to be created (because we use convert_alpha() to convert
      Sprite surfaces for blitting to the screen).

    """
    storage.storage._set_filename_from_path(mod.__file__)
    loaders.set_root(mod.__file__)

    # An icon needs to exist before the window is created.
    PGZeroGame.show_default_icon()
    pygame.display.set_mode((100, 100), DISPLAY_FLAGS)

    # Copy pgzero builtins into system builtins
    from . import builtins as pgzero_builtins
    import builtins as python_builtins
    for k, v in vars(pgzero_builtins).items():
        python_builtins.__dict__.setdefault(k, v)


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
    try:
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
    finally:
        storage.Storage.save_all()
