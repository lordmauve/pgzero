# Expose clock API as a builtin
from . import clock
from . import music
from . import tone
from .actor import Actor
from .keyboard import keyboard
from .gamepad import gamepad_1
from .gamepad import gamepad_2
from .gamepad import gamepad
from .animation import animate
from .rect import Rect, ZRect

from .loaders import images, sounds

from .constants import mouse, keys, keymods

from .game import exit
