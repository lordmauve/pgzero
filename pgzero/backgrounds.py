import random
import pygame.draw
import math

from .screen import round_pos
from . import clock


def random_pos(screen):
    x = random.randrange(0, screen.get_width())
    y = random.randrange(0, screen.get_height())
    return x, y


class WaterBackground:
    WATER_COLOR = (84, 164, 222)
    BUBBLE_COLOR = (187, 217, 238)

    def __init__(self, screen):
        self.bubbles = []
        self.screen = screen
        self.randomize_bubbles()
        clock.each_tick(self.update)

    def randomize_bubbles(self):
        del self.bubbles[:]
        for _ in range(10):
            self.spawn_bubble()

    def spawn_bubble(self, offscreen=False):
        radius = random.randrange(2, 10)
        x, y = random_pos(self.screen)
        if offscreen:
            y = self.screen.get_height() + 2 * radius

        phase = random.uniform(0, 6.283)
        self.bubbles.append((x, y, radius, phase))

    def update(self, dt):
        prev_bubbles = self.bubbles
        self.bubbles = []
        for i, [x, y, radius, phase] in enumerate(prev_bubbles):
            phase += dt
            y -= dt * 100
            x -= math.cos(phase)
            if y < -radius:
                self.spawn_bubble(offscreen=True)
            else:
                self.bubbles.append((x, y, radius, phase))

    def draw(self):
        self.screen.fill(self.WATER_COLOR)
        for x, y, radius, phase in self.bubbles:
            pos = round_pos((x, y))
            pygame.draw.circle(self.screen, self.BUBBLE_COLOR, pos, radius, 1)


class SpaceBackground:
    BLACK = 0, 0, 0

    def __init__(self, screen):
        self.screen = screen
        self.randomize_stars()
        clock.schedule_interval(self.update_stars, 0.1)

    def randomize_stars(self):
        self.stars = []
        for _ in range(30):
            x, y = random_pos(self.screen)
            color = self.rand_color()
            self.stars.append((x, y, color))

    def rand_color(self):
        return random.randrange(50, 256)

    def update_stars(self):
        for i, (x, y, c) in enumerate(self.stars):
            if random.randrange(0, 10) == 0:
                self.stars[i] = (x, y, self.rand_color())

    def draw(self):
        self.screen.lock()
        try:
            self.screen.fill(self.BLACK)
            for x, y, c in self.stars:
                self.screen.set_at((x, y), (c,) * 3)
        finally:
            self.screen.unlock()
