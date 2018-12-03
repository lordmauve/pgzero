from math import sin, cos

# Constants that control the wobble effect
SEGMENT_SIZE = 50
ANGLE = 2.5
PHASE_STEP = 0.3
WOBBLE_AMOUNT = 0.5
SPEED = 4.0

# Dimensions of the screen
WIDTH = 800
HEIGHT = 800

# The sprites we'll use.
# 10 tail pieces
tail = [Actor('tail_piece') for _ in range(10)]
# Plus a hook piece at the end
tail += [Actor('tail_hook')]

# Keep track of time
t = 0


def draw():
    screen.clear()
    # First draw the even tail pieces
    for a in tail[::2]:
        a.draw()
    # Now draw the odd tail pieces
    for a in tail[1::2]:
        a.draw()


def update(dt):
    global t
    t += dt
    # Start at the bottom right
    x = WIDTH - SEGMENT_SIZE // 2
    y = HEIGHT - SEGMENT_SIZE // 2
    for seg, a in enumerate(tail):
        a.pos = x, y

        # Calculate an angle to the next piece which wobbles sinusoidally
        angle = ANGLE + WOBBLE_AMOUNT * sin(seg * PHASE_STEP + t * SPEED)

        # Get the position of the next piece using trigonometry
        x += SEGMENT_SIZE * cos(angle)
        y -= SEGMENT_SIZE * sin(angle)
