import random

TITLE = 'Flappy Bird'
WIDTH = 400
HEIGHT = 708

# These constants control the difficulty of the game
GAP = 130
GRAVITY = 0.3
FLAP_STRENGTH = 6.5
SPEED = 3

bird = Actor('bird1', (75, 200))
bird.dead = False
bird.score = 0
bird.vy = 0

wall_top = Actor('top', anchor=('left', 'bottom'), pos=(-100, 0))
wall_bottom = Actor('bottom', anchor=('left', 'top'), pos=(-100, 0))


def reset_walls():
    wall_gap = random.randint(200, HEIGHT - 200)
    wall_top.pos = (WIDTH, wall_gap - GAP // 2)
    wall_bottom.pos = (WIDTH, wall_gap + GAP // 2)


def update_walls():
    wall_top.left -= SPEED
    wall_bottom.left -= SPEED
    if wall_top.right < 0:
        reset_walls()
        bird.score += 1


def update_bird():
    uy = bird.vy
    bird.vy += GRAVITY
    bird.y += (uy + bird.vy) / 2
    bird.x = 75

    if not bird.dead:
        if bird.vy < -3:
            bird.image = 'bird2'
        else:
            bird.image = 'bird1'

    if bird.colliderect(wall_top) or bird.colliderect(wall_bottom):
        bird.dead = True
        bird.image = 'birddead'

    if not 0 < bird.y < 720:
        bird.y = 200
        bird.dead = False
        bird.score = 0
        bird.vy = 0
        reset_walls()


def update():
    update_walls()
    update_bird()


def on_key_down():
    if not bird.dead:
        bird.vy = -FLAP_STRENGTH


def draw():
    screen.blit('background', (0, 0))
    wall_top.draw()
    wall_bottom.draw()
    bird.draw()
    screen.draw.text(
        str(bird.score),
        color='white',
        midtop=(WIDTH // 2, 10),
        fontsize=70,
        shadow=(1, 1)
    )
