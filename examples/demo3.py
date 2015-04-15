alien = Actor('alien')

TITLE = "Alien walk"
WIDTH = 500
HEIGHT = alien.height + 20

# Define colours we want to use as RGB
BLACK = 0, 0, 0

# The initial position of the alien
alien.pos = -alien.width, 10


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
    # The alien may already be shown as hurt. In this case we need to prolong
    # the time it is shown as hurt. Calling unschedule() will cancel the
    # previous scheduled recovery if there was one. Then we can schedule the
    # alien to recover 1 second from now.
    clock.unschedule(set_alien_normal)
    clock.schedule(set_alien_normal, 1.0)


def set_alien_normal():
    """Set the current alien sprite to the normal image."""
    alien.image = 'alien'
