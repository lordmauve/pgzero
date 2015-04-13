from images import alien

TITLE = "Alien walk"

WIDTH = 500
HEIGHT = alien.get_height() + 20

x = 50


def alien_position():
    """Get the current position of the alien."""
    return (x, 10)


def draw(screen):
    """Clear the screen and draw the alien."""
    screen.fill((0, 0, 0))
    screen.blit(alien, alien_position())


def update(dt):
    """Move the alien by one pixel."""
    global x, HEIGHT
    x += 1
    if x > WIDTH:
        x = -100


def on_mouse_down(pos):
    bounds = alien.get_rect().move(*alien_position())
    if bounds.collidepoint(pos):
        print("You clicked the alien!")
