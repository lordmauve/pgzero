import pygame

from pgzero import game


class Actor(pygame.rect.Rect):
    def __init__(self, image, pos=(0, 0)):
        self.image = image
        super(Actor, self).__init__(pos, self.image.get_size())

    @property
    def pos(self):
        return self.topleft
    @pos.setter
    def pos(self, pos):
        self.topleft = pos

    @property
    def image(self):
        return self._image
    @image.setter
    def image(self, image):
        self._image = pygame.image.load(image)

    def draw(self):
        game.screen.blit(self.image, self.pos)
