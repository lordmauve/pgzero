"""Game to solve a randomly generated maze.

Ideas for improvement:

* Change maze colour every game
* Randomize the position of the start and goal.
* Add more collectibles, eg. coins.
* Count the number of moves.
* Generate more interesting mazes by biasing the algorithm. Instead of
  `random.choice()`, try a weighted random choice, perhaps with higher weight
  for horizontal moves, or going "straight ahead".

"""

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


def generate_maze():
    """Generate a new maze.

    We use a simple maze generation algorithm that fills all squares in the
    grid, visiting each one once. When we have a choice of where to go next,
    we pick at random. If we have no choices, we backtrack to where we last
    had a choice, and if we still have a choice, we pick a different choice.

    This algorithm is guaranteed to provide a route from the start point to
    all points in the grid.

    See https://en.wikipedia.org/wiki/Maze_generation_algorithm for more on
    maze generation.

    We store the available moves as a set of edges. If `frozenset([a, b])`
    is in `edges`, then there is a route between a and b.

    Seperately, we compute a list of lines to draw, based on the edges that
    are *not* available. We add a line in each such case. Calculating the
    lines to draw one time after the maze is generated makes the game run
    faster than doing the same operation every frame.

    """
    # Generate the grid
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

    # Generate the lines
    lines.clear()
    for pos in cells():
        r = cell_to_rect(pos)
        x, y = pos
        if x == 0:
            lines.append((r.topleft, r.bottomleft))
        if y == 0:
            lines.append((r.topleft, r.topright))
        if frozenset((pos, (x + 1, y))) not in edges:
            lines.append((r.topright, r.bottomright))
        if frozenset((pos, (x, y + 1))) not in edges:
            lines.append((r.bottomleft, r.bottomright))


def draw():
    """Draw the screen.

    Because we save a list of the lines to draw when the grid is generated,
    here we just have to iterate through that list.

    We also draw the PC and target sprites.

    """
    screen.clear()
    for start, end in lines:
        screen.draw.line(start, end, LINE_COLOR)
    target.draw()
    pc.draw()


generate_maze()

pc = Actor('pc')
pc.topleft = (0, 0)
pc.grid_pos = (0, 0)

target = Actor('target', topleft=cell_to_rect(TARGET).topleft)


def on_key_down(key):
    """When a direction key is pressed, move the actor.

    We must check if the actor can move in that direction, ie. that there is
    an edge between the current position and the position we want to move it
    to.

    """
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
                tone.play('A4', 0.3)
            else:
                tone.play('E3', 0.05)
        else:
            tone.play('Ab3', 0.2)


def reset():
    """Reset by generating a new maze and moving the PC back to the start."""
    generate_maze()
    pc.topleft = pc.grid_pos = (0, 0)
