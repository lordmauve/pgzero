alien = Actor('alien')

TITLE = "Alien walk"
WIDTH = 500
HEIGHT = alien.height + 20


# The initial position of the alien
alien.pos = 0, 10


def draw():
    """Clear the screen and draw the alien."""
    screen.fill((0, 0, 0))
    alien.draw()


def update():
    """Move the alien around using the keyboard."""
    if keyboard.LEFT:
        alien.x -= 1
    elif keyboard.RIGHT:
        alien.x += 1

    # If the alien is off the screen,
    # move it back on screen
    if alien.right > WIDTH:
        alien.right = WIDTH
    elif alien.left < 0:
        alien.left = 0
