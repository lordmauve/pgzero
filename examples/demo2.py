from images import alien

TITLE = "Alien walk"
WIDTH = 500
HEIGHT = alien.get_height() + 20


# The horizontal position of the alien
x = -50


def draw(screen):
    """Clear the screen and draw the alien."""
    screen.fill((0, 0, 0))
    screen.blit(alien, (x, 10))


def update(dt):
    """Move the alien by one pixel."""
    global x
    x += 1

    # If the alien is off the right hand side of the screen,
    # move it back off screen to the left-hand side
    if x > WIDTH:
        x = -100
