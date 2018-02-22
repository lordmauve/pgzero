"""We provide a simple default draw() hook to show people what to do next.

We show a logo suitable for the screen size and some tips.

"""
from pkgutil import get_data
from io import BytesIO
from pygame import image
from pygame.transform import smoothscale

from . import __version__
from .clock import clock
from .actor import Actor


# The image resource names to load
IMAGES = [
    'joypad',
]


screen = None  # This will be populated by PGZeroGame
surfaces = {}


def load_image_resource(name):
    """Load a resource from the pgzero data directory."""
    buf = BytesIO(get_data(__name__, 'data/{}.png'.format(name)))
    return image.load(buf)


def init():
    """Called by PGZeroGame if we're going to be installed."""
    for name in IMAGES:
        surfaces[name] = load_image_resource(name)


def draw():
    """Draw the screen."""
    screen.clear()
    centerx = screen.width // 2
    centery = screen.height // 2

    surf = surfaces['joypad']
    jw, jh = surf.get_size()

    maxw = screen.width * 0.9
    maxh = screen.height - 40

    if jw > maxw or jh > maxh:
        scale = min(maxw / jw, maxh / jh)
        jw = round(jw * scale)
        jh = round(jh * scale)
        surf = smoothscale(surf, (jw, jh))

    screen.blit(
        surf,
        (centerx - jw // 2, centery - jh // 2)
    )

    screen.draw.text(
        'Pygame Zero v{}'.format(__version__),
        bottomright=(screen.width - 5, screen.height - 5),
        color=(128, 128, 128),
        fontsize=16,
    )
