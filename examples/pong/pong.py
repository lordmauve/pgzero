# Pong is a two-dimensional sports game that simulates table tennis.
# The player controls an in-game paddle by moving it vertically across
# the left side of the screen, and can compete against either a
# computer-controlled opponent or another player controlling a second
# paddle on the opposing side. Players use the paddles to hit a ball
# back and forth. The aim is for each player to reach eleven points
# before the opponent; points are earned when one fails to return
# the ball to the other.
import random

WIDTH = 800
HEIGHT = 600
TITLE = 'pong'

# a color used to draw things
MAIN_COLOR = 'yellow'

# width and height of a player paddle
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100

# radius of the tennis ball
TENNIS_BALL_RADIUS = 10

LEFT_PLAYER = "left"
RIGHT_PLAYER = "right"


class Paddle(Rect):
    """
    Paddle represents one player on the screen.

    It is drawn like a long rectangle and positioned either left or
    right on the screen.

    Two helper methods move the paddle up or down.
    """

    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def up(self):
        if self.y - 5 > 40:
            self.y -= 5

    def down(self):
        if self.y + self.height + 5 < HEIGHT - 40:
            self.y += 5

    def draw(self):
        screen.draw.filled_rect(self, MAIN_COLOR)


class TennisBall():
    """
    Represents a tennis ball on the screen
    """

    def __init__(self, start_pos, dt):
        """
        Initialize the tennis ball position and set the movement rate
        """
        self.x, self.y = start_pos
        self.dx = self.dy = dt

    @property
    def pos(self):
        return (self.x, self.y)

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        screen.draw.filled_circle(self.pos, TENNIS_BALL_RADIUS, MAIN_COLOR)


class Game():

    def __init__(self, player):
        self.active_player = player
        self.score_left = 0
        self.score_right = 0

        self.in_progress = False

        # position paddles in the middle of the screen
        middle = HEIGHT/2 - PADDLE_HEIGHT/2
        self.left_paddle = Paddle(20, middle)
        self.right_paddle = Paddle(WIDTH-40, middle)

        self.set_ball(self.ball_pos)

    @property
    def ball_pos(self):
        if self.active_player == LEFT_PLAYER:
            return (20 + PADDLE_WIDTH + 10, self.left_paddle.centery)
        else:
            return (WIDTH - 35 - PADDLE_WIDTH, self.right_paddle.centery)

    def set_ball(self, pos):
        # a ball is set on the paddle of last player that got a point
        dt = 5 if self.active_player == LEFT_PLAYER else -5
        self.tennis_ball = TennisBall(pos, dt)

    def position_ball(self):
        # used when the player moves tha paddle and
        # game is not in progress
        self.tennis_ball.x, self.tennis_ball.y = self.ball_pos

    def score_for_left(self):
        self.in_progress = False
        self.score_left += 1
        self.set_ball(self.ball_pos)

    def score_for_right(self):
        self.in_progress = False
        self.score_right += 1
        self.set_ball(self.ball_pos)

    def proceed(self):
        self.tennis_ball.move()

        # bounce from the walls
        if self.tennis_ball.y <= 40:
            self.tennis_ball.dy = -self.tennis_ball.dy

        if self.tennis_ball.y >= HEIGHT - 40:
            self.tennis_ball.dy = -self.tennis_ball.dy

        # bounce from the paddles
        if self.left_paddle.collidepoint(self.tennis_ball.pos):
            self.tennis_ball.dx = -self.tennis_ball.dx

        if self.right_paddle.collidepoint(self.tennis_ball.pos):
            self.tennis_ball.dx = -self.tennis_ball.dx

        # if we didn't bounce, then that is a score
        if self.tennis_ball.x <= 0:
            self.score_for_right()

        if self.tennis_ball.x >= WIDTH:
            self.score_for_left()

        if self.score_left == 11 or self.score_right == 11:
            self.in_progress = False

    def draw(self):
        # slightly gray background
        screen.fill((64, 64, 64))

        screen.draw.text(
            '({}, {})'.format(self.tennis_ball.x, self.tennis_ball.y),
            color=MAIN_COLOR,
            center=(WIDTH/2, HEIGHT - 20),
            fontsize=24
        )

        screen.draw.text(
            '({}, {})'.format(self.left_paddle.x, self.left_paddle.y),
            color=MAIN_COLOR,
            center=(40, HEIGHT - 20),
            fontsize=24
        )

        screen.draw.text(
            '({}, {})'.format(self.right_paddle.x, self.right_paddle.y),
            color=MAIN_COLOR,
            center=(WIDTH-80, HEIGHT - 20),
            fontsize=24
        )

        # show the score for the left player
        screen.draw.text(
            'Computer: {}'.format(self.score_left),
            color=MAIN_COLOR,
            center=(WIDTH/4 - 20, 20),
            fontsize=64
        )

        # show the score for the right player
        screen.draw.text(
            'Player: {}'.format(self.score_right),
            color=MAIN_COLOR,
            center=(WIDTH/2 + WIDTH/4 - 20, 20),
            fontsize=64
        )

        # a dividing line
        screen.draw.line(
            (WIDTH/2, 40),
            (WIDTH/2, HEIGHT-40),
            color=MAIN_COLOR)

        self.left_paddle.draw()
        self.right_paddle.draw()
        self.tennis_ball.draw()

player = LEFT_PLAYER if random.randint(0, 1000) % 2 == 0 else RIGHT_PLAYER
game = Game(player)


def draw():
    game.draw()


def update():
    if keyboard.up:
        game.right_paddle.up()
    elif keyboard.down:
        game.right_paddle.down()

    # set the position of the ball to be in the middle of the paddle
    if not game.in_progress:
        game.position_ball()

    if game.in_progress:
        game.proceed()



def on_key_down(key):
    # pressing SPACE launches the ball
    if key == keys.SPACE:
        if not game.in_progress:
            game.in_progress = True
