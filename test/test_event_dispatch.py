import unittest
from unittest.mock import Mock
from pgzero.game import PGZeroGame
from pgzero.constants import mouse


class Event:
    """Mock event."""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class EventDispatchTest(unittest.TestCase):
    def setUp(self):
        self.game = PGZeroGame(Mock())

    def test_dispatch_handler(self):
        """The handler dispatch converts a button value to an enum."""
        presses = []
        h = self.game.prepare_handler(lambda button: presses.append(button))
        h(Event(button=3))  # Right mouse button
        self.assertEqual(presses, [mouse.RIGHT])

    def test_invalid_enum_value(self):
        """Invalid enum values are suppressed (the handler is not called).

        This case exists because Pygame can emit event codes that do not
        correspond to any of its defined constants, in the case of unusual
        mice or unusual keyboard combinations. Because these are edge cases
        we simply drop the event.

        """
        presses = []
        h = self.game.prepare_handler(lambda button: presses.append(True))
        h(Event(button=7))  # Extended mouse button
        self.assertEqual(presses, [])


if __name__ == '__main__':
    unittest.main()
