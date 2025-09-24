from pgzero.builtins import *
from pgzero import animation
import itertools

WIDTH = 800
HEIGHT = 800
#print(animation.TWEEN_FUNCTIONS
MARGIN = 20

def position_for_block(i):
    BLOCK_POSITIONS = [[(150, (i * 50 + i * MARGIN)), (WIDTH - 150, (i * 50 + i * MARGIN))] for i in range(len(animation.TWEEN_FUNCTIONS))]
    return BLOCK_POSITIONS[i]



positions = [itertools.cycle(position_for_block(i)) for i in range(len(animation.TWEEN_FUNCTIONS))]
blocks = [Actor('block', center=next(positions[i])) for i in range(len(animation.TWEEN_FUNCTIONS))]

line_centers = [(WIDTH/2, i * (50 + MARGIN)) for i in range(len(animation.TWEEN_FUNCTIONS))]

def draw():
    screen.clear()
    #[block.draw() for block in blocks]
    for i, easing_f_name in enumerate(animation.TWEEN_FUNCTIONS):
        block = blocks[i]
        screen.draw.text(easing_f_name, line_centers[i])
        block.draw()


def move_blocks():
    for i, easing_f_name in enumerate(animation.TWEEN_FUNCTIONS):
        animate(
            blocks[i],
            easing_f_name,
            duration=5,
            pos = next(positions[i])

        )

"""
def move_block():
    animate(
        block,
        'bounce_end',
        duration=1,
        pos=next(block_positions)
    )
""";

move_blocks()  # start one move now
clock.schedule_interval(move_blocks, 6)

