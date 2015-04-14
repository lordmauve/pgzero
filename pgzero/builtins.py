# Expose clock API as a builtin
from . import clock
from .actor import Actor


def image(name):
    """Load an image from the images directory."""
    from images import load
    return load(name)
