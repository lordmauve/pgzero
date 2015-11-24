import random

TITLE = 'Flappy Bird'
WIDTH = 400
HEIGHT = 708

bird = Actor('bird1', (75, 50))
bird.dead = False
bird.score = 0
bird.jump = 0
bird.jumpSpeed = 10
bird.gravity = 5

wall_top = Actor('top', anchor=('left', 'bottom'), pos=(-100, 0))
wall_bottom = Actor('bottom', anchor=('left', 'top'), pos=(-100, 0))

GAP = 130


def reset_walls():
    wall_gap = random.randint(200, HEIGHT - 200)
    wall_top.pos = (WIDTH, wall_gap - GAP // 2)
    wall_bottom.pos = (WIDTH, wall_gap + GAP // 2)


def update_walls():
    wall_top.left -= 3
    wall_bottom.left -= 3
    if wall_top.right < -0:
        reset_walls()
        bird.score += 1


def update_bird():
    if bird.jump:
        bird.jumpSpeed -= 1
        bird.top -= bird.jumpSpeed
        bird.jump -= 1
    else:
        bird.top += bird.gravity
        bird.gravity += 0.2

    if bird.collidelist([wall_top, wall_bottom]) != -1:
        bird.dead = True
        bird.image = 'birddead'

    if not 0 < bird.y < 720:
        bird.y = 50
        bird.dead = False
        bird.score = 0
        bird.gravity = 5
        reset_walls()


def animate_bird():
    if bird.dead:
        return
    elif bird.image == 'bird1':
        bird.image = 'bird2'
    else:
        bird.image = 'bird1'


def update():
    update_walls()
    update_bird()


def on_key_down():
    if not bird.dead:
        bird.jump = 17
        bird.gravity = 5
        bird.jumpSpeed = 10


WHITE = 255, 255, 255


def draw():
    screen.fill(WHITE)
    screen.blit('background', (0, 0))
    wall_top.draw()
    wall_bottom.draw()
    bird.draw()
    screen.draw.text(
        str(bird.score),
        color=WHITE,
        topright=(WIDTH - 10, 10),
        fontsize=50
    )


clock.schedule_interval(animate_bird, 0.1)
