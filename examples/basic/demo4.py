alien = Actor('alien', anchor=('middle', 'bottom'))

TITLE = "Alien walk"
WIDTH = 500
HEIGHT = alien.height + 100
GROUND = HEIGHT - 10

# The initial position of the alien
alien.left = 0
alien.y = GROUND


def draw():
    """Clear the screen and draw the alien."""
    screen.fill((0, 0, 0))
    alien.draw()


def update():
    """Move the alien around using the keyboard."""
    if keyboard.left:
        alien.x -= 2
    elif keyboard.right:
        alien.x += 2

    if keyboard.space:
        alien.y = GROUND - 50
        animate(alien, y=GROUND, tween='bounce_end', duration=.5)

    # If the alien is off the screen,
    # move it back on screen
    if alien.right > WIDTH:
        alien.right = WIDTH
    elif alien.left < 0:
        alien.left = 0
