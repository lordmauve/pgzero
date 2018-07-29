from math import sin
import random

TITLE = "Shooting Star"
WIDTH = 100
HEIGHT = 500


star = Actor('star', pos=(50, 500))

YELLOW = 255, 240, 128
sparks = []


class Spark:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = 2 * random.random()
        self.age = 0


def draw():
    screen.clear()
    for s in sparks:
        screen.draw.filled_circle((s.x, s.y), 1, YELLOW)
    star.draw()


time = 0

def update(dt):
    global time
    time += dt
    star.scale = 0.75 + 0.25 * sin(time)
    star.angle += 1
    star.y -= 2
    if star.y < -64:
        star.y = 500

    for s in sparks:
        s.y -= s.vy
        s.age += dt

    sparks[:] = [s for s in sparks if s.age < 3.0]


def create_spark():
    w = star.width * 0.4
    x = random.uniform(star.x - w, star.x + w)
    y = star.y
    sparks.append(Spark(x, y))


clock.schedule_interval(create_spark, 0.05)
