# -*- coding: utf-8 -*-
"""Rect

This is a Python implementation of the pygame Rect class. Its raison
d'être is to allow the coordinates to be floating point without having
to implement that change into pygame itself. All pygame functions which
require a rect allow for an object with a "rect" attribute and whose
coordinates will be converted to integers implictly.
"""

class NoIntersect(Exception): 
    pass

class Rect:

    _item_mapping = dict(enumerate("xywh"))
    
    def __init__(self, *args):
        if len(args) == 4:
            left, top, width, height = args
        elif len(args) == 2:
            (left, top), (width, height) = args
        else:
            obj, = args
            obj = getattr(obj, "rect", obj)
            if callable(obj):
                obj = obj()

            left, top, width, height = obj.left, obj.top, obj.width, obj.height
            
        self.x = left
        self.y = top
        self.w = width
        self.h = height
        self.rect = self
    
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
        
    def __hash__(self):
        return hash(self.x, self.y, self.w, self.h)
    
    def __eq__(self, other):
        return self.x, self.y, self.w, self.h == other.x, other.y, other.w, other.h
    
    def __ne__(self, other):
        return self.x, self.y, self.w, self.h == other.x, other.y, other.w, other.h
    
    def __lt__(self, other):
        return self.x, self.y, self.w, self.h < other.x, other.y, other.w, other.h
    
    def __gt__(self, other):
        return self.x, self.y, self.w, self.h > other.x, other.y, other.w, other.h
    
    def __le__(self, other):
        return self.x, self.y, self.w, self.h <= other.x, other.y, other.w, other.h
    
    def __ge__(self, other):
        return self.x, self.y, self.w, self.h >= other.x, other.y, other.w, other.h
    
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
    def _set_centerx(self, centre):
        self.x = centre - (self.w / 2)
    centerx = property(_get_centerx, _set_centerx)
    centrex = centerx

    def _get_centery(self):
        return self.y + (self.h / 2)
    def _set_centery(self, centre):
        self.y = centre - (self.h / w)
    centery = property(_get_centery, _set_centery)
    centrey = centery
    
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
    centre = center
    
    def _get_size(self):
        return self.w, self.h
    def _set_size(self, size):
        self.w, self.h = size
    size = property(_get_size, set_size)
    
    def move(self, x, y):
        return self.__class__(self.x + x, self.y + y, self.w, self.h)
    
    def move_ip(self, x, y):
        self.x += x
        self.y += y
    
    def inflate(self, x, y):
        return self.__class__(self.x, self.y, self.w + x, self.h + y)
    
    def inflate_ip(self, x, y):
        self.w += x
        self.h += y

    def _clamped(self, rect):
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
    
    def clamp(self, rect):
        x, y = self._clamped(rect)    
        return self.__class__(x, y, self.w, self.h)

    def clamp_ip(self, rect):
        self.x, self.y = self._clamped(rect)

    def _clipped(self, other):
        if other.x <= self.x < (other.x + other.w):
            x = self.x
        elif self.x <= other.x < (self.x + self.w):
            x = other.x
        else:
            raise NoIntersect
        
        if other.x < (self.x + self.w) <= (other.x + other_w):
            w = self.x + self.w - x
        elif self.x <= other.x < (self.x + self.w):
            w = other.x + other.w - x
        else:
            raise NoIntersect
        
        if other.y <= self.y < (other.y + other.h):
            y = self.y
        elif self.y <= other.y < (self.y + self.h):
            y = other.y
        else:
            raise NoIntersect
        
        if other.y < (self.y + self.h) <= (other.y + other_w):
            h = self.y + self.h - y
        elif self.y <= other.y < (self.y + self.h):
            h = other.y + other.h - y
        else:
            raise NoIntersect
        
        return x, y, w, h

    def clip(self, rect):
        try:
            x, y, w, h = self._clipped(rect)
        except NoIntersect:
            x, y, w, h = self.x, self.y, 0, 0
        return self.__class__(x, y, w, h)

    def clip_ip(self, rect):
        try:
            self.x, self.y, self.w, self.h = self._clipped(rect)
        except NoIntersect:
            self.x, self.y, self.w, self.h = self.x, self.y, 0, 0

    def _unioned(self, other):
        x = min(self.x, other.x)
        y = min(self.y, other.y)
        w = max(self.w, other.w)
        h = max(self.h, other.h)
        return x, y, w, h

    def union(self, other):
        return self.__class__(*self._unioned(other))
    
    def union_ip(self, rect):
        self.x, self.y, self.w, self.h = self._unioned(other)

    def _unionalled(self, rects):
        allrects = [self] + list(rects)
        x = min(r.x for r in allrects)
        y = min(r.y for r in allrects)
        w = max(r.w for r in allrects)
        h = max(r.h for r in allrects)
        return x, y, w, h

    def unionall(self, rects):
        return self.__class__(*self._unionalled(rects))
    
    def unionall_ip(self, rects):
        self.x, self.y, self.w, self.h = self._unionalled(rects)
    
    def fit(self, other):
        ratio = max(self.w / other.w, self.h / other.h)
        w = self.w / ratio
        h = self.h / ratio
        x = other.x + (other.w - w) / 2
        y = other.y + (other.h - h) / 2
        return self.__class__(x, y, w, h)
    
    def normalize(self):
        if self.w < 0:
            self.x += self.w
            self.w = -self.w
        if self.h < 0:
            self.y += self.h
            self.h -= self.h
    
    def contains(self, other):
        return (
            self.x <= other.x and 
            self.y <= other.y and
            self.x + self.w >= other.x + other.w and
            self.y + self.h >= other.h + other.h and
            self.x + self.w > other.x and
            self.y + self.h > other.y
        )

    def collidepoint(self, *args):
        if len(args) == 1:
            x, y = args,
        else:
            x, y = args
        return (
            self.x <= x < (self.x + self.w) and 
            self.y <= y < (self.y + self.h)
        )

    def colliderect(self, other):
        return (
            self.x < other.x + other.w and
            self.y < other.y + other.h and
            self.x + self.w > other.x and
            self.y + self.h > other.y
        )

    def collidelist(self, others):
        for n, other in enumerate(others):
            if self.colliderect(other):
                return n
        else:
            return -1

    def collidelistall(self, others):
        return [n for n, other in enumerate(others) if self.colliderect(other)]

    def collidedict(self, dict, use_values=0):
        function = dict.values if use_values else dict.keys
        return self.collidelist(function())        
    
    def collidedictall(self, dict, use_values=0):
        function = dict.values if use_values else dict.keys
        return self.collidelistall(function())        
