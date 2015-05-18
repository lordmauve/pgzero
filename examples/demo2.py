alien = Actor('alien')

TITLE = "Alien walk"
WIDTH = 500
HEIGHT = alien.height + 20


# The initial position of the alien
alien.topright = 0, 10


def draw():
    """Clear the screen and draw the alien."""
    screen.clear()
    alien.draw()


def update():
    """Move the alien by one pixel."""
    alien.x += 1

    # If the alien is off the right hand side of the screen,
    # move it back off screen to the left-hand side
    if alien.left > WIDTH:
        alien.right = 0
