import math

WIDTH = 400
HEIGHT = 800

# How many wobbles the ship does while diving
DIVE_WOBBLE_SPEED = 2

# How far the ship wobbles while diving
DIVE_WOBBLE_AMOUNT = 100


def dive_path(t):
    """Get the ship's position at time t when diving.

    This is relative to the ship's original position (so, at t=0, dive_path(t)
    returns (0, 0)). Here we flip to the right before diving.

    """
    if t < 0.5:
        # During the first 0.5s, do a half-loop to the right
        return (
            50 * (1 - math.cos(2 * t * math.pi)),
            -50 * (math.sin(2 * t * math.pi))
        )

    # For the rest of the time, follow a sinusoidal path downwards
    t -= 0.5
    return (
        DIVE_WOBBLE_AMOUNT * math.cos(t * DIVE_WOBBLE_SPEED),
        t * 350,
    )


def make_individual_dive(start_pos, flip_x=False):
    """Return a function that will return a dive path from start_pos.

    If flip_x is True then the path will be flipped in the x direction.
    """
    dir = -1 if flip_x else 1
    sx, sy = start_pos

    def _dive_path(t):
        x, y = dive_path(t)
        return sx + x * dir, sy + y

    return _dive_path


def ship_controller_pan(ship, dt):
    """Update the ship when the ship is panning."""
    ship.x += ship.vx * dt
    if ship.right > WIDTH - 50:
        ship.vx = -ship.vx
        ship.right = WIDTH - 50
    elif ship.left < 50:
        ship.vx = -ship.vx
        ship.left = 50


def ship_controller_dive(ship, dt):
    """Update the ship when the ship is diving."""
    # Move the ship along the path
    ship.t += dt
    ship.pos = ship.dive_path(ship.t)

    # Look ahead along the path to see what direction the ship
    # is moving, and set the ship's rotation accordingly
    ship.angle = ship.angle_to(ship.dive_path(ship.t + EPSILON))

    # If we've reached the bottom of the screen, resume dive mode
    if ship.top > HEIGHT:
        ship.controller_function = ship_controller_pan
        ship.pos = ship.dive_path(0)
        ship.angle = 90
        clock.schedule(start_dive, 3)


EPSILON = 0.001

# Create an Actor using the 'ship' sprite
ship = Actor('ship', pos=(100, 100), angle=90)
ship.angle = 90  # Face upwards
ship.controller_function = ship_controller_pan
ship.vx = 100


def draw():
    """Just draw the actor on the screen."""
    screen.clear()
    ship.draw()


def update(dt):
    """Update the ship using its current controller function."""
    ship.controller_function(ship, dt)


def start_dive():
    """Make the ship start a dive."""
    # flip the dive if we're on the left of the screen
    flip_x = ship.x < WIDTH // 2
    ship.controller_function = ship_controller_dive
    ship.dive_path = make_individual_dive(ship.pos, flip_x=flip_x)
    ship.t = 0


clock.schedule(start_dive, 3)
