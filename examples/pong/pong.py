# Pong is a two-dimensional sports game that simulates table tennis.
# The player controls an in-game paddle by moving it vertically across
# the left side of the screen, and can compete against either a
# computer-controlled opponent or another player controlling a second
# paddle on the opposing side. Players use the paddles to hit a ball
# back and forth. The aim is for each player to reach eleven points
# before the opponent; points are earned when one fails to return
# the ball to the other.

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

class Score():

    def __init__(self):
        self.left = 0
        self.right = 0

score = Score()


# TODO: extend Rect and use center...
class Paddle():

    def __init__(self, start_x, start_y):
        self.pos_x = start_x
        self.pos_y = start_y

    @property
    def pos(self):
        return (self.pos_x, self.pos_y)

    def draw(self):
        rect = Rect(self.pos, (PADDLE_WIDTH, PADDLE_HEIGHT))
        screen.draw.filled_rect(rect, MAIN_COLOR)


class GameFinished(Exception):
    """The game is finished"""


class TennisBall():
    """
    Represents a tennis ball on the screen
    """

    def __init__(self, start_pos):
        self.pos_x = start_pos[0]
        self.pos_y = start_pos[1]

        self.dx = 5
        self.dy = 5

    @property
    def pos(self):
        return (self.pos_x, self.pos_y)

    def move(self):
        self.pos_x += self.dx
        self.pos_y += self.dy

        if self.pos_x >= WIDTH:
            score.left += 1

        if self.pos_x <= 0:
            score.right += 1

        if self.pos_y >= HEIGHT:
            score.left += 1

        if self.pos_y <= 0:
            score.right += 1

        if score.left == 11 or score.right == 11:
            raise GameFinished()

    def draw(self):
        screen.draw.filled_circle(
            (self.pos_x, self.pos_y),
            TENNIS_BALL_RADIUS,
            MAIN_COLOR)


class Game():

    def __init__(self):
        self.started = False
        self.finished = False

        self.left_paddle = Paddle(20, HEIGHT/2 - PADDLE_HEIGHT/2)
        self.right_paddle = Paddle(WIDTH-40, HEIGHT/2 - PADDLE_HEIGHT/2)

        tennis_ball_pos = (20 + PADDLE_WIDTH + 10,
            self.left_paddle.pos_y + PADDLE_HEIGHT / 2)
        self.tennis_ball = TennisBall(tennis_ball_pos)

    def proceed(self):
        try:
            self.tennis_ball.move()

            # check for end game conditions
            if self.tennis_ball.pos == self.left_paddle.pos:
                self.tennis_ball.dx = -self.tennis_ball.dx

            if self.tennis_ball.pos == self.right_paddle.pos:
                self.tennis_ball.dx = -self.tennis_ball.dx


        except GameFinished:
            self.finished = True

    def draw(self):
        # slightly gray background
        screen.fill((64, 64, 64))

        screen.draw.text(
            '({}, {})'.format(self.tennis_ball.pos_x, self.tennis_ball.pos_y),
            color=MAIN_COLOR,
            center=(WIDTH/2, HEIGHT - 20),
            fontsize=24
        )

        # show the score for the left player
        screen.draw.text(
            '{}'.format(score.left),
            color=MAIN_COLOR,
            center=(WIDTH/4, 20),
            fontsize=64
        )

        # show the score for the right player
        screen.draw.text(
            '{}'.format(score.right),
            color=MAIN_COLOR,
            center=(WIDTH/2 + WIDTH/4, 20),
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

game = Game()


def draw():
    game.draw()


def update():
    if not game.started:
        return

    if game.finished:
        return

    game.proceed()


def on_key_down(key):
    if key == keys.space:
        if not game.started:
            game.started = True

