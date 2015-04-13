from pgzero.clock import schedule, unschedule
from images import alien, alien_hurt

TITLE = "Alien walk"
WIDTH = 500
HEIGHT = alien.get_height() + 20


# The rectangle in which the alien will be drawn
alien_rect = alien.get_rect().move((-50, 10))
sprite = alien


def draw(screen):
    """Clear the screen and draw the alien."""
    screen.fill((0, 0, 0))
    screen.blit(sprite, alien_rect.topleft)


def update():
    """Move the alien."""
    # Move the alien one pixel to the right
    alien_rect.x += 1

    # If the alien is off the right hand side of the screen,
    # move it back off screen to the left-hand side
    if alien_rect.x > WIDTH:
        alien_rect.x = -100


def on_mouse_down(pos):
    """Detect clicks on the alien."""
    if alien_rect.collidepoint(pos):
        set_alien_hurt()


def set_alien_hurt():
    """Set the current alien sprite to the "hurt" image."""
    global sprite
    sprite = alien_hurt
    # The alien may already be shown as hurt. In this case we need to prolong
    # the time it is shown as hurt. Calling unschedule() will cancel the
    # previous scheduled recovery if there was one. Then we can schedule the
    # alien to recover 1 second from now.
    unschedule(set_alien_normal)
    schedule(set_alien_normal, 1.0)


def set_alien_normal():
    """Set the current alien sprite to the normal image."""
    global sprite
    sprite = alien
