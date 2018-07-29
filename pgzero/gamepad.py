import pygame
from warnings import warn

class Gamepad:
    _pressed = set()

    def __init__(self):
        pygame.joystick.init() # main joystick device system
        try:
            self.pad0 = pygame.joystick.Joystick(0)
            self.pad0.init()
        except pygame.error:
            pass
        try:
            self.pad1 = pygame.joystick.Joystick(1)
            self.pad1.init()
        except pygame.error:
            pass


    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self._pressed.add(UP)
            elif event.key == pygame.K_d:
                self._pressed.add(RIGHT)
            elif event.key == pygame.K_s:
                self._pressed.add(DOWN)
            elif event.key == pygame.K_a:
                self._pressed.add(LEFT)
        if event.type == pygame.KEYUP:
           if event.key == pygame.K_w:
               self._pressed.discard(UP)
           elif event.key == pygame.K_d:
               self._pressed.discard(RIGHT)
           elif event.key == pygame.K_s:
               self._pressed.discard(DOWN)
           elif event.key == pygame.K_a:
               self._pressed.discard(LEFT)

    def map(self, val):
        return val

gamepad = Gamepad()

UP    = (0)
RIGHT = (1)
DOWN  = (2)
LEFT  = (3)
A     = (4)
B     = (5)