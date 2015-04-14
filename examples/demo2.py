alien = Actor('examples/images/alien.png')

TITLE = "Alien walk"
WIDTH = 500
HEIGHT = alien.height + 20


# The initial position of the alien
alien.pos = -alien.width, 10


def draw():
    """Clear the screen and draw the alien."""
    screen.fill((0, 0, 0))
    alien.draw()


def update():
    """Move the alien by one pixel."""
    alien.x += 1

    # If the alien is off the right hand side of the screen,
    # move it back off screen to the left-hand side
    if alien.x > WIDTH:
        alien.x = -100
