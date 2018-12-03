from math import sin, cos

# Constants that control the wobble effect
SEGMENT_SIZE = 50  # pixels from one segment to the next
ANGLE = 2.5  # Base direction for the tail (radians)
PHASE_STEP = 0.3  # How much the phase differs in each tail piece (radians)
WOBBLE_AMOUNT = 0.5  # How much of a wobble there is (radians)
SPEED = 4.0  # How fast the wobble moves (radians per second)

# Dimensions of the screen (pixels)
WIDTH = 800
HEIGHT = 800

# The sprites we'll use.
# 10 tail pieces
tail = [Actor('tail_piece') for _ in range(10)]
# Plus a hook piece at the end
tail += [Actor('tail_hook')]

# Keep track of time
t = 0  # seconds


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
