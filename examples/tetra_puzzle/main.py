"""
The MIT License (MIT)

Copyright (c) 2015 David Bern

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import random


def grid_list(block_size):
    """
    Generates a gridlist used shape class
    """
    grids = []
    for y in range(-5, 1):
        row = []
        for x in range(0, 6):
            row.append((x * block_size, y * block_size))
        grids.append(row)

    return grids


class GameOver(Exception):
    """
    Exception that is raised when a brick causes a game over state.
    """


class Shape(object):
    """
    This will make the foundation for a Shape that the others shapes
    will inherit.
    """

    def __init__(self, x_pos, size, color):
        """
        Inits the shape to start at y_pos and every block is of size in size.
        OShape consists of 4 blocks, each block is size wide and high.
        """
        # the widths and heights is determined by the shape and block size.
        self.block_size = size
        self._width = size
        self._height = size

        # Rows of blocks.
        # _block_init() sets allocates all the rectangles and resets the shape
        # to start position.
        self._x = x_pos - (self.block_size * 3)
        self._y = 0
        self.piece = []

        self.grid = grid_list(self.block_size)

        self.color = color

    def shape_grid_update(self):
        """
        Update shapes position with the given _x and _y value.
        To be used after move or rotation is performed on the shape.
        """
        for row_n, row in enumerate(self.piece):
            for element_n, element in enumerate(row):
                if element is not None:
                    start_x, start_y = self.grid[row_n][element_n]
                    self.piece[row_n][element_n].x = start_x + self._x
                    self.piece[row_n][element_n].y = start_y + self._y

    def draw(self):
        """
        Draws all the blocks inside the shape.
        """
        for row in self.piece:
            for element in row:
                if element is not None:
                    screen.draw.filled_rect(element, self.color)

    def pos_rotate(self):
        """
        Rotate shape clockwise
        """
        # Transpose the list
        transposed = [new_row for new_row in zip(*self.piece)]

        # Reverse elements in each row.
        rotated_shape = []
        for row in transposed:
            row = list(row)
            reversed_row = [element for element in reversed(row)]
            rotated_shape.append(reversed_row)

        self.piece = rotated_shape
        self.shape_grid_update()

    def neg_rotate(self):
        """
        Rotate shape clockwise
        """
        # Transpose the list
        transposed = [new_row for new_row in zip(*self.piece)]

        # Reverse elements in each row.
        rotated_shape = []
        for row in reversed(transposed):
            row = list(row)
            rotated_shape.append(row)

        self.piece = rotated_shape
        self.shape_grid_update()

    def move_down(self, speed):
        """
        Moves the shape downwards in the speed passed in arg speed.
        speed is the number of pixels to move per update.
        """
        self._y += speed
        self.shape_grid_update()

    def move_up(self, speed):
        """
        Moves the shape upwards in the speed passed in arg speed.
        speed is the number of pixels to move per update.
        """
        self._y -= speed
        self.shape_grid_update()

    def move_right(self):
        """
        Moves the shape 1 step to the right.
        """
        self._x += self.block_size
        self.shape_grid_update()

    def move_left(self):
        """
        Moves the shape 1 step to the left
        """
        self._x -= self.block_size
        self.shape_grid_update()

    def bottom(self):
        """
        Gives the bottom pos of the first block in the first row.
        """
        return self._y

    def left(self):
        """
        Gives the left pos of the first block in the first row.
        """
        x_pos = []
        for row in self.piece:
            for element in row:
                if element is not None:
                    x_pos.append(element.x)

        return min(x_pos)

    def right(self):
        """
        Gives the right pos of the last block in the first row.
        """
        x_pos = []
        for row in self.piece:
            for element in row:
                if element is not None:
                    x_pos.append(element.x)

        return max(x_pos)

    def top(self):
        """
        Gives the top pos of the first block in the second row.
        """
        # second row, first block will work fine.
        return self._y + (self.block_size * 2)

    def gameboard_collision(self, gameboard):
        """
        Check if this piece have collided with any other piece on the bottom.
        """
        for row in self.piece:
            for element in row:
                if element is not None:
                    if not gameboard.contains(element):
                        if element.bottom > gameboard.bottom:
                            return True
                        elif self.right() >= gameboard.right:
                            return True
                        elif self.left() < gameboard.left:
                            return True
        return False

    def shape_collision(self, other_pieces):
        """
        Check if this piece have collided with any other piece on the bottom.
        """

        # Unexpected behaviour. As it seems the bottom check is unnecessary
        for row in self.piece:
            for element in row:
                if element is not None:
                    collisions = element.collidelistall(other_pieces)
                    if collisions:
                        return True
        return False

    def get_rect(self):
        """
        Returns a list of rects
        """
        rect_list = []
        for row in self.piece:
            for element in row:
                if element is not None:
                    rect_list.append(element)
                    # rect_list.extend(row_rects)

        return rect_list

    def remove(self, block_list):
        """
        Compare list of bricks against piece. If any match remove the entity.
        """
        for block in block_list:
            for row in self.piece:
                try:
                    row.remove(block)
                except ValueError:
                    # Expected for some blocks.
                    # Not all blocks resides inside all bricks.
                    pass

    def __str__(self):
        return str(self.piece)


class OShape(Shape):
    """
    Shape:
      xx
      xx
    """

    def __init__(self, x_pos, size, color):
        Shape.__init__(self, x_pos, size, color)
        self.piece = [[None, None, None, None, None, None],
                      [None, None, None, None, None, None],
                      [None, None, Rect((0, 0), (size, size)),
                       Rect((0, 0), (size, size)), None, None],
                      [None, None, Rect((0, 0), (size, size)),
                       Rect((0, 0), (size, size)), None, None],
                      [None, None, None, None, None, None],
                      [None, None, None, None, None, None]]

        # Upate shape with set _x and _y values
        self.shape_grid_update()

    def pos_rotate(self):
        """
        Try to rotate this one to victory is futile
        """
        # This will override the method defined in the base class Shape
        pass

    def neg_rotate(self):
        """
        Try to rotate this one to victory is futile
        """
        # This will override the method defined in the base class Shape
        pass


class LShape(Shape):
    """
    Shape:
      x
      x
      xx
    """

    def __init__(self, x_pos, size, color):
        Shape.__init__(self, x_pos, size, color)
        self.piece = [[None, None, None, None, None, None],
                      [None, None, None, None, None, None],
                      [None, None, Rect((0, 0), (size, size)), None, None, None],
                      [None, None, Rect((0, 0), (size, size)), None, None, None],
                      [None, None, Rect((0, 0), (size, size)), Rect(
                          (0, 0), (size, size)), None, None],
                      [None, None, None, None, None, None]]

        # Upate shape with set _x and _y values
        self.shape_grid_update()


class IShape(Shape):
    """
    Shape:
      x
      x
      x
      x
    """

    def __init__(self, x_pos, size, color):
        Shape.__init__(self, x_pos, size, color)
        self.piece = [[None, None, None, None, None, None],
                      [None, None, Rect((0, 0), (size, size)), None, None, None],
                      [None, None, Rect((0, 0), (size, size)), None, None, None],
                      [None, None, Rect((0, 0), (size, size)), None, None, None],
                      [None, None, Rect((0, 0), (size, size)), None, None, None],
                      [None, None, None, None, None, None]]

        # Upate shape with set _x and _y values
        self.shape_grid_update()


class ZShape(Shape):
    """
    Shape:
     xx
      xx
    """

    def __init__(self, x_pos, size, color):
        Shape.__init__(self, x_pos, size, color)
        self.piece = [[None, None, None, None, None, None],
                      [None, None, None, None, None, None],
                      [None, None, Rect((0, 0), (size, size)), Rect(
                          (0, 0), (size, size)), None, None],
                      [None, None, None, Rect((0, 0), (size, size)), Rect(
                          (0, 0), (size, size)), None],
                      [None, None, None, None, None, None],
                      [None, None, None, None, None, None]]

        # Upate shape with set _x and _y values
        self.shape_grid_update()


class SShape(Shape):
    """
    Shape:
      xx
     xx
    """

    def __init__(self, x_pos, size, color):
        Shape.__init__(self, x_pos, size, color)
        self.piece = [[None, None, None, None, None, None],
                      [None, None, None, None, None, None],
                      [None, None, None, Rect((0, 0), (size, size)), Rect(
                          (0, 0), (size, size)), None],
                      [None, None, Rect((0, 0), (size, size)), Rect(
                          (0, 0), (size, size)), None, None],
                      [None, None, None, None, None, None],
                      [None, None, None, None, None, None]]

        # Upate shape with set _x and _y values
        self.shape_grid_update()


class TShape(Shape):
    """
    Shape:
     xxx
      x
    """

    def __init__(self, x_pos, size, color):
        Shape.__init__(self, x_pos, size, color)
        self.piece = [[None, None, None, None, None, None],
                      [None, None, None, None, None, None],
                      [None, None, Rect((0, 0), (size, size)),
                       Rect((0, 0), (size, size)),
                       Rect((0, 0), (size, size)), None],
                      [None, None, None, Rect((0, 0), (size, size)), None, None],
                      [None, None, None, None, None, None],
                      [None, None, None, None, None, None]]

        # Upate shape with set _x and _y values
        self.shape_grid_update()


class JShape(Shape):
    """
    Shape:
      x
      x
     xx
    """

    def __init__(self, x_pos, size, color):
        Shape.__init__(self, x_pos, size, color)
        self.piece = [[None, None, None, None, None, None],
                      [None, None, None, None, None, None],
                      [None, None, Rect((0, 0), (size, size)), None, None, None],
                      [None, None, Rect((0, 0), (size, size)), None, None, None],
                      [None, Rect((0, 0), (size, size)), Rect((0, 0), (size, size)),
                       None, None, None],
                      [None, None, None, None, None, None]]

        # Upate shape with set _x and _y values
        self.shape_grid_update()


class Bricks(object):
    """
    There is the following kind of bricks
    1: O-shaped
    2: L-shaped
    3: I-shaped
    4: Z-shaped
    5: S-shaped
    6: T-shaped
    7: J-shaped

    There is the following list of colors.
    1: Red (0xFF, 0x0, 0x0)
    2: Yellow (0xF9, 0xFF, 0x0)
    3: Magenta (0xFF, 0x0, 0xFF)
    4: Blue (0x42, 0x0, 0xFF)
    5: Cyan (0x0, 0xFF, 0xFF)
    6: Lime (0x1A, 0xFF, 0x0)
    7: Orange (0xFF, 0xA1, 0x0)

    The Brick class will function as a bridge for all the shapes
    and as a container for bricks.
    """

    def __init__(self, block_size):
        """
        Valid data for parameter shape is:
        1, 2, 3, 4
        """
        self.block_size = block_size
        self.bricklist = []

        # A dict with references to the constructor for each available shape.
        self.shape_list = {1: OShape, 2: LShape, 3: IShape, 4: ZShape,
                           5: SShape, 6: TShape, 7: JShape}
        # A-Arcade color theme
        self.color_palette = {1: (0xFF, 0x0, 0x0), 2: (0xF9, 0xFF, 0x0),
                              3: (0xFF, 0x0, 0xFF), 4: (0x42, 0x0, 0xFF),
                              5: (0x0, 0xFF, 0xFF), 6: (0x1A, 0xFF, 0x0),
                              7: (0xFF, 0xA1, 0x0)}

    def new_brick(self, shape, color, pos, size):
        """
        Adds a new brick to the list
        """
        # Check if parameter shape is valid else create the Brick piece.
        if shape not in self.shape_list:
            raise ValueError('Not in shape_list: {0}'.format(shape))
        elif color not in self.color_palette:
            raise ValueError('Not in color_palette: {0}'.format(color))
        else:
            self.bricklist.append(self.shape_list[shape](
                pos, size, self.color_palette[color]))

    @property
    def bottom(self):
        """
        Returns the position of the bottom.
        """
        return self.bricklist[-1].bottom()

    def move_list_down(self, move_list):
        """
        Moves the list of blocks one step down.
        """
        for block in move_list:
            block.y += self.block_size

    def move_active_down(self, speed):
        """
        Move active brick down in a given speed
        """
        self.bricklist[-1].move_down(speed)

    def move_active_up(self, speed):
        """
        Move active brick up with a given speed
        """
        self.bricklist[-1].move_up(speed)

    def move_active_right(self):
        """
        Move brick right one step
        """
        self.bricklist[-1].move_right()

    def move_active_left(self):
        """
        Move active brick left one step
        """
        self.bricklist[-1].move_left()

    def pos_rotate_active(self):
        """
        Rotates active brick 90deg.
        """
        self.bricklist[-1].pos_rotate()

    def neg_rotate_active(self):
        """
        Rotates active brick -90deg.
        """
        self.bricklist[-1].neg_rotate()

    def draw(self):
        """
        Draw shape on to the screen
        """
        for brick in self.bricklist:
            brick.draw()

    def gameboard_collision(self, gameboard):
        """
        Check if Brick have hit gameboard bottom
        """
        return self.bricklist[-1].gameboard_collision(gameboard)

    def shape_collision(self):
        """
        other_pieces is expected to be a list of type Rect
        If piece have collided with other piece at bottom.
        returns true.
        """
        for brick in self.bricklist[:-1]:
            if self.bricklist[-1].shape_collision(brick.get_rect()):
                return True

        return False

    def bounds_out(self, gameboard):
        """
        Returns True if any of the active brick is out side of the
        gameboard when called.
        Else False
        """
        block_list = self.bricklist[-1].get_rect()
        game_rect = gameboard.get_rect()

        # Check if all the blocks from the brick is inside the gameboard.
        # If not, then return True. otherwise the function will return False
        for block in block_list:
            if not game_rect.contains(block):
                return True

        return False

    def remove(self, block_list):
        """
        If brick contains any of the bricks in list. It will remove them
        """
        for brick in self.bricklist:
            brick.remove(block_list)

    def get_active_rect(self):
        """
        Returns rectangle objects from brick.
        """
        return self.bricklist[-1].get_rect()

    def get_rect_list(self):
        """
        Helper method to compile a list of rects from a list of bricks
        """
        rect_list = []
        for brick in self.bricklist:
            rect_list.extend(brick.get_rect())
        return rect_list


class ScoreBoard(object):
    """
    Shows the game the current score
    """

    def __init__(self, pos):
        self.title = 'Score'
        self.pos_x, self.pos_y = pos
        self.current_score = 0

    def add_to_score(self, points):
        """
        Takes points as argument and adds it to the current score
        """
        # Calculate score multiplier
        multiplier = points / 10

        # Set new score
        self.current_score += int(points * multiplier)

    def draw(self):
        """
        Draws title and current score to surface
        """
        screen.draw.text(self.title,
                         (self.pos_x, self.pos_y),
                         color=(0xDE, 0xAD, 0xFF),
                         fontsize=20)
        screen.draw.text(str(self.current_score),
                         (self.pos_x, self.pos_y + 20),
                         color=(0x00, 0xAD, 0xFF),
                         fontsize=20)


class GameBoard(object):
    """
    Implements the play area and is judge that decides what rectangles
    that should be removed and which dead bricks that should move down.
    """

    def __init__(self, position, gameboard_size, block_size, color):
        pos_x, pos_y = position
        self._pos_x = pos_x
        self._pos_y = pos_y
        self.cols, self.rows = gameboard_size
        self.block_size = block_size
        width = self.cols * self.block_size
        height = self.rows * self.block_size
        self._board = Rect(position, (width, height))
        self.color = color

    def center(self):
        """
        Returns the centrum pos in the X axis.
        """
        center = (self._board.width / 2) + self._pos_x
        return center

    def get_rect(self):
        """
        Returns a Rect object of the GameBoard
        """
        return self._board

    def draw(self):
        """
        To be called when we want it to be drawn onto the screen surface.
        """
        screen.draw.filled_rect(self._board, self.color)

    def ruler(self, rects):
        """
        Takes a list of bricks. Returns a list of rects that should be removed
        from the first row that it encounters
        and a list of rects that should be moved down a row.

        If nothing to report, it returns a tuple of (None, None)
        """
        # Get a list of every block that is available on the gameboard.
        blocks = rects

        # A complete row, is a row with the same amount of blocks
        # as there is columns
        complete_row = self.cols

        # Create a ruler that can be used to check if a row is full of blocks.
        ruler_rect = Rect((self._pos_x, self._board.bottom - self.block_size),
                          (self._board.width, self.block_size))

        # If a row is full, we need to figure out if there is
        # any blocks above that row that should be moved down.
        other_rect = Rect((self._pos_x, self._pos_y),
                          (self._board.width, self._board.height))
        remove_list = []
        move_down_list = []

        # Uses the ruler rect to check if all the columns in row is filled.
        # If so, it creates a list of blocks that should be removed
        # and a list of blocks that should be moved one row down.
        for _ in range(0, self.rows):
            # Area to capture rects above the row for which the ruler is at.
            other_rect.height -= self.block_size

            collision_indices = ruler_rect.collidelistall(blocks)
            move_down_indices = other_rect.collidelistall(blocks)
            if len(collision_indices) == complete_row:
                for index in collision_indices:
                    remove_list.append(blocks[index])
                for index in move_down_indices:
                    move_down_list.append(blocks[index])

                return (remove_list, move_down_list)

            # Step the ruler to next row.
            ruler_rect.y -= self.block_size

        # No full row, no blocks the be moved down.
        return (None, None)


class Game(object):
    """
    Game board, bricks and controls.
    """

    def __init__(self, x, y, cols, rows):
        """
        """
        # Block setting
        self.block_size = 20

        self._xpos = x
        self._ypos = y
        self._cols = cols
        self._rows = rows

        self.width = cols * self.block_size
        self.height = rows * self.block_size
        self.gameboard = GameBoard(
            (x, y), (cols, rows), self.block_size, (0x00, 0x00, 0x00))

        # Scoreboard
        margin = 10
        self.scoreboard = ScoreBoard((self._xpos + self.width + margin,
                                      self._ypos))

        # Contains a list of previously active bricks.
        self.bricks = Bricks(self.block_size)
        # Speed affects all moving objects, such as the active_brick
        self.speed = 1

        # A lock that will be False once the game hits the state of game over.
        self.game_active = True
        self.game_pause = False

        self.new_brick()

    def new_brick(self):
        """
        Creates a new brick when previous get locked in place
        """
        self.bricks.new_brick(random.randint(1, 7),
                              random.randint(1, 7),
                              self.gameboard.center(),
                              self.block_size)

    def draw(self):
        """
        Draw game
        """
        self.gameboard.draw()
        self.bricks.draw()
        self.scoreboard.draw()

        if not self.game_active:
            screen.draw.text('Game Over', (40, 100), color=(
                0xDE, 0xAD, 0xFF), fontsize=80)

    def remove_complete_rows(self):
        """
        For every complete row, request to remove it.
        The request is sent to each brick in the game.
        """
        points = 0
        # Check if row/rows became complete
        while True:
            remove_list, move_list = self.gameboard.ruler(self.bricks.get_rect_list())
            if remove_list:
                self.bricks.remove(remove_list)
                points += len(remove_list)

            if move_list:
                self.bricks.move_list_down(move_list)

            else:
                break

        # Add points to scoreboard
        self.scoreboard.add_to_score(points)

    def toggle_pause(self):
        """
        Pause/Un-pause the game
        """
        self.game_pause = not self.game_pause

    def proceed(self):
        """
        Is called to change the state of the game.
        """
        # Is brick active, if not, kill it and create a new one.
        if self.found_collision():
            self.bricks.move_active_up(self.speed)
            self.remove_complete_rows()
            # Game over if brick is outside
            if self.bricks.bounds_out(self.gameboard):
                # Draw game over to the screen and raise GameOver
                self.game_active = False
                raise GameOver
            else:
                self.new_brick()

        else:
            self.bricks.move_active_down(self.speed)

    def found_collision(self):
        """
        Check if active brick have collided with anything.
        """
        if self.bricks.gameboard_collision(self.gameboard.get_rect()):
            return True
        elif self.bricks.shape_collision():
            return True
        else:
            return False

    def controls(self, direction):
        """
        Will be called for a given intervall. This prevents the blocks from
        flying from left to right in high speed
        """

        # Check if user want to move brick side ways.
        if direction == 'right':
            self.bricks.move_active_right()
        elif direction == 'left':
            self.bricks.move_active_left()
        elif direction == 'down':
            self.bricks.move_active_down(self.speed * 10)
        elif direction == 'pos_rotate':
            self.bricks.pos_rotate_active()
        elif direction == 'neg_rotate':
            self.bricks.neg_rotate_active()

        # Damage control after collision
        if self.found_collision():
            if direction == 'right':
                self.bricks.move_active_left()
            elif direction == 'left':
                self.bricks.move_active_right()
            elif direction == 'down':
                self.bricks.move_active_up(self.speed * 10)
            elif direction == 'pos_rotate':
                self.bricks.neg_rotate_active()
            elif direction == 'neg_rotate':
                self.bricks.pos_rotate_active()

    def reset(self):
        """
        Restarts the game
        """
        Game.__init__(self, self._xpos, self._ypos, self._cols, self._rows)


WIDTH = 500
HEIGHT = 800

music.set_volume(0.5)
music.play('hhavok-main')

# Create a gamecontroller and a gameboard with a width and a height
# Width and height is given in columns and rows.
TETRA_PUZZLE = Game(100, 50, 10, 20)

# Global that keeps track on wheen to increase the speed on
# right and left movement
SPEEDOMETER_LEFT = 0
SPEEDOMETER_RIGHT = 0


def control_tick():
    """
    Gets triggerad by clock.
    Tells the game betris what the user want to do, if any.
    """
    global SPEEDOMETER_RIGHT
    global SPEEDOMETER_LEFT

    if TETRA_PUZZLE.game_active:
        if keyboard.space:
            TETRA_PUZZLE.controls('down')
        elif keyboard.right:
            if SPEEDOMETER_LEFT:
                SPEEDOMETER_LEFT = 0
            SPEEDOMETER_RIGHT += 0.01
            TETRA_PUZZLE.controls('right')
        elif keyboard.left:
            if SPEEDOMETER_RIGHT:
                SPEEDOMETER_RIGHT = 0
            SPEEDOMETER_LEFT += 0.01
            TETRA_PUZZLE.controls('left')


def on_key_down(key):
    # if key is keys.RIGHT:
    # TETRA_PUZZLE.controls('right')
    # elif key is keys.LEFT:
    # TETRA_PUZZLE.controls('left')
    if key is keys.R:
        TETRA_PUZZLE.reset()
    elif key is keys.P:
        TETRA_PUZZLE.toggle_pause()
    elif key is keys.UP:
        TETRA_PUZZLE.controls('pos_rotate')
    elif key is keys.DOWN:
        TETRA_PUZZLE.controls('neg_rotate')


# Setup time between each check of user controls.
clock.schedule_interval(control_tick, (0.05 - SPEEDOMETER_RIGHT) - SPEEDOMETER_LEFT)


def update():
    """
    Update block position.
    """
    if TETRA_PUZZLE.game_active and not TETRA_PUZZLE.game_pause:
        try:
            TETRA_PUZZLE.proceed()
        except GameOver:
            draw()


def draw():
    """
    Draw game
    """
    screen.fill((0xFF, 0xFF, 0xFF))
    TETRA_PUZZLE.draw()
