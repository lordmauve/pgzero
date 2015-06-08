"""Rect

This is a trivial Python wrapper around the pygame Rect
implementation so that arbitrary attributes can be added
to it

"""
import pygame

class NoIntersect(BaseException): pass

class Rect(pygame.rect.Rect):

    def __new__(cls, *args):
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
        
        rect = super().__new__(cls, left, top, width, height)
        rect._x = left
        rect._y = top
        rect._w = width
        rect._h = height
        return rect
   
    def __repr__(self):
        return "<%s(%s, %s, %s, %s)>" % (self.__class__.__name__, self._x, self._y, self._w, self._h)
        
    def move(self, x, y):
        return self.__class__(self._x + x, self._y + y, self._w, self._h)
    
    def move_ip(self, x, y):
        self._x += x
        self._y += y
        self.x = self._x
        self.y = self._y
    
    def inflate(self, x, y):
        return self.__class__(self._x, self._y, self._w + x, self._h + y)
    
    def inflate_ip(self, x, y):
        self._w += x
        self._h += y
        self.w = self._w
        self.h = self._h

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
        self._x, self._y = self._clamped(rect)
        self.x = self._x
        self.y = self._y

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
            x, y, w, h = self._x, self._y, 0, 0
        return self.__class__(x, y, w, h)

    def clip_ip(self, rect):
        try:
            x, y, w, h = self._clipped(rect)
        except NoIntersect:
            x, y, w, h = self._x, self._y, 0, 0
        self.x = self._x = x
        self.y = self._y = y
        self.w = self._w = w
        self.h = self._h = h

    def unioned(self, other):
        x = min(self.x, other.x)
        y = min(self.y, other.y)
        w = max(self.w, other.w)
        h = max(self.h, other.h)
        return x, y, w, h

    def union(self, other):
        return self.__class__(*self.unioned(other))
    
    def union_ip(self, rect):
        x, y, w, h = self.unioned(other)
        self.x = x, self.y = y, self.w = w, self.h = h
    
    def unionall(self, rects):
        """ FIXME
        l, t, b, r = self.x, self.y, self.x + self.w, self.y + self.h
        l = min(r.x for r in [self] + rects)
        t = min(r.y for r in [self
        """
        raise NotImplementedError
    
    def unionall_ip(self, rects):
        raise NotImplementedError
    
    def fit(self, rect):
        raise NotImplementedError
    
    def normalise(self):
        raise NotImplementedError
    
    def contains(self):
        raise NotImplementedError
    
