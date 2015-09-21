import pygame

from . import game
from . import loaders
from . import rect
from . import spellcheck


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


# These are methods (of the same name) on pygame.Rect
SYMBOLIC_POSITIONS = set((
    "topleft", "bottomleft", "topright", "bottomright",
    "midtop", "midleft", "midbottom", "midright",
    "center",
))

# Provides more meaningful default-arguments e.g. for display in IDEs etc.
POS_TOPLEFT = None
ANCHOR_CENTER = None


class Actor:
    EXPECTED_INIT_KWARGS = SYMBOLIC_POSITIONS
    DELEGATED_ATTRIBUTES = [
        "width", "height", "top", "left", "right", "bottom",
        "centerx", "centery", "topleft", "topright",
        "bottomleft", "bottomright", "midtop", "midleft", "midbottom", "midright",
        "center", "size"
    ]

    _anchor = _anchor_value = (0, 0)
    
    def __init__(self, image, pos=POS_TOPLEFT, anchor=ANCHOR_CENTER, **kwargs):
        self._handle_unexpected_kwargs(kwargs)

        self.__dict__["_rect"] = rect.ZRect((0, 0), (0, 0))
        # Initialise it at (0, 0) for size (0, 0). 
        # We'll move it to the right place and resize it later

        self._init_position(pos, anchor, **kwargs)
        self.image = image

    def __getattr__(self, attr):
        if attr in self.__class__.DELEGATED_ATTRIBUTES:
            return getattr(self._rect, attr)
        else:
            raise AttributeError
    
    def __setattr__(self, attr, value):
        if attr in self.__class__.DELEGATED_ATTRIBUTES:
            setattr(self._rect, attr, value)
        else:
            raise AttributeError

    def _handle_unexpected_kwargs(self, kwargs):
        unexpected_kwargs = set(kwargs.keys()) - self.EXPECTED_INIT_KWARGS
        if not unexpected_kwargs:
            return

        for found, suggested in spellcheck.compare(
                unexpected_kwargs, self.EXPECTED_INIT_KWARGS):
            raise TypeError(
                "Unexpected keyword argument '{}' (did you mean '{}'?)".format(
                    found, suggested))

    def _init_position(self, pos, anchor, **kwargs):
        if anchor is None:
            anchor = ("center", "center")
        self.anchor = anchor

        symbolic_pos_args = {
            k: kwargs[k] for k in kwargs if k in SYMBOLIC_POSITIONS}

        if not pos and not symbolic_pos_args:
            # No positional information given, use sensible top-left default
            self.topleft = (0, 0)
        elif pos and symbolic_pos_args:
            raise TypeError("'pos' argument cannot be mixed with 'topleft', 'topright' etc. argument.")
        elif pos:
            self.pos = pos
        else:
            self._set_symbolic_pos(symbolic_pos_args)

    def _set_symbolic_pos(self, symbolic_pos_dict):
        if len(symbolic_pos_dict) == 0:
            raise TypeError("No position-setting keyword arguments ('topleft', 'topright' etc) found.")
        if len(symbolic_pos_dict) > 1:
            raise TypeError("Only one 'topleft', 'topright' etc. argument is allowed.")

        setter_name, position = symbolic_pos_dict.popitem()
        setattr(self, setter_name, position)

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
