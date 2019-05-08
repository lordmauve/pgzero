import pygame
from math import radians, sin, cos, atan2, degrees, sqrt

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

MAX_ALPHA = 255  # Based on pygame's max alpha.


class BoundingBox:
    def __init__(self, width, height, anchor):
        self.width = width
        self.height = height
        self.anchor = anchor

    def set_angle(self, angle):
        """Rotate the box and calculate the new height, width and anchor."""
        theta = -radians(angle)
        w, h = self.width, self.height
        ax, ay = self.anchor

        sintheta = sin(theta)
        costheta = cos(theta)

        # Dims of the transformed rect
        tw = abs(w * costheta) + abs(h * sintheta)
        th = abs(w * sintheta) + abs(h * costheta)

        # Offset of the anchor from the center
        cax = ax - w * 0.5
        cay = ay - h * 0.5

        # Rotated offset of the anchor from the center
        rax = cax * costheta - cay * sintheta
        ray = cax * sintheta + cay * costheta

        # Update the bounding box
        self.width = tw
        self.height = th
        self.anchor = (
            tw * 0.5 + rax,
            th * 0.5 + ray
        )

    def set_dimensions(self, dimensions):
        w, h = dimensions
        ax, ay = self.anchor
        xscale = (1.0 * w) / self.width
        yscale = (1.0 * h) / self.height
        self.width = w
        self.height = h
        self.anchor = (ax * xscale, ay * yscale)

    def set_flip(self, xflip, yflip):
        ax, ay = self.anchor
        if xflip:
            ax = self.width - ax
        if yflip:
            ay = self.height - ay
        self.anchor = ax, ay


def _set_dimensions(actor, current_surface):
    if actor.dimensions == (actor._orig_width, actor._orig_height):
        return current_surface
    return pygame.transform.scale(current_surface, actor._dimensions)


def _set_flip(actor, current_surface):
    if not (actor._xflip or actor._yflip):
        return current_surface
    return pygame.transform.flip(current_surface, actor._xflip, actor._yflip)


def _set_angle(actor, current_surface):
    if actor._angle % 360 == 0:
        # No changes required for default angle.
        return current_surface
    return pygame.transform.rotate(current_surface, actor._angle)


def _set_opacity(actor, current_surface):
    alpha = int(actor.opacity * MAX_ALPHA + 0.5)  # +0.5 for rounding up.

    if alpha == MAX_ALPHA:
        # No changes required for fully opaque surfaces (corresponds to the
        # default opacity of the current_surface).
        return current_surface

    alpha_img = pygame.Surface(current_surface.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, alpha))
    alpha_img.blit(
        current_surface,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_MULT
    )
    return alpha_img


class Actor:
    EXPECTED_INIT_KWARGS = SYMBOLIC_POSITIONS
    DELEGATED_ATTRIBUTES = [
        a for a in dir(rect.ZRect) if not a.startswith("_")
    ]

    function_order = [_set_opacity, _set_dimensions, _set_flip, _set_angle]
    _anchor = _anchor_value = (0, 0)
    _angle = 0.0
    _opacity = 1.0
    _xflip = False
    _yflip = False

    def _build_transformed_surf(self):
        cache_len = len(self._surface_cache)
        if cache_len == 0:
            last = self._orig_surf
        else:
            last = self._surface_cache[-1]
        for f in self.function_order[cache_len:]:
            new_surf = f(self, last)
            self._surface_cache.append(new_surf)
            last = new_surf
        return self._surface_cache[-1]

    def __init__(self, image, pos=POS_TOPLEFT, anchor=ANCHOR_CENTER, **kwargs):
        self._handle_unexpected_kwargs(kwargs)

        self._surface_cache = []

        # Initialise rect at (0, 0) for size (0, 0).
        # We'll move it to the right place and resize it later
        self.__dict__["_rect"] = rect.ZRect((0, 0), (0, 0))

        self.image = image
        self._init_position(pos, anchor, **kwargs)

    def __getattr__(self, attr):
        if attr in self.__class__.DELEGATED_ATTRIBUTES:
            return getattr(self._rect, attr)
        else:
            return object.__getattribute__(self, attr)

    def __setattr__(self, attr, value):
        """Assign rect attributes to the underlying rect."""
        if attr in self.__class__.DELEGATED_ATTRIBUTES:
            return setattr(self._rect, attr, value)
        else:
            # Ensure data descriptors are set normally
            return object.__setattr__(self, attr, value)

    def __iter__(self):
        return iter(self._rect)

    def __repr__(self):
        return '<{} {!r} pos={!r}>'.format(
            type(self).__name__,
            self._image_name,
            self.pos
        )

    def __dir__(self):
        standard_attributes = [
            key
            for key in self.__dict__.keys()
            if not key.startswith("_")
        ]
        return standard_attributes + self.__class__.DELEGATED_ATTRIBUTES

    def _handle_unexpected_kwargs(self, kwargs):
        unexpected_kwargs = set(kwargs.keys()) - self.EXPECTED_INIT_KWARGS
        if not unexpected_kwargs:
            return

        typos, _ = spellcheck.compare(
            unexpected_kwargs, self.EXPECTED_INIT_KWARGS)
        for found, suggested in typos:
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
            raise TypeError(
                "'pos' argument cannot be mixed with 'topleft', "
                "'topright' etc. argument."
            )
        elif pos:
            self.pos = pos
        else:
            self._set_symbolic_pos(symbolic_pos_args)

    def _set_symbolic_pos(self, symbolic_pos_dict):
        if len(symbolic_pos_dict) == 0:
            raise TypeError(
                "No position-setting keyword arguments ('topleft', "
                "'topright' etc) found."
            )
        if len(symbolic_pos_dict) > 1:
            raise TypeError(
                "Only one 'topleft', 'topright' etc. argument is allowed."
            )

        setter_name, position = symbolic_pos_dict.popitem()
        setattr(self, setter_name, position)

    def _update_transform(self, function):
        if function in self.function_order:
            i = self.function_order.index(function)
            del self._surface_cache[i:]
        else:
            raise IndexError(
                "function {!r} does not have a registered order."
                "".format(function))

    @property
    def anchor(self):
        return self._anchor_value

    @anchor.setter
    def anchor(self, val):
        self._anchor_value = val
        self._update_orig_anchor()
        self._update_box()

    def _update_orig_anchor(self):
        ax, ay = self._anchor_value
        ax = calculate_anchor(ax, 'x', self._orig_width)
        ay = calculate_anchor(ay, 'y', self._orig_height)
        self._orig_anchor = ax, ay

    def _update_box(self):
        b = BoundingBox(
                self._orig_width,
                self._orig_height,
                self._orig_anchor)
        # This order of operations must be preserved
        b.set_dimensions(self._dimensions)
        b.set_flip(self._xflip, self._yflip)
        b.set_angle(self._angle)

        # Copy the transformed height and width
        self.height = b.height
        self.width = b.width

        # Now move the topleft so that the anchor stays in position
        p = self.pos
        self._anchor = b.anchor
        self.pos = p

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle
        self._update_box()
        self._update_transform(_set_angle)

    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        self._dimensions = dimensions
        self._update_box()
        self._update_transform(_set_dimensions)

    @property
    def xflip(self):
        return self._xflip

    @xflip.setter
    def xflip(self, flipped):
        self._xflip = flipped
        self._update_box()
        self._update_transform(_set_flip)

    @property
    def yflip(self):
        return self._yflip

    @yflip.setter
    def yflip(self, flipped):
        self._yflip = flipped
        self._update_box()
        self._update_transform(_set_flip)

    def flip_x(self):
        self.xflip = not self.xflip

    def flip_y(self):
        self.yflip = not self.yflip

    @property
    def opacity(self):
        """Get/set the current opacity value.

        The allowable range for opacity is any number between and including
        0.0 and 1.0. Values outside of this will be clamped to the range.

        * 0.0 makes the image completely transparent (i.e. invisible).
        * 1.0 makes the image completely opaque (i.e. fully viewable).

        Values between 0.0 and 1.0 will give varying levels of transparency.
        """
        return self._opacity

    @opacity.setter
    def opacity(self, opacity):
        # Clamp the opacity to the allowable range.
        self._opacity = min(1.0, max(0.0, opacity))
        self._update_transform(_set_opacity)

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
        self._orig_surf = loaders.images.load(image)
        self._surface_cache.clear()  # Clear out old image's cache.
        self._update_orig()
        self._dimensions = self._orig_surf.get_size()
        self._update_box()

    def _update_orig(self):
        """Set original properties based on the image dimensions."""
        self._orig_width, self._orig_height = self._orig_surf.get_size()
        self._update_orig_anchor()

    def draw(self):
        s = self._build_transformed_surf()
        game.screen.blit(s, self.topleft)

    def angle_to(self, target):
        """Return the angle from this actors position to target, in degrees."""
        if isinstance(target, Actor):
            tx, ty = target.pos
        else:
            tx, ty = target
        myx, myy = self.pos
        dx = tx - myx
        dy = myy - ty   # y axis is inverted from mathematical y in Pygame
        return degrees(atan2(dy, dx))

    def distance_to(self, target):
        """Return the distance from this actor's pos to target, in pixels."""
        if isinstance(target, Actor):
            tx, ty = target.pos
        else:
            tx, ty = target
        myx, myy = self.pos
        dx = tx - myx
        dy = ty - myy
        return sqrt(dx * dx + dy * dy)

    def unload_image(self):
        loaders.images.unload(self._image_name)
