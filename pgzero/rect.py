# -*- coding: utf-8 -*-
import pygame.rect


class Rect(pygame.rect.Rect):
    __slots__ = ()

    # From Pygame docs
    VALID_ATTRIBUTES = """
        x y
        top  left  bottom  right
        topleft  bottomleft  topright  bottomright
        midtop  midleft  midbottom  midright
        center  centerx  centery
        size  width  height
        w h
    """.split()

    def __setattr__(self, key, value):
        try:
            pygame.rect.Rect.__setattr__(self, key, value)
        except AttributeError as e:
            from .spellcheck import suggest
            suggestions = suggest(key, self.VALID_ATTRIBUTES)
            msg = e.args[0]
            if suggestions:
                msg += "; did you mean {!r}?".format(suggestions[0])
            raise AttributeError(msg) from None

Rect.__doc__ = pygame.rect.Rect.__doc__


class NoIntersect(Exception):
    pass


class ZRect:
    """ZRect

    This is a Python implementation of the pygame Rect class. Its raison
    d'être is to allow the coordinates to be floating point. All pygame
    functions which require a rect allow for an object with a "rect"
    attribute and whose coordinates will be converted to integers implictly.

    All functions which require a dict will use the flexible constructor
    to convert from: this (or a subclass); a Pygame Rect; a 4-tuple or a
    pair of 2-tuples. In addition, they'll recognise any object which has
    an (optionally callable) .rect attribute whose value will be used instead.
    """

    _item_mapping = dict(enumerate("xywh"))

    def __init__(self, *args):

        if len(args) == 1:
            args = tuple(self._handle_one_arg(args[0]))

        #
        # At this point we have one of:
        #
        # x, y, w, h
        # (x, y), (w, h)
        # (x, y, w, h),
        #
        if len(args) == 4:
            self.x, self.y, self.w, self.h = args
        elif len(args) == 2:
            (self.x, self.y), (self.w, self.h) = args
        elif len(args) == 1:
            self.x, self.y, self.w, self.h = args[0]
        else:
            raise TypeError("%s should be called with one, two or four arguments" % (cls.__name__))

        self.rect = self

    def _handle_one_arg(self, arg):
        """Handle -- possibly recursively -- the case of one parameter

        Pygame -- and consequently pgzero -- is very accommodating when constructing
        a rect. You can pass four integers, two pairs of 2-tuples, or one 4-tuple.

        Also, you can pass an existing Rect-like object, or an object with a .rect
        attribute. The object named by the .rect attribute is either one of the above,
        or it's a callable object which returns one of the above.

        This is evidently a recursive solution where an object with a .rect
        attribute can yield an object with a .rect attribute, and so ad infinitum.
        """
        #
        # If the arg is an existing rect, return its elements
        #
        if isinstance(arg, RECT_CLASSES):
            return arg.x, arg.y, arg.w, arg.h

        #
        # If it's something with a .rect attribute, start again with
        # that attribute, calling it first if it's callable
        #
        if hasattr(arg, "rect"):
            rectobj = arg.rect
            if callable(rectobj):
                rectobj = rectobj()
            return self._handle_one_arg(rectobj)

        #
        # Otherwise, we assume it's an iterable of four elements
        #
        return arg

    def __repr__(self):
        return "<%s (x: %s, y: %s, w: %s, h: %s)>" % (self.__class__.__name__, self.x, self.y, self.w, self.h)

    def __reduce__(self):
        return self.__class__, (self.x, self.y, self.w, self.h)

    def copy(self):
        return self.__class__(self.x, self.y, self.w, self.h)
    __copy__ = copy

    def __len__(self):
        return 4

    def __getitem__(self, item):
        try:
            return getattr(self, self._item_mapping[item])
        except KeyError:
            raise IndexError

    def __setitem__(self, item, value):
        try:
            attribute = self._item_mapping[item]
        except KeyError:
            raise IndexError
        else:
            setattr(attribute, value)

    def __bool__(self):
        return self.w != 0 and self.h != 0

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.w
        yield self.h

    def __hash__(self):
        raise TypeError("ZRect instances may not be used as dictionary keys")

    def __eq__(self, *other):
        rect = self.__class__(*other)
        return (self.x, self.y, self.w, self.h) == (rect.x, rect.y, rect.w, rect.h)

    def __ne__(self, *other):
        rect = self.__class__(*other)
        return (self.x, self.y, self.w, self.h) != (rect.x, rect.y, rect.w, rect.h)

    def __lt__(self, *other):
        rect = self.__class__(*other)
        return (self.x, self.y, self.w, self.h) < (rect.x, rect.y, rect.w, rect.h)

    def __gt__(self, *other):
        rect = self.__class__(*other)
        return (self.x, self.y, self.w, self.h) > (rect.x, rect.y, rect.w, rect.h)

    def __le__(self, *other):
        rect = self.__class__(*other)
        return (self.x, self.y, self.w, self.h) <= (rect.x, rect.y, rect.w, rect.h)

    def __ge__(self, *other):
        rect = self.__class__(*other)
        return (self.x, self.y, self.w, self.h) >= (rect.x, rect.y, rect.w, rect.h)

    def __contains__(self, other):
        """Test whether a point (x, y) or another rectangle
        (anything accepted by ZRect) is contained within this ZRect
        """
        if len(other) == 2:
            return self.collidepoint(*other)
        else:
            return self.contains(*other)

    def _get_width(self):
        return self.w
    def _set_width(self, width):
        self.w = width
    width = property(_get_width, _set_width)

    def _get_height(self):
        return self.h
    def _set_height(self, height):
        self.h = height
    height = property(_get_height, _set_height)

    def _get_top(self):
        return self.y
    def _set_top(self, top):
        self.y = top
    top = property(_get_top, _set_top)

    def _get_left(self):
        return self.x
    def _set_left(self, left):
        self.x = left
    left = property(_get_left, _set_left)

    def _get_right(self):
        return self.x + self.w
    def _set_right(self, right):
        self.x = right - self.w
    right = property(_get_right, _set_right)

    def _get_bottom(self):
        return self.y + self.h
    def _set_bottom(self, bottom):
        self.y = bottom - self.h
    bottom = property(_get_bottom, _set_bottom)

    def _get_centerx(self):
        return self.x + (self.w / 2)
    def _set_centerx(self, centerx):
        self.x = centerx - (self.w / 2)
    centerx = property(_get_centerx, _set_centerx)

    def _get_centery(self):
        return self.y + (self.h / 2)
    def _set_centery(self, centery):
        self.y = centery - (self.h / 2)
    centery = property(_get_centery, _set_centery)

    def _get_topleft(self):
        return self.x, self.y
    def _set_topleft(self, topleft):
        self.x, self.y = topleft
    topleft = property(_get_topleft, _set_topleft)

    def _get_topright(self):
        return self.x + self.w, self.y
    def _set_topright(self, topright):
        x, y = topright
        self.x = x - self.w
        self.y = y
    topright = property(_get_topright, _set_topright)

    def _get_bottomleft(self):
        return self.x, self.y + self.h
    def _set_bottomleft(self, bottomleft):
        x, y = bottomleft
        self.x = x
        self.y = y - self.h
    bottomleft = property(_get_bottomleft, _set_bottomleft)

    def _get_bottomright(self):
        return self.x + self.w, self.y + self.h
    def _set_bottomright(self, bottomright):
        x, y = bottomright
        self.x = x - self.w
        self.y = y - self.h
    bottomright = property(_get_bottomright, _set_bottomright)

    def _get_midtop(self):
        return self.x + self.w / 2, self.y
    def _set_midtop(self, midtop):
        x, y = midtop
        self.x = x - self.w / 2
        self.y = y
    midtop = property(_get_midtop, _set_midtop)

    def _get_midleft(self):
        return self.x, self.y + self.h / 2
    def _set_midleft(self, midleft):
        x, y = midleft
        self.x = x
        self.y = y - self.h / 2
    midleft = property(_get_midleft, _set_midleft)

    def _get_midbottom(self):
        return self.x + self.w / 2, self.y + self.h
    def _set_midbottom(self, midbottom):
        x, y = midbottom
        self.x = x - self.w / 2
        self.y = y - self.h
    midbottom = property(_get_midbottom, _set_midbottom)

    def _get_midright(self):
        return self.x + self.w, self.y + self.h / 2
    def _set_midright(self, midright):
        x, y = midright
        self.x = x - self.w
        self.y = y - self.h / 2
    midright = property(_get_midright, _set_midright)

    def _get_center(self):
        return self.x + self.w / 2, self.y + self.h / 2
    def _set_center(self, center):
        x, y = center
        self.x = x - self.w / 2
        self.y = y - self.h / 2
    center = property(_get_center, _set_center)

    def _get_size(self):
        return self.w, self.h
    def _set_size(self, size):
        self.w, self.h = size
    size = property(_get_size, _set_size)

    def move(self, x, y):
        return self.__class__(self.x + x, self.y + y, self.w, self.h)

    def move_ip(self, x, y):
        self.x += x
        self.y += y

    def _inflated(self, x, y):
        return self.x - x / 2, self.y - y / 2, self.w + x, self.h + y

    def inflate(self, x, y):
        return self.__class__(*self._inflated(x, y))

    def inflate_ip(self, x, y):
        self.x, self.y, self.w, self.h = self._inflated(x, y)

    def _clamped(self, *other):
        rect = self.__class__(*other)

        if self.w >= rect.w:
            x = rect.x + rect.w / 2 - self.w / 2
        elif self.x < rect.x:
            x = rect.x
        elif self.x + self.w > rect.x + rect.w:
            x = rect.x + rect.w - self.w
        else:
            x = self.x

        if self.h >= rect.h:
            y = rect.y + rect.h / 2 - self.h / 2
        elif self.y < rect.y:
            y = rect.y
        elif self.y + self.h > rect.y + rect.h:
            y = rect.y + rect.h - self.h
        else:
            y = self.y

        return x, y

    def clamp(self, *other):
        rect = self.__class__(*other)
        x, y = self._clamped(rect)
        return self.__class__(x, y, self.w, self.h)

    def clamp_ip(self, *other):
        rect = self.__class__(*other)
        self.x, self.y = self._clamped(rect)

    def _clipped(self, *other):
        rect = self.__class__(*other)

        if self.x >= rect.x and self.x < (rect.x + rect.w):
            x = self.x
        elif rect.x >= self.x and rect.x < (self.x + self.w):
            x = rect.x
        else:
            raise NoIntersect

        if (self.x + self.w) > rect.x and (self.x + self.w) <= (rect.x + rect.w):
            w = self.x + self.w - x
        elif (rect.x + rect.w) > self.x and (rect.x + rect.w) <= (self.x + self.w):
            w = rect.x + rect.w - x
        else:
            raise NoIntersect

        if self.y >= rect.y and self.y < (rect.y + rect.h):
            y = self.y
        elif rect.y >= self.y and rect.y < (self.y + self.h):
            y = rect.y
        else:
            raise NoIntersect

        if (self.y + self.h) > rect.y and (self.y + self.h) <= (rect.y + rect.h):
            h = self.y + self.h - y
        elif (rect.y + rect.h) > self.y and (rect.y + rect.h) <= (self.y + self.h):
            h = rect.y + rect.h - y
        else:
            raise NoIntersect

        return x, y, w, h

    def clip(self, *other):
        rect = self.__class__(*other)
        try:
            x, y, w, h = self._clipped(rect)
        except NoIntersect:
            x, y, w, h = self.x, self.y, 0, 0
        return self.__class__(x, y, w, h)

    def clip_ip(self, *other):
        rect = self.__class__(*other)
        try:
            self.x, self.y, self.w, self.h = self._clipped(rect)
        except NoIntersect:
            self.x, self.y, self.w, self.h = self.x, self.y, 0, 0

    def _unioned(self, *other):
        rect = self.__class__(*other)
        x = min(self.x, rect.x)
        y = min(self.y, rect.y)
        w = max(self.x + self.w, rect.x + rect.w) - x
        h = max(self.y + self.h, rect.y + rect.h) - y
        return x, y, w, h

    def union(self, *other):
        rect = self.__class__(*other)
        return self.__class__(*self._unioned(rect))

    def union_ip(self, *other):
        rect = self.__class__(*other)
        self.x, self.y, self.w, self.h = self._unioned(rect)

    def _unionalled(self, others):
        allrects = [self] + [self.__class__(other) for other in others]
        x = min(r.x for r in allrects)
        y = min(r.y for r in allrects)
        w = max(r.x + r.w for r in allrects) - x
        h = max(r.y + r.h for r in allrects) - y
        return x, y, w, h

    def unionall(self, others):
        return self.__class__(*self._unionalled(others))

    def unionall_ip(self, others):
        self.x, self.y, self.w, self.h = self._unionalled(others)

    def fit(self, *other):
        rect = self.__class__(*other)
        ratio = max(self.w / rect.w, self.h / rect.h)
        w = self.w / ratio
        h = self.h / ratio
        x = rect.x + (rect.w - w) / 2
        y = rect.y + (rect.h - h) / 2
        return self.__class__(x, y, w, h)

    def normalize(self):
        if self.w < 0:
            self.x += self.w
            self.w = abs(self.w)
        if self.h < 0:
            self.y += self.h
            self.h = abs(self.h)

    def contains(self, *other):
        rect = self.__class__(*other)
        return (
            self.x <= rect.x and
            self.y <= rect.y and
            self.x + self.w >= rect.x + rect.w and
            self.y + self.h >= rect.y + rect.h and
            self.x + self.w > rect.x and
            self.y + self.h > rect.y
        )

    def collidepoint(self, *args):
        if len(args) == 1:
            x, y = args[0]
        else:
            x, y = args
        return (
            self.x <= x < (self.x + self.w) and
            self.y <= y < (self.y + self.h)
        )

    def colliderect(self, *other):
        rect = self.__class__(*other)
        return (
            self.x < rect.x + rect.w and
            self.y < rect.y + rect.h and
            self.x + self.w > rect.x and
            self.y + self.h > rect.y
        )

    def collidelist(self, others):
        for n, other in enumerate(others):
            if self.colliderect(other):
                return n
        else:
            return -1

    def collidelistall(self, others):
        return [n for n, other in enumerate(others) if self.colliderect(other)]

    def collidedict(self, dict, use_values=True):
        for k, v in dict.items():
            if self.colliderect(v if use_values else k):
                return k, v

    def collidedictall(self, dict, use_values=True):
        return [(k, v) for (k, v) in dict.items() if self.colliderect(v if use_values else k)]


RECT_CLASSES = (pygame.rect.Rect, ZRect)
