"""Rect

This is a trivial Python wrapper around the pygame Rect
implementation so that arbitrary attributes can be added
to it

"""
import pygame

class Rect(pygame.rect.Rect):
    
    def __init__(self, *args, **kwargs):
        super(Rect, self).__init__(*args, **kwargs)
