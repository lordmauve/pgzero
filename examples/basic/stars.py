import math
import random

WIDTH = 1000
HEIGHT = 1000 * 9 // 16
ACCEL = 1.0  # Warp factor per second
DRAG = 0.71  # Fraction of speed per second
TRAIL_LENGTH = 2
MIN_WARP_FACTOR = 0.1
BOUNDS = Rect(0, 0, WIDTH, HEIGHT)
FONT = 'eunomia_regular'


warp_factor = MIN_WARP_FACTOR
centerx = WIDTH // 2
centery = HEIGHT // 2
stars = []


class Star:
    __slots__ = (
        'pos', 'vel', 'brightness',
        'speed', 'position_history'
    )

    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.brightness = 10
        self.speed = math.hypot(*vel)

    @property
    def end_pos(self):
        """Get the point where the star trail ends."""
        x, y = self.pos
        vx, vy = self.vel

        return (
            x - vx * warp_factor * TRAIL_LENGTH / 60,
            y - vy * warp_factor * TRAIL_LENGTH / 60,
        )


def draw():
    screen.clear()

    # Draw all our stars
    for star in stars:
        b = star.brightness
        color = (b, b, b)  # a grey
        screen.draw.line(star.end_pos, star.pos, color)

    # Head-up-display
    screen.draw.text(
        "III Warp {:0.1f} III".format(warp_factor),
        fontsize=40,
        fontname=FONT,
        midbottom=(WIDTH // 2, HEIGHT - 40),
        color=(180, 160, 0),
        gcolor=(120, 100, 0),
    )
    screen.draw.text(
        "Hold SPACE to accelerate",
        fontsize=30,
        fontname=FONT,
        midbottom=(WIDTH // 2, HEIGHT - 8),
        color=(90, 80, 0),
        gcolor=(50, 40, 0),
    )


def update(dt):
    global stars, warp_factor

    # Calculate the new warp factor
    if keyboard.space:
        # If space is held, accelerate
        warp_factor += ACCEL * dt

    # Apply drag to slow us, regardless of whether space is held
    warp_factor = (
        MIN_WARP_FACTOR +
        (warp_factor - MIN_WARP_FACTOR) * DRAG ** dt
    )

    # Spawn new stars until we have 300
    while len(stars) < 300:
        # Pick a direction and speed
        angle = random.uniform(-math.pi, math.pi)
        speed = 255 * random.uniform(0.3, 1.0) ** 2

        # Turn the direction into position and velocity vectors
        dx = math.cos(angle)
        dy = math.sin(angle)
        d = random.uniform(25 + TRAIL_LENGTH, 100)
        pos = centerx + dx * d, centery + dy * d
        vel = speed * dx, speed * dy

        stars.append(Star(pos, vel))

    # Update the positions of stars
    for s in stars:
        x, y = s.pos
        vx, vy = s.vel

        # Move according to speed and warp factor
        x += vx * warp_factor * dt
        y += vy * warp_factor * dt
        s.pos = x, y

        # Grow brighter
        s.brightness = min(s.brightness + warp_factor * 200 * dt, s.speed)

        # Get faster
        s.vel = vx * 2 ** dt, vy * 2 ** dt

    # Drop any stars that are completely off-screen
    stars = [
        star
        for star in stars
        if BOUNDS.collidepoint(star.end_pos)
    ]


# Jump-start the star field
for _ in range(30):
    update(0.5)
for _ in range(5):
    update(1 / 60)
