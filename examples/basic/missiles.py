import random
from collections import deque
from math import sin, floor
WIDTH = 800
HEIGHT = 400

GRAVITY = 5
TRAIL_LENGTH = 500
WIND_SCALE = 8
WIND_AMOUNT_X = 2.5
WIND_AMOUNT_Y = 1.5

TRAIL_BRIGHTNESS = 100
FLARE_COLOR = (255, 220, 160)

missiles = []


class Missile:
    def __init__(self, x, vx, y=0, vy=20):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.trail = deque(maxlen=TRAIL_LENGTH)
        self.t = random.uniform(0, 3)

    def step(self, dt):
        self.t += dt
        uy = self.vy
        self.vy += GRAVITY * dt
        self.y += 0.5 * (uy + self.vy) * dt

        self.x += self.vx * dt
        self.trail.appendleft((self.x, self.y))

        for i, (x, y) in enumerate(self.trail):
            nx = x + wind_x.get((x, y)) * dt
            ny = y + wind_y.get((x, y)) * dt
            self.trail[i] = nx, ny

        # If the trail is off the bottom of the screen, kill the missile
        if self.trail[-1][1] > HEIGHT:
            missiles.remove(self)
            return

    def draw(self):
        for i in range(len(self.trail)):
            if i + 1 == len(self.trail):
                break
            start = self.trail[i]
            end = self.trail[i + 1]
            c = TRAIL_BRIGHTNESS * (1.0 - i / TRAIL_LENGTH)
            color = (c, c, c)
            screen.draw.line(start, end, color)
        screen.draw.filled_circle((self.x, self.y), 2, FLARE_COLOR)

        # This small flickering lens flare makes it look like the
        # missile's exhaust is very bright.
        flare_length = 4 + sin(self.t) * 2 + sin(self.t * 5) * 1
        screen.draw.line(
            (self.x - flare_length, self.y),
            (self.x + flare_length, self.y),
            FLARE_COLOR
        )


class Perlin:
    def __init__(self, amount=1.0):
        self.seed = random.randrange(1000000)
        self.amount = amount

    def _rnd(self, i):
        n = 982451653
        d = 67867967
        return (self.seed + i) * n % d / d - 0.5

    def _get(self, p):
        n = int(floor(p / WIND_SCALE))
        frac = (p - n * WIND_SCALE) / WIND_SCALE
        left = self._rnd(n)
        right = self._rnd(n + 1)
        return frac * right + (1.0 - frac) * left

    def get(self, p):
        x, y = p
        return (self._get(x) - self._get(y + 1000000)) * self.amount


wind_x = Perlin(WIND_AMOUNT_X)
wind_y = Perlin(WIND_AMOUNT_Y)


def draw():
    screen.clear()
    for m in missiles:
        m.draw()


def update(dt):
    for m in list(missiles):
        m.step(dt)


def new_missile():
    m = Missile(x=random.randrange(600, 800), vx=random.uniform(-70, -10))
    missiles.append(m)


new_missile()
clock.schedule_interval(new_missile, 5)
