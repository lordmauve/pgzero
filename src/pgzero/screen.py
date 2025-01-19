import numpy as np
import pygame
import pygame.draw

from . import ptext
from .rect import RECT_CLASSES, ZRect
from . import loaders


def round_pos(pos):
    """Round a tuple position so it can be used for drawing."""
    try:
        x, y = pos
    except TypeError:
        raise TypeError("Coordinate must be a tuple (not {!r})".format(pos)) from None
    try:
        return round(x), round(y)
    except TypeError:
        raise TypeError("Coordinate values must be numbers (not {!r})".format(pos)) from None # noqa


def make_color(arg):
    if isinstance(arg, tuple):
        return arg
    return tuple(pygame.Color(arg))


class SurfacePainter:
    """Interface to pygame.draw that is bound to a surface."""

    def __init__(self, screen):
        self._screen = screen

    @property
    def _surf(self):
        return self._screen.surface

    def line(self, start, end, color, width=1):
        """Draw a line from start to end."""
        start = round_pos(start)
        end = round_pos(end)
        pygame.draw.line(self._surf, make_color(color), start, end, width)

    def circle(self, pos, radius, color, width=1):
        """Draw a circle."""
        pos = round_pos(pos)
        pygame.draw.circle(self._surf, make_color(color), pos, radius, width)

    def filled_circle(self, pos, radius, color):
        """Draw a filled circle."""
        pos = round_pos(pos)
        pygame.draw.circle(self._surf, make_color(color), pos, radius, 0)

    def polygon(self, points, color):
        """Draw a polygon."""
        try:
            iter(points)
        except TypeError:
            raise TypeError("screen.draw.filled_polygon() requires an iterable of points to draw") from None # noqa
        points = [round_pos(point) for point in points]
        pygame.draw.polygon(self._surf, make_color(color), points, 1)

    def filled_polygon(self, points, color):
        """Draw a filled polygon."""
        try:
            iter(points)
        except TypeError:
            raise TypeError("screen.draw.filled_polygon() requires an iterable of points to draw") from None # noqa
        points = [round_pos(point) for point in points]
        pygame.draw.polygon(self._surf, make_color(color), points, 0)

    def rect(self, rect, color, width=1):
        """Draw a rectangle."""
        if not isinstance(rect, RECT_CLASSES):
            raise TypeError("screen.draw.rect() requires a rect to draw")

        if width <= 1:
            pygame.draw.rect(self._surf, make_color(color), rect, width)
            return

        c = make_color(color)

        hw = width / 2
        l, t, w, h = rect  # noqa: E741
        l1, l2 = round(l - hw), round(l + hw)
        r1, r2 = round(l + w - hw), round(l + w + hw)
        t1, t2 = round(t - hw), round(t + hw)
        b1, b2 = round(t + h - hw), round(t + h + hw)

        def r(x1, y1, x2, y2):
            r = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
            pygame.draw.rect(self._surf, c, r, 0)

        r(l1, t1, r2, t2)  # top inclusive
        r(l1, t2, l2, b1)  # left exclusive
        r(r1, t2, r2, b1)  # right exclusive
        r(l1, b1, r2, b2)  # bottom inclusive

    def filled_rect(self, rect, color):
        """Draw a filled rectangle."""
        if not isinstance(rect, RECT_CLASSES):
            raise TypeError("screen.draw.filled_rect() requires a rect to draw")
        pygame.draw.rect(self._surf, make_color(color), rect, 0)

    def text(self, *args, **kwargs):
        """Draw text to the screen."""
        # FIXME: expose ptext parameters, for autocompletion and autodoc
        ptext.draw(*args, surf=self._surf, **kwargs)

    def textbox(self, *args, **kwargs):
        """Draw text to the screen, wrapped to fit a box"""
        # FIXME: expose ptext parameters, for autocompletion and autodoc
        ptext.drawbox(*args, surf=self._surf, **kwargs)


class Screen:
    """Interface to the screen."""
    def _set_surface(self, surface):
        self.surface = surface
        self.width, self.height = surface.get_size()

    def bounds(self):
        """Return a Rect representing the bounds of the screen."""
        return ZRect((0, 0), (self.width, self.height))

    def clear(self):
        """Clear the screen to black."""
        self.fill((0, 0, 0))

    def fill(self, color, gcolor=None):
        """Fill the screen with a colour."""
        if gcolor:
            start = make_color(color)
            stop = make_color(gcolor)
            pixs = pygame.surfarray.pixels3d(self.surface)
            h = self.height

            gradient = np.dstack(
                [np.linspace(a, b, h) for a, b in zip(start, stop)][:3]
            )
            pixs[...] = gradient
        else:
            self.surface.fill(make_color(color))

    def blit(self, image, pos):
        """Draw a sprite onto the screen.

        "blit" is an archaic name for this operation, but one that is is still
        frequently used, for example in Pygame. See the `Wikipedia article`__
        for more about the etymology of the term.

        .. __: http://en.wikipedia.org/wiki/Bit_blit

        :param image: A Surface or the name of an image object to load.
        :param pos: The coordinates at which the top-left corner of the sprite
                    will be positioned. This may be given as a pair of
                    coordinates or as a Rect. If a Rect is given the sprite
                    will be drawn at ``rect.topleft``.

        """
        if isinstance(image, str):
            image = loaders.images.load(image)
        self.surface.blit(image, pos, None, pygame.BLEND_ALPHA_SDL2)

    @property
    def draw(self):
        return SurfacePainter(self)

    def __repr__(self):
        return "<Screen width={} height={}>".format(self.width, self.height)


screen_instance = Screen()
