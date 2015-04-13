from images import alien

TITLE = "Alien walk"
WIDTH = 500
HEIGHT = alien.get_height() + 20


# The rectangle in which the alien will be drawn
alien_rect = alien.get_rect().move((-50, 10))


def draw(screen):
    """Clear the screen and draw the alien."""
    screen.fill((0, 0, 0))
    screen.blit(alien, alien_rect)


def update(dt):
    """Move the alien by one pixel."""
    alien_rect.x += 1

    # If the alien is off the right hand side of the screen,
    # move it back off screen to the left-hand side
    if alien_rect.x > WIDTH:
        alien_rect.x = -100


def on_mouse_down(pos):
    """Detect clicks on the alien."""
    if alien_rect.collidepoint(pos):
        print("You clicked the alien!")
    else:
        print("You missed the alien!")
