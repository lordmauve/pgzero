from math import sin, cos
SEGMENT_SIZE = 50
ANGLE = 2.5
PHASE_STEP = 0.3
WOBBLE_AMOUNT = 0.5
SPEED = 4.0

tail = [
    Actor('tail_piece') for _ in range(10)
] + [Actor('tail_hook')]


WIDTH = 800
HEIGHT = 800

t = 0


def draw():
    screen.clear()
    for a in tail[::2]:
        a.draw()
    for a in tail[1::2]:
        a.draw()

def update(dt):
    global t
    t += dt
    x = WIDTH - SEGMENT_SIZE // 2
    y = HEIGHT - SEGMENT_SIZE // 2
    for seg, a in enumerate(tail):
        a.pos = x, y
        angle = ANGLE + WOBBLE_AMOUNT * sin(seg * PHASE_STEP + t * SPEED)
        x += SEGMENT_SIZE * cos(angle)
        y -= SEGMENT_SIZE * sin(angle)
