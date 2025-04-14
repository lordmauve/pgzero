# Expose clock API as a builtin
from . import clock
from . import music
from . import tone
from .actor import Actor
from .storage import storage
from .keyboard import keyboard
from .animation import animate
from .rect import Rect, ZRect
from .loaders import images, sounds
# Removed the former mouse enum import
from .constants import keys, keymods
from .game import exit

# The actual screen will be installed here
from .screen import screen_instance as screen
# Make mouse globally available
from .mouse import mouse_instance as mouse


__all__ = [
    'screen',  # graphics output
    'Actor', 'images',  # graphics
    'sounds', 'music', 'tone',  # sound
    'clock', 'animate',  # timing
    'Rect', 'ZRect',  # geometry
    'keyboard', 'mouse', 'keys', 'keymods',  # input
    'storage',  # persistence
    'exit',
]
