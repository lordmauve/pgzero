import random
import math


WIDTH = 800
HEIGHT = 600

DRAG = 0.8  # fraction of speed lost per second
PARTICLE_COLOR = 255, 230, 128
MAX_AGE = 3

particles = []

def explode(x, y, speed=300):
    age = 0
    for _ in range(100):
        angle = random.uniform(0, math.tau)
        radius = random.uniform(0, 1) ** 0.5

        vx = speed * radius * math.sin(angle)
        vy = speed * radius * math.cos(angle)
        particles.append((x, y, vx, vy, age))


def draw():
    screen.clear()
    for x, y, *_ in particles:
        screen.surface.set_at((int(x), int(y)), PARTICLE_COLOR)


def update(dt):
    new_particles = []
    for (x, y, vx, vy, age) in particles:
        if age + dt > MAX_AGE:
            continue
        drag = DRAG ** dt
        vx *= drag
        vy *= drag
        x += vx * dt
        y += vy * dt
        age += dt
        new_particles.append((x, y, vx, vy, age))
    particles[:] = new_particles


def explode_random():
    x = random.randrange(WIDTH)
    y = random.randrange(HEIGHT)
    explode(x, y)

clock.schedule_interval(explode_random, 1.5)
