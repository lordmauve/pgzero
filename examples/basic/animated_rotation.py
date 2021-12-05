"""An example of using animate() and clock scheduling to move actors around.

There are two actors in this example, each with a different movement strategy.

The block
---------

The block moves in a loop around the screen:

* We schedule the move_block() function to be called every 2 seconds using
  clock.schedule_interval().
* The next position of the block is given by calling next() on a "cycle"
  object, returned by itertools.cycle(). This will cycle through the block
  coordinates we provide it, repeating without end.
* We use animate() to move the block.


The ship
--------

The ship moves in a random dance in the middle of the screen. The ship
flips back and forth between a rotation phase and a movement phase:


* next_ship_target(): pick a new target location for the ship at random, and
  animate rotating the ship to aim at it. When the rotation animation is
  complete, we will call move_ship().
* move_ship(): Move the ship to its target. When the move animation is
  complete, we will call next_ship_target().


"""
import random
import itertools


WIDTH = 400
HEIGHT = 400


# Define four sets of coordinates for the block to move between
BLOCK_POSITIONS = [
    (350, 50),
    (350, 350),
    (50, 350),
    (50, 50),
]
# The "cycle()" function will let us cycle through the positions indefinitely
block_positions = itertools.cycle(BLOCK_POSITIONS)


block = Actor('block', center=(50, 50))
ship = Actor('ship', center=(200, 200))


def draw():
    screen.clear()
    block.draw()
    ship.draw()


# Block movement
# --------------

def move_block():
    """Move the block to the next position over 1 second."""
    animate(
        block,
        'bounce_end',
        duration=1,
        pos=next(block_positions)
    )


move_block()  # start one move now
clock.schedule_interval(move_block, 2)  # schedule subsequent moves


# Ship movement
# -------------

def next_ship_target():
    """Pick a new target for the ship and rotate to face it."""
    x = random.randint(100, 300)
    y = random.randint(100, 300)
    ship.target = x, y

    target_angle = ship.angle_to(ship.target)

    # Angles are tricky because 0 and 359 degrees are right next to each other.
    #
    # If we call animate(angle=target_angle) now, it wouldn't know about this,
    # and will simple adjust the value of angle from 359 down to 0, which means
    # that the ship spins nearly all the way round.
    #
    # We can always add multiples of 360 to target_angle to get the same angle.
    # 0 degrees = 360 degrees = 720 degrees = -360 degrees and so on. If the
    # ship is currently at 359 degrees, then having it animate to 360 degrees
    # is the animation we want.
    #
    # Here we calculate how many multiples we need to add so that any rotations
    # will be less than 180 degrees.
    target_angle += 360 * ((ship.angle - target_angle + 180) // 360)

    animate(
        ship,
        angle=target_angle,
        duration=0.3,
        on_finished=move_ship,
    )


def move_ship():
    """Move the ship to the target."""
    animate(
        ship,
        tween='accel_decel',
        pos=ship.target,
        duration=ship.distance_to(ship.target) / 200,
        on_finished=next_ship_target,
    )


next_ship_target()
