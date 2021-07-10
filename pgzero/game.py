import sys
import operator
import time
import asyncio

import pygame
import pgzero.clock
import pgzero.keyboard
import pgzero.screen
import pgzero.loaders
import pgzero.screen

from . import constants


screen = None  # This global surface is what actors draw to
DISPLAY_FLAGS = 0


def exit(exit_status=0):
    """Cleanly exits pgzero and pygame.

    Args:
        exit_status (int): Exit status. The default value of 0 indicates
            a successful termination.

    """
    sys.exit(exit_status)


def positional_parameters(handler):
    """Get the positional parameters of the given function."""
    code = handler.__code__
    return code.co_varnames[:code.co_argcount]


class DEFAULTICON:
    """Sentinel indicating that we want to use the default icon."""


class PGZeroGame:
    def __init__(self, mod):
        self.mod = mod
        self.screen = None
        self.width = None
        self.height = None
        self.title = None
        self.icon = None
        self.running = False
        self.keyboard = pgzero.keyboard.keyboard
        self.handlers = {}

    def reinit_screen(self):
        """Reinitialise the window.

        Return True if the dimensions of the screen changed.

        """
        global screen
        changed = False
        mod = self.mod

        icon = getattr(self.mod, 'ICON', DEFAULTICON)
        if icon and icon != self.icon:
            self.show_icon()

        w = getattr(mod, 'WIDTH', 800)
        h = getattr(mod, 'HEIGHT', 600)
        if w != self.width or h != self.height:
            self.screen = pygame.display.set_mode((w, h), DISPLAY_FLAGS)
            pgzero.screen.screen_instance._set_surface(self.screen)

            # Set the global screen that actors blit to
            screen = self.screen
            self.width = w
            self.height = h

        title = getattr(self.mod, 'TITLE', 'Pygame Zero Game')
        if title != self.title:
            pygame.display.set_caption(title)
            self.title = title

        return changed

    @staticmethod
    def show_default_icon():
        """Show a default icon loaded from Pygame Zero resources."""
        from io import BytesIO
        from pkgutil import get_data
        buf = BytesIO(get_data(__name__, 'data/icon.png'))
        pygame.display.set_icon(pygame.image.load(buf))

    def show_icon(self):
        icon = getattr(self.mod, 'ICON', DEFAULTICON)
        if icon is DEFAULTICON:
            self.show_default_icon()
        else:
            pygame.display.set_icon(pgzero.loaders.images.load(icon))
        self.icon = icon

    EVENT_HANDLERS = {
        pygame.MOUSEBUTTONDOWN: 'on_mouse_down',
        pygame.MOUSEBUTTONUP: 'on_mouse_up',
        pygame.MOUSEMOTION: 'on_mouse_move',
        pygame.KEYDOWN: 'on_key_down',
        pygame.KEYUP: 'on_key_up',
        constants.MUSIC_END: 'on_music_end'
    }

    def map_buttons(val):
        return {c for c, pressed in zip(constants.mouse, val) if pressed}

    EVENT_PARAM_MAPPERS = {
        'buttons': map_buttons,
        'button': constants.mouse,
        'key': constants.keys
    }

    def load_handlers(self):
        from .spellcheck import spellcheck
        spellcheck(vars(self.mod))
        self.handlers = {}
        for type, name in self.EVENT_HANDLERS.items():
            handler = getattr(self.mod, name, None)
            if callable(handler):
                self.handlers[type] = self.prepare_handler(handler)

    def prepare_handler(self, handler):
        """Adapt a pgzero game's raw handler function to take a Pygame Event.

        Returns a one-argument function of the form ``handler(event)``.
        This will ensure that the correct arguments are passed to the raw
        handler based on its argument spec.

        The wrapped handler will also map certain parameter values using
        callables from EVENT_PARAM_MAPPERS; this ensures that the value of
        'button' inside the handler is a real instance of constants.mouse,
        which means (among other things) that it will print as a symbolic value
        rather than a naive integer.

        """
        code = handler.__code__
        param_names = code.co_varnames[:code.co_argcount]

        def make_getter(mapper, getter):
            if mapper:
                return lambda event: mapper(getter(event))
            return getter

        param_handlers = []
        for name in param_names:
            getter = operator.attrgetter(name)
            mapper = self.EVENT_PARAM_MAPPERS.get(name)
            param_handlers.append((name, make_getter(mapper, getter)))

        def prep_args(event):
            return {name: get(event) for name, get in param_handlers}

        def new_handler(event):
            try:
                prepped = prep_args(event)
            except ValueError:
                # If we couldn't construct the keys/mouse objects representing
                # the button that was pressed, then skip the event handler.
                #
                # This happens because Pygame can generate key codes that it
                # does not have constants for.
                return
            else:
                return handler(**prepped)

        return new_handler

    def dispatch_event(self, event):
        handler = self.handlers.get(event.type)
        if handler:
            self.need_redraw = True
            handler(event)

    def get_update_func(self):
        """Get a one-argument update function.

        If the module defines a function matching ::

            update(dt)

        or ::

            update()

        then this will be called. Otherwise return a no-op function.

        """
        try:
            update = self.mod.update
        except AttributeError:
            return None
        else:
            if update.__code__.co_argcount == 0:
                return lambda dt: update()
            return update

    def get_draw_func(self):
        """Get a draw function.

        If no draw function is define, raise an exception.

        """
        try:
            draw = self.mod.draw
        except AttributeError:
            return lambda: None
        else:
            if draw.__code__.co_argcount != 0:
                raise TypeError(
                    "draw() must not take any arguments."
                )
            return draw

    def _call_users_on_enter_func(self):
        # Calls the user's on_enter function if defined.
        try:
            on_enter = self.mod.on_enter
        except AttributeError:
            # No func defined, so nothing to do.
            return

        if 0 != on_enter.__code__.co_argcount:
            # Put exception string on its own line for a cleaner traceback.
            raise TypeError(
                    'on_enter() must not take any arguments'
            )

        on_enter()

    def _call_users_on_exit_func(self, exit_status):
        # Calls the user's on_exit function if defined.
        # Supports calling functions with zero or one argument (exit_status).
        try:
            on_exit = self.mod.on_exit
        except AttributeError:
            # No func defined, so nothing to do.
            return

        if 0 == on_exit.__code__.co_argcount:
            on_exit()
        elif 1 == on_exit.__code__.co_argcount:
            on_exit(exit_status)
        else:
            # Put exception string on its own line for a cleaner traceback.
            raise TypeError(
                    'on_exit() can only take up to one argument'
            )

    def _on_exit(self, exit_status):
        # Exit clean up done here.
        # User's on_exit func is called right after exiting the game loop.
        self._call_users_on_exit_func(exit_status)

        # Wait (up to a second) for all sounds to play out.
        t0 = time.time()
        while pygame.mixer.get_busy():
            time.sleep(0.1)
            if time.time() - t0 > 1.0:
                break

        pygame.quit()  # Uninitialize any initialized pygame modules.

    def run(self):
        """Invoke the main loop, and then clean up."""
        loop = asyncio.SelectorEventLoop()
        try:
            loop.run_until_complete(self.run_as_coroutine())
        finally:
            loop.close()

    @asyncio.coroutine
    def run_as_coroutine(self):
        self.running = True
        exit_status = 0

        try:
            yield from self.mainloop()
        except SystemExit as e:
            exit_status = e.code
        finally:
            self._on_exit(exit_status)
            self.running = False

        # This needs to be outside the finally clause to allow all other
        # exceptions to be passed up.
        sys.exit(exit_status)

    @asyncio.coroutine
    def mainloop(self):
        """Run the main loop of Pygame Zero."""
        clock = pygame.time.Clock()
        self.reinit_screen()

        update = self.get_update_func()
        draw = self.get_draw_func()
        self.load_handlers()

        pgzclock = pgzero.clock.clock
        self.need_redraw = True

        # User's on_enter func is called right before entering the game loop.
        self._call_users_on_enter_func()

        while True:
            # TODO: Use asyncio.sleep() for frame delay if accurate enough
            yield from asyncio.sleep(0)
            dt = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_q and
                            event.mod & (pygame.KMOD_CTRL | pygame.KMOD_META)):
                        return
                    self.keyboard._press(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyboard._release(event.key)
                self.dispatch_event(event)

            pgzclock.tick(dt)

            if update:
                update(dt)

            screen_change = self.reinit_screen()
            if screen_change or update or pgzclock.fired or self.need_redraw:
                draw()
                pygame.display.flip()
                self.need_redraw = False
