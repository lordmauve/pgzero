"""Rect

This is a trivial Python wrapper around the pygame Rect
implementation so that arbitrary attributes can be added
to it

"""
import pygame

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

    def clamp(self, rect):
        raise NotImplementedError

    def clamp_ip(self, rect):
        raise NotImplementedError

    def clip(self, rect):
        raise NotImplementedError

    def union(self, rect):
        raise NotImplementedError
    
    def union_ip(self, rect):
        raise NotImplementedError
    
    def unionall(self, rects):
        raise NotImplementedError
    
    def unionall_ip(self, rects):
        raise NotImplementedError
    
    def fit(self, rect):
        raise NotImplementedError
    
    def normalise(self):
        raise NotImplementedError
    
    def contains(self):
        raise NotImplementedError
    
