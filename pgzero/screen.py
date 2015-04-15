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

    @property
    def _surf(self):
        return self._screen.surface

    def line(self, start, end, color):
        """Draw a line from start to end."""
        start = round_pos(start)
        end = round_pos(end)
        pygame.draw.line(self._surf, color, start, end, 1)

    def circle(self, pos, radius, color):
        """Draw a circle."""
        pos = round_pos(pos)
        pygame.draw.circle(self._surf, color, pos, radius, 1)

    def filled_circle(self, pos, radius, color):
        """Draw a filled circle."""
        pos = round_pos(pos)
        pygame.draw.circle(self._surf, color, pos, radius, 0)

    def rect(self, rect, color):
        """Draw a rectangle."""
        if not isinstance(rect, pygame.Rect):
            raise TypeError("screen.draw.rect() requires a rect to draw")
        pygame.draw.rect(self._surf, color, rect, 1)

    def filled_rect(self, rect, color):
        """Draw a filled rectangle."""
        if not isinstance(rect, pygame.Rect):
            raise TypeError("screen.draw.filled_rect() requires a rect to draw")
        pygame.draw.rect(self._surf, color, rect, 0)


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
