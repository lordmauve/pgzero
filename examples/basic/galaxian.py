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
    returns (0, 0)).

    """
    if t < 0.5:
        # During the first 0.5s, do a half-loop
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
    divex, divey = dive_path(ship.t)
    startx, starty = ship.dive_start
    ship.pos = (startx + divex * ship.dive_dir, starty + divey)

    # Look ahead along the path to see what direction the ship
    # is moving, and set the ship's rotation accordingly
    ex, ey = dive_path(ship.t + EPSILON)
    ship.angle = math.degrees(math.atan2(
        divey - ey,
        (ex - divex) * ship.dive_dir
    ))

    # If we've reached the bottom of the screen, resume dive mode
    if ship.top > HEIGHT:
        ship.controller_function = ship_controller_pan
        ship.pos = ship.dive_start
        ship.angle = 90
        clock.schedule(start_dive, 3)


EPSILON = 0.001

# Create a ship
ship = Actor('ship', pos=(100, 100), angle=90)
ship.angle = 90  # Face upwards
ship.controller_function = ship_controller_pan
ship.vx = 100


def draw():
    screen.clear()
    ship.draw()


def update(dt):
    ship.controller_function(ship, dt)


def start_dive():
    ship.controller_function = ship_controller_dive
    ship.dive_start = ship.pos
    x, y = ship.pos
    if ship.x < WIDTH // 2:
        ship.dive_dir = 1
    else:
        ship.dive_dir = -1
    ship.t = 0


clock.schedule(start_dive, 3)
