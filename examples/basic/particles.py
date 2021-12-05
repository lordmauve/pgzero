import random
import math


WIDTH, HEIGHT = 800, 600  # set the window dimensions

DRAG = 0.7  # fraction of speed lost per second
MAX_AGE = 3  # lifetime of a particle

# Control the radius distribution
# <0.5 = weighted towards the outside
# 0.5 = uniform coverage of the circle
# >0.5 = weighted towards the inside
RADIUS_EXP = 0.5
TAU = math.pi * 2  # math.tau is available in python 3.6+

# A global list to hold all our particles
particles = []


def explode(x, y, speed=300, num=200):
    """Create a particle explosion at (x, y).

    `num` is the number of particles to spawn.
    `speed` is the maximum speed of a particle in pixels per second.

    """
    age = 0
    # Pick a random colour
    color = tuple(random.randint(128, 255) for _ in range(3))
    for _ in range(num):  # spawn 300 particles
        # Choose a random angle anywhere in the circle
        angle = random.uniform(0, TAU)
        # Choose a random radius using a controllable distribution
        radius = random.uniform(0, 1) ** RADIUS_EXP

        # Convert angle/radius to a cartesian vector
        vx = speed * radius * math.sin(angle)
        vy = speed * radius * math.cos(angle)
        particles.append((x, y, vx, vy, age, color))  # add it


def draw():
    """Draw all the particles as pixels."""
    screen.clear()
    for x, y, *_, color in particles:  # we only care about position and color
        screen.surface.set_at((round(x), round(y)), color)


def update(dt):
    """Update all particles. dt is the time step in seconds."""
    new_particles = []
    for (x, y, vx, vy, age, color) in particles:
        age += dt  # update the age of the particle
        if age > MAX_AGE:
            continue  # particle is expired, don't keep it

        drag = DRAG ** dt  # amount of drag that is applied
        vx *= drag  # apply drag to the velocity vector
        vy *= drag
        x += vx * dt  # move the particle according to its velocity
        y += vy * dt

        if age > 2:  # If the particle is getting old, fade it
            color = tuple(round(c - 100 * dt) for c in color)

        new_particles.append((x, y, vx, vy, age, color))  # keep it
    particles[:] = new_particles  # write back the particles we're keeping


def explode_random():
    """Create an explosion at a random position on the screen."""
    x = random.randrange(WIDTH)
    y = random.randrange(HEIGHT)
    explode(x, y)


clock.schedule_interval(explode_random, 1.0)  # Schedule explosions every 1s
