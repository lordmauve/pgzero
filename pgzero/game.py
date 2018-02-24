import sys
import operator
import time

import pygame
import pgzero.clock
import pgzero.keyboard
import pgzero.screen

from . import constants


screen = None
DISPLAY_FLAGS = 0


def exit():
    """Wait for up to a second for all sounds to play out
    and then exit
    """
    t0 = time.time()
    while pygame.mixer.get_busy():
        time.sleep(0.1)
        if time.time() - t0 > 1.0:
            break
    sys.exit()


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
            if icon is DEFAULTICON:
                self.show_default_icon()
            else:
                pygame.display.set_icon(pygame.image.load(icon))
            self.icon = icon

        w = getattr(mod, 'WIDTH', 800)
        h = getattr(mod, 'HEIGHT', 600)
        if w != self.width or h != self.height:
            self.screen = pygame.display.set_mode((w, h), DISPLAY_FLAGS)
            if hasattr(self.mod, 'screen'):
                self.mod.screen.surface = self.screen
            else:
                self.mod.screen = pgzero.screen.Screen(self.screen)
            screen = self.screen     # KILL ME
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

    def run(self):
        """Invoke the main loop, and then clean up."""
        try:
            self.mainloop()
        finally:
            pygame.display.quit()
            pygame.mixer.quit()

    def mainloop(self):
        """Run the main loop of Pygame Zero."""
        clock = pygame.time.Clock()
        self.reinit_screen()

        update = self.get_update_func()
        draw = self.get_draw_func()
        self.load_handlers()

        pgzclock = pgzero.clock.clock

        self.need_redraw = True
        while True:
            dt = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q and \
                            event.mod & (pygame.KMOD_CTRL | pygame.KMOD_META):
                        sys.exit(0)
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
