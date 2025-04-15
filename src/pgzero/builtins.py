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
from .constants import mouse, keys, keymods, joybtn, axis
from .game import exit

# The actual screen will be installed here
from .screen import screen_instance as screen
from .joystick import joysticks_instance as joysticks
from .joystick import joy


__all__ = [
    'screen',  # graphics output
    'Actor', 'images',  # graphics
    'sounds', 'music', 'tone',  # sound
    'clock', 'animate',  # timing
    'Rect', 'ZRect',  # geometry
    'keyboard', 'mouse', 'keys', 'keymods',  # input
    'joysticks', 'joy', 'joybtn', 'axis',
    'storage',  # persistence
    'exit',
]
