from itertools import product
import random

WIDTH = 801
HEIGHT = 601

LINE_COLOR = 'purple'
CELL_SIZE = 20
cells_x = WIDTH // CELL_SIZE
cells_y = HEIGHT // CELL_SIZE

lines = []
edges = set()

TARGET = (cells_x - 1, cells_y - 1)


def cells():
    """Iterate over all cells in the grid."""
    return product(range(cells_x), range(cells_y))


def cell_to_rect(pos):
    """Get a Rect for the bounds of a cell."""
    x, y = pos
    return Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)


def neighbours(pos):
    """Iterate over the 4 neighbouring grid cells of the given position.

    Only in-bounds cells will be returned.
    """
    x, y = pos
    if x > 0:
        yield (x - 1, y)
    if y > 0:
        yield (x, y - 1)
    if x < cells_x - 1:
        yield (x + 1, y)
    if y < cells_y + 1:
        yield (x, y + 1)


def generate_grid():
    edges.clear()
    unvisited = set(cells())
    pos = (0, 0)
    decision_points = []
    while unvisited:
        unvisited.discard(pos)
        if pos == TARGET:
            # Only one road into target
            pos = decision_points.pop()
            continue

        choices = [p for p in neighbours(pos) if p in unvisited]
        if len(choices) > 1:
            decision_points.append(pos)
            next_pos = random.choice(choices)
        elif len(choices) == 1:
            next_pos = choices[0]
        else:
            pos = decision_points.pop()
            continue

        edge = frozenset((pos, next_pos))
        edges.add(edge)
        pos = next_pos


def draw():
    screen.clear()
    for pos in cells():
        r = cell_to_rect(pos)
        x, y = pos
        if x == 0:
            screen.draw.line(r.topleft, r.bottomleft, LINE_COLOR)
        if y == 0:
            screen.draw.line(r.topleft, r.topright, LINE_COLOR)
        if frozenset((pos, (x + 1, y))) not in edges:
            screen.draw.line(r.topright, r.bottomright, LINE_COLOR)
        if frozenset((pos, (x, y + 1))) not in edges:
            screen.draw.line(r.bottomleft, r.bottomright, LINE_COLOR)
    target.draw()
    pc.draw()


generate_grid()

pc = Actor('pc')
pc.topleft = (0, 0)
pc.grid_pos = (0, 0)

target = Actor('target', topleft=cell_to_rect(TARGET).topleft)


def on_key_down(key):
    px, py = pc.grid_pos
    dest = None
    if key is keys.UP:
        dest = px, py - 1
    elif key is keys.DOWN:
        dest = px, py + 1
    elif key is keys.LEFT:
        dest = px - 1, py
    elif key is keys.RIGHT:
        dest = px + 1, py

    if dest:
        if frozenset((pc.grid_pos, dest)) in edges:
            dest_cell = cell_to_rect(dest)
            animate(
                pc,
                duration=0.1,
                tween='accel_decel',
                topleft=dest_cell.topleft
            )
            pc.grid_pos = dest
            if dest == TARGET:
                clock.schedule_unique(reset, 0.3)


def reset():
    generate_grid()
    pc.topleft = pc.grid_pos = (0, 0)


