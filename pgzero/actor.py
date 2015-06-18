import pygame

from . import game
from . import loaders
from . import rect


ANCHORS = {
    'x': {
        'left': 0.0,
        'center': 0.5,
        'middle': 0.5,
        'right': 1.0,
    },
    'y': {
        'top': 0.0,
        'center': 0.5,
        'middle': 0.5,
        'bottom': 1.0,
    }
}


def calculate_anchor(value, dim, total):
    if isinstance(value, str):
        try:
            return total * ANCHORS[dim][value]
        except KeyError:
            raise ValueError(
                '%r is not a valid %s-anchor name' % (value, dim)
            )
    return float(value)


TOPLEFT = None  # symbolic name for the default positioning of the Actor


class Actor(rect.ZRect):
    _anchor = _anchor_value = (0, 0)

    def __init__(self, image, pos=TOPLEFT, anchor=('center', 'center')):
        self.image = image
        super(Actor, self).__init__(pos or (0, 0), self._surf.get_size())
        self.anchor = anchor
        if pos == TOPLEFT:
            self.topleft = 0, 0
        else:
            self.pos = pos

    @property
    def anchor(self):
        return self._anchor_value

    @anchor.setter
    def anchor(self, val):
        self._anchor_value = val
        self._calc_anchor()

    def _calc_anchor(self):
        ax, ay = self._anchor_value
        ax = calculate_anchor(ax, 'x', self.width)
        ay = calculate_anchor(ay, 'y', self.height)
        self._anchor = ax, ay

    @property
    def pos(self):
        px, py = self.topleft
        ax, ay = self._anchor
        return px + ax, py + ay

    @pos.setter
    def pos(self, pos):
        px, py = pos
        ax, ay = self._anchor
        self.topleft = px - ax, py - ay

    @property
    def x(self):
        ax = self._anchor[0]
        return self.left + ax

    @x.setter
    def x(self, px):
        self.left = px - self._anchor[0]

    @property
    def y(self):
        ay = self._anchor[1]
        return self.top + ay

    @y.setter
    def y(self, py):
        self.top = py - self._anchor[1]

    @property
    def image(self):
        return self._image_name

    @image.setter
    def image(self, image):
        self._image_name = image
        p = self.pos
        self._surf = loaders.images.load(image)
        self.width, self.height = self._surf.get_size()
        self._calc_anchor()
        self.pos = p

    def draw(self):
        game.screen.blit(self._surf, self.topleft)
