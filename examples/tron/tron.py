from pygame import Surface
from pygame import transform
from collections import deque

WIDTH = 800
HEIGHT = 800

# The grid is lower resolution than the screen; this constant
# defines how much
GRID_SIZE = 5

CYAN = (0, 255, 255)
BLACK = (0, 0, 0)


def screen_to_grid(x, y):
    """Convert screen coordinates x, y to grid coords."""
    return round(x / GRID_SIZE), round(y / GRID_SIZE)


trails = Surface(screen_to_grid(WIDTH, HEIGHT))


speed = GRID_SIZE
bike = Actor('bike', anchor_x=28)

# Cardinal directions -> (angle, velocity, reverse)
DIRECTIONS = {
    keys.RIGHT: (0, (speed, 0), keys.LEFT),
    keys.UP: (90, (0, -speed), keys.DOWN),
    keys.LEFT: (180, (-speed, 0), keys.RIGHT),
    keys.DOWN: (270, (0, speed), keys.UP),
}


def reset_bike():
    trails.fill(BLACK)
    bike.pos = (WIDTH + GRID_SIZE) // 2, (HEIGHT + GRID_SIZE) // 2
    bike.dead = False
    bike.angle, bike.v, bike.reverse = DIRECTIONS[keys.RIGHT]
    bike.trail = deque(maxlen=200)


def kill_bike():
    bike.dead = True
    bike.explosion_radius = 2


# Reset the bike immediately
reset_bike()


def update():
    # Fade down the trail
    for t in bike.trail:
        r, g, b, *_ = trails.get_at(t)
        c = round(g * 0.99)
        trails.set_at(t, (round(r * 0.97), c, c))

    if bike.dead:
        bike.explosion_radius += 20
        return
    vx, vy = bike.v
    x, y = bike.pos
    x += vx
    y += vy
    bike.pos = x, y

    trail_pos = screen_to_grid(x, y)

    try:
        current_value = trails.get_at(trail_pos)[2]
    except IndexError:
        # Out of bounds! we crashed
        kill_bike()
        return

    if current_value:
        # We've already set this pixel, so this is a crash
        kill_bike()
    else:
        trails.set_at(trail_pos, (255, 255, 255))
        bike.trail.append(trail_pos)


def draw():
    transform.scale(trails, (WIDTH, HEIGHT), screen.surface)
    if bike.dead:
        screen.draw.circle(
            pos=bike.pos,
            radius=round(bike.explosion_radius),
            color=CYAN,
        )
        screen.draw.text(
            'YOU ARE DEREZZED!\nPRESS SPACE TO RESTART',
            center=(WIDTH // 2, 100),
            color=CYAN,
            fontsize=50,
            fontname="tr2n"
        )
    else:
        bike.draw()


def on_key_down(key):
    if bike.dead:
        if key is keys.SPACE:
            reset_bike()

    elif key in DIRECTIONS and key != bike.reverse:
        bike.angle, bike.v, bike.reverse = DIRECTIONS[key]
