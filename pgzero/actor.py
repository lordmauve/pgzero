import pygame

from . import game
from . import loaders


class Actor(pygame.rect.Rect):
    def __init__(self, image, pos=(0, 0)):
        self.image = image
        super(Actor, self).__init__(pos, self._surf.get_size())

    @property
    def pos(self):
        return self.topleft

    @pos.setter
    def pos(self, pos):
        self.topleft = pos

    @property
    def image(self):
        return self._image_name

    @image.setter
    def image(self, image):
        self._image_name = image
        self._surf = loaders.images.load(image)

    def draw(self):
        game.screen.blit(self._surf, self.pos)
