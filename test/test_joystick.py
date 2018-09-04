import unittest
from unittest.mock import Mock
from pgzero.game import PGZeroGame
from pgzero.constants import joystick


class Event:
    """Mock event."""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class JoystickTest(unittest.TestCase):
    def setUp(self):
        self.game = PGZeroGame(Mock())

    def test_button_press_handler(self):
        """The handler dispatch converts a button value to an enum."""
        presses = []
        h = self.game.prepare_handler(lambda button: presses.append(button))
        h(Event(joy=0, button=3))  # Right mouse button
        self.assertEqual(presses, [joystick.THREE])

        
if __name__ == '__main__':
    unittest.main()
