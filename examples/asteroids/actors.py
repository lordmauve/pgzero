import math
import random

from pygame.math import Vector2


class Player(Actor):
    def __init__(self, **kwargs):
        super(Player, self).__init__('player', **kwargs)
        self.thrust = False
        self.turn = 0
        self.speed = 0.2
        self.velocity = Vector2(0, 0)
        self.exact_pos = Vector2(self.center)
        self.frozen = False

    def fire(self):
        bullet = Actor('bullet', pos=self.pos)
        ang = math.radians(self.angle)
        bullet.exact_pos = bullet.start_pos = Vector2(self.pos)
        bullet.velocity = Vector2(math.sin(ang), math.cos(ang)).normalize() * 1000.0
        return bullet

    def move(self, dt, bounds):
        if self.turn:
            self.angle += self.turn * dt * 270

        if self.thrust:
            ang = math.radians(self.angle)
            self.velocity += math.sin(ang) * self.speed, math.cos(ang) * self.speed
        else:
            self.velocity *= 0.99
        self.exact_pos = self.exact_pos - self.velocity
        self.exact_pos.x %= bounds[0]
        self.exact_pos.y %= bounds[1]
        self.pos = self.exact_pos

    def destroy(self, spawn):
        self.pos = spawn
        self.angle = 0
        self.velocity = Vector2()
        self.invulnerable = True
        self.thrust = False
        self.exact_pos = self.pos


class Asteroid(Actor):
    INITIAL_MASS = 3
    ASTEROIDS = 3

    def __init__(self, bounds, mass=INITIAL_MASS, **kwargs):
        self.bounds = bounds
        self.mass = mass
        pos = (random.randint(0, bounds[0]), random.randint(0, bounds[1]))
        self.velocity = Vector2()
        self.velocity.from_polar((50, random.uniform(0, 360)))

        image = 'asteroid%s-%s' % (random.randint(1, self.ASTEROIDS), self.mass)
        super().__init__(image, pos=pos, **kwargs)
        self.exact_pos = Vector2(pos)

    def move(self, dt):
        self.exact_pos = self.exact_pos - (self.velocity * dt)
        self.exact_pos.x %= self.bounds[0]
        self.exact_pos.y %= self.bounds[1]
        self.pos = self.exact_pos

    def destroy(self):
        if self.mass > 1:
            return [self.chunk() for i in range(3)]
        return []

    def chunk(self):
        chunk = Asteroid(self.bounds, mass=self.mass - 1)
        chunk.pos = self.pos
        chunk.velocity = self.velocity.rotate(random.uniform(180, 360)) * 2
        chunk.exact_pos = Vector2(chunk.pos)
        return chunk
