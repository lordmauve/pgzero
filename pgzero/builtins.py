# Expose clock API as a builtin
from . import clock


def image(name):
    """Load an image from the images directory."""
    from images import load
    return load(name)
