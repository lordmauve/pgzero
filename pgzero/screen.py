import pygame
import pygame.draw


def round_pos(pos):
    """Round a tuple position so it can be used for drawing."""
    x, y = pos
    return round(x), round(y)


class SurfacePainter:
    """Interface to pygame.draw that is bound to a surface."""

    def __init__(self, screen):
        self._screen = screen
        self.stroke = (128, 0, 0)
        self.stroke_width = 1
        self.fill = (255, 128, 128)

    @property
    def _surf(self):
        return self._screen.surface

    @property
    def draw_strokes(self):
        return bool(self.stroke and self.stroke_width)

    @property
    def fill_shapes(self):
        return bool(self.fill)

    def line(self, start, end):
        """Draw a line from start to end."""
        start = round_pos(start)
        end = round_pos(end)
        if self.draw_strokes:
            pygame.draw.line(self._surf, self.stroke, start, end, self.stroke_width)

    def circle(self, pos, radius):
        """Draw a circle."""
        pos = round_pos(pos)
        if self.fill_shapes:
            pygame.draw.circle(self._surf, self.fill, pos, radius, 0)
        if self.draw_strokes:
            pygame.draw.circle(self._surf, self.stroke, pos, radius, self.stroke_width)

    def rect(self, rect):
        """Draw a rectangle."""
        if not isinstance(rect, pygame.Rect):
            raise TypeError("screen.draw.rect() requires a rect to draw")
        if self.fill_shapes:
            pygame.draw.rect(self._surf, self.fill, rect, 0)
        if self.draw_strokes:
            pygame.draw.rect(self._surf, self.stroke, rect, self.stroke_width)


class Screen:
    """Interface to the screen."""
    def __init__(self, surface):
        self.surface = surface
        self.width, self.height = surface.get_size()

    def clear(self):
        """Clear the screen to black."""
        self.fill((0, 0, 0))

    def fill(self, color):
        """Fill the screen with a colour."""
        self.surface.fill(color)

    def blit(self, image, pos):
        """Draw a sprite onto the screen.

        "blit" is an archaic name for this operation, but one that is is still
        frequently used, for example in Pygame. See the `Wikipedia article`__
        for more about the etymology of the term.

        .. __: http://en.wikipedia.org/wiki/Bit_blit

        """
        self.surface.blit(image, pos)

    @property
    def draw(self):
        return SurfacePainter(self)
