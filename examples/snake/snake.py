import random
from enum import Enum
from collections import deque
from itertools import islice

from pygame.transform import flip, rotate


TILE_SIZE = 24

TILES_W = 20
TILES_H = 15

WIDTH = TILE_SIZE * TILES_W
HEIGHT = TILE_SIZE * TILES_H


def screen_rect(tile_pos):
    """Get the screen rectangle for the given tile coordinate."""
    x, y = tile_pos
    return Rect(TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE)


class Direction(Enum):
    RIGHT = (1, 0)
    UP = (0, -1)
    LEFT = (-1, 0)
    DOWN = (0, 1)

    def opposite(self):
        x, y = self.value
        return Direction((-x, -y))


class Crashed(Exception):
    """The snake has crashed into itself."""


class Snake:
    def __init__(self, pos=(TILES_W // 2, TILES_H // 2)):
        self.pos = pos
        self.dir = Direction.LEFT
        self.length = 4
        self.tail = deque(maxlen=self.length)

        x, y = pos
        for i in range(self.length):
            p = (x + i, y)
            segment = p, self.dir
            self.tail.append(segment)

    @property
    def lastdir(self):
        return self.tail[0][1]

    def move(self):
        dx, dy = self.dir.value
        px, py = self.pos
        px = (px + dx) % TILES_W
        py = (py + dy) % TILES_H

        self.pos = px, py
        segment = self.pos, self.dir
        self.tail.appendleft(segment)
        for t, d in islice(self.tail, 1, None):
            if t == self.pos:
                raise Crashed(t)

    def __len__(self):
        return self.length

    def __contains__(self, pos):
        return any(p == pos for p, d in self.tail)

    def grow(self):
        self.length += 1
        self.tail = deque(self.tail, maxlen=self.length)

    def draw(self):
        for pos in self.tail:
            screen.draw.filled_rect(screen_rect(pos), 'green')


class SnakePainter:
    def __init__(self):
        right, up, left, down = (d.value for d in Direction)
        straight = images.snake_straight
        corner = images.snake_corner
        corner2 = flip(corner, True, False)
        self.tiles = {
            # Straight sections in each direction
            (right, right): straight,
            (up, up): rotate(straight, 90),
            (left, left): rotate(straight, 180),
            (down, down): rotate(straight, 270),

            # Corner sections in the anticlockwise direction
            (right, up): corner,
            (up, left): rotate(corner, 90),
            (left, down): rotate(corner, 180),
            (down, right): rotate(corner, 270),

            # Corner sections in the clockwise direction
            (left, up): corner2,
            (up, right): rotate(corner2, -90),
            (right, down): rotate(corner2, -180),
            (down, left): rotate(corner2, -270),
        }

        head = images.snake_head
        self.heads = {
            right: head,
            up: rotate(head, 90),
            left: rotate(head, 180),
            down: rotate(head, 270),
        }

        tail = images.snake_tail
        self.tails = {
            right: tail,
            up: rotate(tail, 90),
            left: rotate(tail, 180),
            down: rotate(tail, 270),
        }

    def draw(self, snake):
        for i, (pos, dir) in enumerate(snake.tail):
            if not i:
                # draw head
                tile = self.heads[snake.dir.value]
            elif i >= len(snake.tail) - 1:
                # draw tail
                nextdir = snake.tail[i - 1][1]
                tile = self.tails[nextdir.value]
            else:
                nextdir = snake.tail[i - 1][1]
                key = dir.value, nextdir.value
                try:
                    tile = self.tiles[key]
                except KeyError:
                    tile = self.tiles[dir.value, dir.value]

            r = screen_rect(pos)
            screen.blit(tile, r)


class Apple:
    def __init__(self):
        self.pos = 0, 0

    def draw(self):
        screen.blit(images.apple, screen_rect(self.pos))


KEYBINDINGS = {
    keys.LEFT: Direction.LEFT,
    keys.RIGHT: Direction.RIGHT,
    keys.UP: Direction.UP,
    keys.DOWN: Direction.DOWN,
}


snake = Snake()
snake.alive = True

snake_painter = SnakePainter()

apple = Apple()


def place_apple():
    """Randomly place the apple somewhere that isn't currently occupied.

    We will generate coordinates at random until we find some that are not on
    top of the snake.

    """
    if len(snake) == TILES_W * TILES_H:
        raise ValueError("No empty spaces!")

    while True:
        pos = (
            random.randrange(TILES_W),
            random.randrange(TILES_H)
        )

        if pos not in snake:
            apple.pos = pos
            return


def on_key_down(key):
    if not snake.alive:
        return

    dir = KEYBINDINGS.get(key)
    if dir and dir != snake.lastdir.opposite():
        snake.dir = dir
        return


def tick():
    if not snake.alive:
        return

    try:
        snake.move()
    except Crashed:
        snake.alive = False
        stop()
    else:
        if snake.pos == apple.pos:
            snake.grow()
            start()
            place_apple()


def start():
    """Set/update the tick interval.

    This is called whenever the snake grows to make the game run faster.

    """
    interval = max(0.1, 0.4 - 0.03 * (len(snake) - 3))
    clock.unschedule(tick)
    clock.schedule_interval(tick, interval)


def stop():
    """Stop the game from updating."""
    clock.unschedule(tick)


def draw():
    screen.clear()
    snake_painter.draw(snake)
    apple.draw()

    screen.draw.text(
        'Score: %d' % len(snake),
        color='white',
        topright=(WIDTH - 5, 5)
    )

    if not snake.alive:
        screen.draw.text(
            "You died!",
            color='white',
            center=(WIDTH/2, HEIGHT/2)
        )


place_apple()
start()
