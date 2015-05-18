alien = Actor('alien')

TITLE = "Alien walk"
WIDTH = 500
HEIGHT = alien.height + 20

# Define colours we want to use as RGB
BLACK = 0, 0, 0

# The initial position of the alien
alien.topright = 0, 10


def draw():
    """Clear the screen and draw the alien."""
    screen.fill(BLACK)
    alien.draw()


def update():
    """Move the alien."""
    # Move the alien one pixel to the right
    alien.x += 1

    # If the alien is off the right hand side of the screen,
    # move it back off screen to the left-hand side
    if alien.x > WIDTH:
        alien.x = -100


def on_mouse_down(pos):
    """Detect clicks on the alien."""
    if alien.collidepoint(pos):
        set_alien_hurt()


def set_alien_hurt():
    """Set the current alien sprite to the "hurt" image."""
    alien.image = 'alien_hurt'
    sounds.eep.play()
    clock.schedule_unique(set_alien_normal, 1.0)


def set_alien_normal():
    """Set the current alien sprite to the normal image."""
    alien.image = 'alien'
