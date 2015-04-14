import pygame
import pgzero.clock
import pgzero.keyboard


screen = None


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
        self.reinit_screen()

    def reinit_screen(self):
        global screen
        mod = self.mod
        w = getattr(mod, 'WIDTH', 800)
        h = getattr(mod, 'HEIGHT', 600)
        if w != self.width or h != self.height:
            self.mod.screen = self.screen = pygame.display.set_mode((w, h))
            screen = self.screen     # KILL ME
            self.width = w
            self.height = h

        icon = getattr(mod, 'ICON', None)
        if icon and icon != self.icon:
            pygame.display.set_icon(pygame.image.load(icon))
            self.icon = icon

        title = getattr(self.mod, 'TITLE', 'Pygame Zero Game')
        if title != self.title:
            pygame.display.set_caption(title)
            self.title = title

    EVENT_HANDLERS = {
        pygame.MOUSEBUTTONDOWN: 'on_mouse_down',
        pygame.MOUSEBUTTONUP: 'on_mouse_up',
        pygame.MOUSEMOTION: 'on_mouse_move',
        pygame.KEYDOWN: 'on_key_down',
        pygame.KEYUP: 'on_key_up',
    }

    def load_handlers(self):
        self.handlers = {}
        for type, name in self.EVENT_HANDLERS.items():
            handler = getattr(self.mod, name, None)
            if callable(handler):
                self.handlers[type] = self.prepare_handler(handler)

    def prepare_handler(self, handler):
        code = handler.__code__
        param_names = code.co_varnames[:code.co_argcount]

        def prep_args(event):
            return {n: getattr(event, n) for n in param_names}
        return lambda event: handler(**prep_args(event))

    def dispatch_event(self, event):
        handler = self.handlers.get(event.type)
        if handler:
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
            return lambda dt: None
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
            raise AttributeError(
                "Your game module must define a function 'draw()'"
            )
        else:
            if draw.__code__.co_argcount != 0:
                raise TypeError(
                    "draw() must not take any arguments."
                )
            return draw

    def run(self):
        clock = pygame.time.Clock()
        update = self.get_update_func()
        draw = self.get_draw_func()
        self.load_handlers()
        while True:
            dt = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    self.keyboard[event.key] = True
                elif event.type == pygame.KEYUP:
                    self.keyboard[event.key] = False
                self.dispatch_event(event)

            pgzero.clock.tick(dt)
            update(dt)
            self.reinit_screen()
            draw()
            pygame.display.flip()
