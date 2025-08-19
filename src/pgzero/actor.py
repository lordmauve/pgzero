import pygame
from math import radians, sin, cos, atan2, degrees, sqrt

from . import game
from . import loaders
from . import rect
from . import spellcheck
from .actor_animation import ActorAnimationSystem, ActorAnimation


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


def transform_anchor(ax, ay, w, h, angle):
    """Transform anchor based upon a rotation of a surface of size w x h."""
    theta = -radians(angle)

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

    return (
        tw * 0.5 + rax,
        th * 0.5 + ray
    )


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

    function_order = [_set_opacity, _set_angle]
    _anchor = _anchor_value = (0, 0)
    _angle = 0.0
    _opacity = 1.0
    _anim = ActorAnimationSystem() # Initialize any actor with a new animation system
    _a_image = None # Image variable to hold the currently displayed animation frame.
    # This image is separate from the static image so that falling back to it is 
    # possible if something goes wrong with the animations.

    def _build_transformed_surf(self):
        cache_len = len(self._surface_cache)
        if cache_len == 0:
            # If there is no cache and the actor is in an animation,
            # the last drawn surface is the animation image.
            if self._anim._current_animation:
                last = self._a_image
            # Otherwise, it's the static image.
            else:
                last = self._orig_surf
        # If there is a cache, it reflects the correct image either way.
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
        self.__dict__["_rect"] = rect.ZRect((0, 0), (0, 0))
        # Initialise it at (0, 0) for size (0, 0).
        # We'll move it to the right place and resize it later

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
        self._calc_anchor()

    def _calc_anchor(self):
        # Values are "left", "center", etc.
        ax, ay = self._anchor_value
        # If an animation is ongoing, the current
        # frame is used.
        if self._anim._current_animation:
            ow, oh = self._a_image.get_size()
        # Otherwise, the static image is used.
        else:
            ow, oh = self._orig_surf.get_size()
        #ow, oh = self._orig_surf.get_size()
        # calculate_anchor() returns the x and y coords
        # of the anchor in relation to the topleft of
        # the image. (e.g. if img. is 200x150 and anchor
        # is centered, ax and ay would be 100 and 75
        # after the operation)
        ax = calculate_anchor(ax, 'x', ow)
        ay = calculate_anchor(ay, 'y', oh)
        # If an animation is playing, change the anchor coordinates
        # based on animation frame offsets.
        if self._anim._current_animation:
            # Add the frame offsets to the relative pos of
            # anchor in relation to topleft.
            ax -= self._anim._current_animation.offset_x
            ay -= self._anim._current_animation.offset_y
        # The untransformed anchor assumes the image isn't 
        # rotated. If it is, the anchor position has to be
        # recalculated because the rotated image has a different
        # size and topleft, so the position of the anchor
        # in relation to topleft must also change.
        self._untransformed_anchor = ax, ay
        if self._angle == 0.0:
            self._anchor = self._untransformed_anchor
        else:
            self._anchor = transform_anchor(ax, ay, ow, oh, self._angle)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle
        if self._anim._current_animation:
            w, h = self._a_image.get_size()
        else:
            w, h = self._orig_surf.get_size()

        ra = radians(angle)
        sin_a = sin(ra)
        cos_a = cos(ra)
        self.height = abs(w * sin_a) + abs(h * cos_a)
        self.width = abs(w * cos_a) + abs(h * sin_a)
        ax, ay = self._untransformed_anchor
        p = self.pos
        self._anchor = transform_anchor(ax, ay, w, h, angle)
        self.pos = p
        self._update_transform(_set_angle)

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

    def rect(self):
        """Get a copy of the actor's rect object.

        This allows Actors to duck-type like rects in Pygame rect operations,
        and is not expected to be used in user code.
        """
        return self._rect.copy()

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
        self._update_pos()
        # Stop any running animation to show the static image instead.
        self._anim.stop()
        self._a_image = None

    # The instance of animation system should be able to be returned
    # but not be able to be set directly by the user.
    @property
    def anim(self):
        return self._anim

    def _update_pos(self):
        p = self.pos
        # TODO: Decide whether the actors base width should be
        #       changed with each animation frame or not.
        #if self._anim._current_animation:
        #    self.width, self.height = self._a_image.get_size()
        #else: 
        #    self.width, self.height = self._orig_surf.get_size()
        self.width, self.height = self._orig_surf.get_size()
        self._calc_anchor()
        self.pos = p

    def draw(self):
        # If an animation is running and it has advanced a frame, the 
        # actors new animation image needs to be fetched.
        # TODO: Solve this differently? An animation could directly 
        # change actor._a_image when it runs _next_frame, would that
        # be better?
        if self._anim._current_animation and self._anim._current_animation._new_frame:
            # Index of the right frame.
            i = self._anim._current_animation._frame_index
            # Setting the actors animation image to the right frame.
            self._a_image = self._anim._current_animation.frames[i]
            # Updating the animation status that the frame has been udpated.
            self._anim._current_animation.new_frame = False
            # Clear the surface cache for the new image.
            self._surface_cache.clear()
            """
            DEBUG PRINTS
            print("\nPos:", self.pos)
            print("Anchor:", self._anchor)
            print("Topleft:", self.topleft)
            print("Added:", self._anchor[0] + self.topleft[0], self._anchor[1] + self.topleft[1])
            print("Width:", self.width, "Height:", self.height)
            """
            # Update actor position to incorporate frame offsets.
            self._update_pos()
        # Otherwise, if no animation is running but there still is an 
        # animation image, it is deleted and the surface cache cleared
        # so that the static image is displayed again.
        elif not self._anim._current_animation and self._a_image and not self._anim.paused:
            self._a_image = None
            self._surface_cache.clear()
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

