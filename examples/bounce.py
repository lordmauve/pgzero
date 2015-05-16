TITLE = 'Flappy Ball'
WIDTH = 800
HEIGHT = 600

BLUE = 0, 128, 255
GRAVITY = 2000.0  # pixels per second per second


class Ball:
    def __init__(self, initial_x, initial_y):
        self.x = initial_x
        self.y = initial_y
        self.vx = 200
        self.vy = 0
        self.radius = 20

    def draw(self):
        pos = (self.x, self.y)
        screen.draw.filled_circle(pos, self.radius, BLUE)


ball = Ball(50, 100)


def draw():
    screen.clear()
    ball.draw()


def update(dt):
    # Apply constant acceleration formulae
    uy = ball.vy
    ball.vy += GRAVITY * dt
    ball.y += (uy + ball.vy) * 0.5 * dt

    # detect and handle bounce
    if ball.y > HEIGHT - ball.radius:  # we've bounced!
        ball.y = HEIGHT - ball.radius  # fix the position
        ball.vy = -ball.vy * 0.9  # inelastic collision

    # X component doesn't have acceleration
    ball.x += ball.vx * dt
    if ball.x > WIDTH - ball.radius or ball.x < ball.radius:
        ball.vx = -ball.vx


def on_key_down(key):
    """Pressing a key will kick the ball upwards."""
    if key == keys.SPACE:
        ball.vy = -500
