import sys
import operator
import time
import types
from time import perf_counter, sleep

import pygame
import pgzero.clock
import pgzero.keyboard
import pgzero.screen
import pgzero.loaders
import pgzero.screen

from . import constants


screen = None  # This global surface is what actors draw to
DISPLAY_FLAGS = pygame.SHOWN


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
    """The core game loop for Pygame Zero.

    Dispatch events, call update functions, draw. Repeat.
    """

    def __init__(
        self,
        mod: types.ModuleType,
        fps: bool = False
    ):
        """Construct a game loop given the pgzero module mod.

        If fps is True, show a FPS count at the bottom left of the window.
        """
        self.mod = mod
        self.screen = None
        self.width = None
        self.height = None
        self.title = None
        self.icon = None
        self.fps = fps
        self.keyboard = pgzero.keyboard.keyboard
        self.handlers = {}

    def reinit_screen(self) -> bool:
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
            self.screen = pygame.display.set_mode(
                (w, h),
                DISPLAY_FLAGS,
                vsync=1
            )
            pgzero.screen.screen_instance._set_surface(self.screen)

            # Set the global screen that actors blit to
            screen = self.screen
            self.width = w
            self.height = h

            # Dimensions changed, request a redraw
            changed = True

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

    def inject_global_handlers(self):
        """Inject handlers provide by the Pygame Zero system.

        Some of these wrap user handlers so must be injected later.
        """
        self.handlers[pygame.QUIT] = lambda e: sys.exit(0)
        self.handlers[pygame.VIDEOEXPOSE] = lambda e: None

        user_key_down = self.handlers.get(pygame.KEYDOWN)
        user_key_up = self.handlers.get(pygame.KEYUP)

        def key_down(event):
            if event.key == pygame.K_q and \
                    event.mod & (pygame.KMOD_CTRL | pygame.KMOD_META):
                sys.exit(0)
            self.keyboard._press(event.key)
            if user_key_down:
                return user_key_down(event)

        def key_up(event):
            self.keyboard._release(event.key)
            if user_key_up:
                return user_key_up(event)

        self.handlers[pygame.KEYDOWN] = key_down
        self.handlers[pygame.KEYUP] = key_up

    def handle_events(self, dt, update) -> bool:
        """Handle all events for the current frame.

        Return True if an event was handled.
        """
        updated = False

        for event in pygame.event.get():
            handler = self.handlers.get(event.type)
            if handler:
                handler(event)
                updated = True

        clock = pgzero.clock.clock
        clock.tick(dt)
        updated |= clock.fired

        if update:
            update(dt)
            updated = True

        updated |= self.reinit_screen()
        return updated

    def mainloop(self):
        """Run the main loop of Pygame Zero."""
        self.reinit_screen()

        update = self.get_update_func()
        draw = self.get_draw_func()
        self.load_handlers()
        self.inject_global_handlers()

        logic_timer = Timer('logic', print=self.fps)
        draw_timer = Timer('draw', print=self.fps)
        for i, dt in enumerate(frames(60)):
            with logic_timer:
                updated = self.handle_events(dt, update)

            if updated:
                with draw_timer:
                    draw()

                if self.fps and i and i % 60 == 0:
                    ftime_ms = draw_timer.get_mean() + logic_timer.get_mean()
                    fps = 1000 / ftime_ms

                    print(f"fps: {fps:0.1f}  time per frame: {ftime_ms:0.1f}ms")
                pygame.display.flip()


def frames(fps=60):
    """Iterate over frames at the given fps, yielding time delta (in s)."""
    tgt = 1 / fps  # target frame time

    t = perf_counter()
    dt = tgt
    dts = []

    awake_lag = 0
    while True:
        yield dt
        nextt = perf_counter()
        dt = nextt - t
        if dt < tgt:
            sleep(tgt - dt - awake_lag)
            nextt = perf_counter()
            dt = nextt - t
        t = nextt
        dts.append(dt)
        if len(dts) > 60:
            mean = sum(dts) / len(dts)
            awake_lag = (mean - tgt) * 0.5
            dts.clear()


class Timer:
    """Context manager to time the game loop."""

    __slots__ = (
        'name',
        'total', 'count', 'worst',
        'start',
        'print',
    )

    def __init__(self, name, print=False):
        self.name = name
        self.total = 0
        self.count = 0
        self.worst = 0
        self.print = print

    def __enter__(self):
        self.start = perf_counter()

    def __exit__(self, *_):
        t = (perf_counter() - self.start) * 1e3
        self.count += 1
        self.total += t
        if t > self.worst:
            self.worst = t

    def get_mean(self) -> float:
        mean = self.total / self.count
        if self.print:
            print(
                f"{self.name} mean: {mean:0.1f}ms  "
                f"worst: {self.worst:0.1f}ms")
        self.worst = self.total = self.count = 0
        return mean
