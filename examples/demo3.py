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


def update(dt):
    """Move the alien by one pixel."""
    alien_rect.x += 1

    # If the alien is off the right hand side of the screen,
    # move it back off screen to the left-hand side
    if alien_rect.x > WIDTH:
        alien_rect.x = -100


def on_mouse_down(pos):
    """Detect clicks on the alien."""
    global sprite
    if alien_rect.collidepoint(pos):
        set_alien_hurt()


def set_alien_hurt():
    global sprite
    sprite = alien_hurt
    unschedule(set_alien_normal)
    schedule(set_alien_normal, 1.0)


def set_alien_normal():
    global sprite
    sprite = alien
