"""Rect

This is a trivial Python wrapper around the pygame Rect
implementation so that arbitrary attributes can be added
to it

"""
import pygame

class NoIntersect(BaseException): pass

class Rect(object):

    _item_mapping = dict(enumerate("xywh"))
    
    def __init__(cls, *args):
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
        raise NotImplementedError
    
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
    
    #
    # TODO: set / get slice
    # TODO: coerce
    # TODO: comparison operator
    #

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
            x, y, w, h = self._clipped(rect)
        except NoIntersect:
            x, y, w, h = self.x, self.y, 0, 0
        self.x = self.x = x
        self.y = self.y = y
        self.w = self.w = w
        self.h = self.h = h

    def _unioned(self, other):
        x = min(self.x, other.x)
        y = min(self.y, other.y)
        w = max(self.w, other.w)
        h = max(self.h, other.h)
        return x, y, w, h

    def union(self, other):
        return self.__class__(*self._unioned(other))
    
    def union_ip(self, rect):
        self.x, self.y, self.w_, self.h = self._unioned(other)

    def _unionalled(self, rects):
        allrects = [self] + rects
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
            self.x <= other.x and self.y <= other.y and
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
        return self.x <= x < (self.x + self.w) and self.y <= y < (self.y + self.h)

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
