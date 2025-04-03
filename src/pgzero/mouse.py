import pygame
import pygame.mouse
from collections import deque
from . import loaders


class Mouse:
    """Interface to the pygame mouse. Also integrates former
    enum properties of mouse to retain all previous functionality
    and be backwards compatible.
    """

    @property
    def LEFT(self):
        return 1

    @property
    def MIDDLE(self):
        return 2

    @property
    def RIGHT(self):
        return 3

    @property
    def WHEEL_UP(self):
        return 4

    @property
    def WHEEL_DOWN(self):
        return 5

    # TODO: Clean up the return value of this to make it easier
    # to understand for users.
    @property
    def pressed(self):
        return pygame.mouse.get_pressed()

    @property
    def pressed_left(self):
        return pygame.mouse.get_pressed()[0]

    @property
    def pressed_middle(self):
        return pygame.mouse.get_pressed()[1]

    @property
    def pressed_right(self):
        return pygame.mouse.get_pressed()[2]

    @property
    def pos(self):
        return pygame.mouse.get_pos()

    @pos.setter
    def pos(self, pos, pos_y=None):
        # Setting mouse visibility is a workaround to allow
        # setting the mouse position under Wayland, which
        # normally prevents user applications from doing this.
        # switch_back is necessary in case the pointer is
        # moved while already set invisible by the user.
        switch_back = True if self.visible else False
        pygame.mouse.set_visible(False)
        if pos_y:
            pygame.mouse.set_pos([pos, pos_y])
        # TODO: Nicer way to do this? Does it have to be so strict
        # in checking?
        elif isinstance(pos, (tuple, list)) and len(pos) == 2 and\
                isinstance(pos[0], int) and isinstance(pos[1], int):
            pygame.mouse.set_pos(pos)
        else:
            raise ValueError("Setting the mouse position requires either"
                             " one tuple with two integers or two integers"
                             " as individual parameters.")
        if switch_back:
            pygame.mouse.set_visible(True)

    @property
    def rel(self):
        return pygame.mouse.get_rel()

    @property
    def recent_rel(self):
        pass

    @property
    def visible(self):
        return pygame.mouse.get_visible()

    @visible.setter
    def visible(self, val):
        match val:
            case bool():
                vis = val
            case 0:
                vis = False
            case 1:
                vis = True
            case _:
                raise ValueError("Value to set mouse visibility must be"
                                 " a boolean or either 1 or 0.")
        pygame.mouse.set_visible(vis)

    @property
    def focused(self):
        return pygame.mouse.get_focused()

    # TODO: Better way to separate cursor, name and hotspot getting
    # without doubling up on the code? cursor could just call
    # name and hotspot, but then we would run pygames get_cursor()
    # twice. Neither is ideal.
    # Another option would be to expose an explicit getter function
    # and then turn it into a property the old fashioned way. This
    # works, but it rather ugly and terrible practise...
    @property
    def cursor(self):
        c = pygame.mouse.get_cursor()
        if c.type == "system":
            return c.__repr__().split("_")[-1][:-2], None
        elif c.type == "color":
            name = self._cursor_image_name
            if name and loaders.images._cache[name] == c.data[1]:
                return name, c.data[0]
            else:
                return "UNKNOWN", c.data[0]
        else:
            return "BITMAP", None

    @cursor.setter
    def cursor(self, args):
        # Separate arguments if both a cursor and hotspot were given.
        if isinstance(args, tuple) and len(args) > 1:
            c_string = args[0]
            hotspot = args[1]
        else:
            c_string = args
            hotspot = None
        system_cursors = ["ARROW", "IBEAM", "WAIT", "CROSSHAIR", "HAND"]
        if c_string in system_cursors:
            self._cursor_image_name = None
            exec("pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_"
                 + c_string + ")")
            if hotspot:
                print("WARNING: System cursors can't be given a hotspot"
                      " as they define their own. The given hotspo was"
                      " ignored.")
        else:
            if not hotspot:
                hotspot = (0, 0)
            surface = loaders.images.load(c_string)
            self._cursor_image_name = c_string
            pygame.mouse.set_cursor(hotspot, surface)

    @property
    def cursor_name(self):
        c = pygame.mouse.get_cursor()
        # As pygame doesn't have an exposed parameter to get
        # the kind of system cursor applied, we get it here
        # in a kind of dirty but consistent way.
        if c.type == "system":
            return c.__repr__().split("_")[-1][:-2]
        elif c.type == "color":
            name = self._cursor_image_name
            if name and loaders.images._cache[name] == c.data[1]:
                return name
            else:
                return "UNKNOWN"
        else:
            return "BITMAP"

    @property
    def cursor_hotspot(self):
        c = pygame.mouse.get_cursor()
        # For color cursors, the hotspot is easy to get.
        if c.type == "color":
            return c.data[0]
        # Pygame doesn't have a way to give us the hotspot
        # for system cursors and bitmap cursors aren't
        # supported for PGZero.
        else:
            return None


mouse_instance = Mouse()
