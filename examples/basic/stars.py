import math
import random
from collections import deque

WIDTH = 1000
HEIGHT = 1000 * 9 // 16
ACCEL = 1.0  # Warp factor per second
DRAG = 0.71  # Fraction of speed per second
MIN_WARP_FACTOR = 0.1
BOUNDS = Rect(0, 0, WIDTH, HEIGHT)


warp_factor = MIN_WARP_FACTOR
centerx = WIDTH // 2
centery = HEIGHT // 2
stars = []


class Star:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.brightness = 10
        self.speed = math.hypot(*vel)
        self.prev_pos = deque(maxlen=3)
        self.prev_pos.append(self.pos)

    def set_pos(self, pos):
        self.pos = pos
        self.prev_pos.append(pos)


def draw():
    screen.clear()
    for star in stars:
        b = star.brightness
        color = (b, b, b)  # a grey
        screen.draw.line(star.prev_pos[0], star.pos, color)

    screen.draw.text(
        "Warp {:0.1f}".format(warp_factor),
        fontsize=40,
        midbottom=(WIDTH // 2, HEIGHT - 40),
        color=(180, 160, 0),
    )
    screen.draw.text(
        "Hold SPACE to accelerate",
        fontsize=30,
        midbottom=(WIDTH // 2, HEIGHT - 8),
        color=(90, 80, 0),
    )


def update(dt):
    global stars, warp_factor
    if keyboard.space:
        warp_factor += ACCEL * dt
    warp_factor = (
        MIN_WARP_FACTOR +
        (warp_factor - MIN_WARP_FACTOR) * DRAG ** dt
    )

    for _ in range(int(dt * 200)):
        angle = random.uniform(-math.pi, math.pi)
        dx = math.cos(angle)
        dy = math.sin(angle)
        speed = 255 * random.uniform(0.3, 1.0) ** 2

        d = random.uniform(0, 100)
        pos = centerx + dx * d, centery + dy * d

        v = speed * dx, speed * dy
        stars.append(Star(pos, v))

    for s in stars:
        x, y = s.pos
        vx, vy = s.vel

        x += vx * warp_factor * dt
        y += vy * warp_factor * dt
        s.set_pos((x, y))
        s.brightness = min(s.brightness + warp_factor * 200 * dt, s.speed)
        s.vel = vx * 2 ** dt, vy * 2 ** dt
    stars = [star for star in stars if BOUNDS.collidepoint(star.prev_pos[0])]


# Jump-start the star field
for _ in range(10):
    update(0.5)
for _ in range(5):
    update(1 / 60)
