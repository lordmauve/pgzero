import unittest
from collections import deque

import pygame

from pgzero.loaders import set_root
from pgzero.mouse import mouse_instance as mouse


class MouseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialise the display and set loaders to target the current dir."""
        pygame.init()
        cls.surf = pygame.display.set_mode((200, 200))
        set_root(__file__)

    @classmethod
    def tearDownClass(cls):
        """Shut down the display."""
        pygame.display.quit()

    def setUp(self):
        mouse._press(mouse.LEFT)
        mouse._press(mouse.MIDDLE)
        mouse._set_pos((10, 10))
        pygame.mouse.set_visible(False)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    def tearDown(self):
        mouse._null_rel()

    def test_never_pressed(self):
        """A button value is false if never pressed."""
        self.assertFalse(mouse.pressed_right)

    def test_press(self):
        """We can check for depressed buttons by property check."""
        self.assertTrue(mouse.pressed_left)

    def test_release(self):
        """We can release a previously pressed key."""
        mouse._release(mouse.LEFT)
        self.assertFalse(mouse.pressed_left)

    def test_get_pressed(self):
        """We can get all button states together."""
        self.assertEqual(mouse.pressed, (True, True, False))

    def test_already_pressed(self):
        """Pressing an already pressed button still works."""
        mouse._press(mouse.LEFT)
        self.assertTrue(mouse.pressed_left)

    def test_already_released(self):
        """Releasing an unpressed button still works."""
        mouse._release(mouse.RIGHT)
        self.assertFalse(mouse.pressed_right)

    def test_release_other(self):
        """Releasing one key does not release any others that are pressed."""
        mouse._release(mouse.LEFT)
        self.assertTrue(mouse.pressed_middle)

    def test_uppercase_constants(self):
        """The uppercase attribute names from earlier in the project still
        work. This is important for backwards compatibility."""
        self.assertEqual(mouse.LEFT, 1)
        self.assertEqual(mouse.MIDDLE, 2)
        self.assertEqual(mouse.RIGHT, 3)
        self.assertEqual(mouse.WHEEL_UP, 4)
        self.assertEqual(mouse.WHEEL_DOWN, 5)

    def test_get_position(self):
        """We get the correct current position of the mouse."""
        self.assertEqual(mouse.pos, (10, 10))

    def test_get_lc_position(self):
        """We can get the last called position."""
        self.assertEqual(mouse.last_called_pos, (0, 0))

    def test_set_position(self):
        """We can change the mouse position."""
        # TODO: Can this be done via mouse.pos = (25, 25)? Problem is that a
        # normal Pygame event would have to be gotten before changes take
        # effect.
        mouse._set_pos((25, 25))
        self.assertEqual(mouse.pos, (25, 25))

    def test_recent_pos(self):
        """Recent positions can be gotten."""
        mouse._recent_pos = deque(maxlen=60)
        # TODO: Can this be done via mouse.pos = (1, 1) etc.? Problem is that a
        # normal Pygame event would have to be gotten before changes take
        # effect.
        mouse._set_pos((1, 1))
        mouse._set_pos((2, 2))
        self.assertEqual(mouse.recent_pos, ((2, 2), (1, 1)))

    def test_recent_pos_max(self):
        """We can change the number of recent positions."""
        mouse.recent_pos_max = 120
        self.assertEqual(mouse._recent_pos.maxlen, 120)

    def test_get_relative(self):
        """We can get the last position change, starting from (10,10)."""
        # TODO: Can this be done via mouse.pos = (5, 5)? Problem is that a
        # normal Pygame event would have to be gotten before changes take
        # effect.
        mouse._add_rel((-5, -5))
        self.assertEqual(mouse.rel, (-5, -5))

    def test_get_lc_relative(self):
        """We can get the last called position change, startig from (0, 0)."""
        # TODO: Can this be done via mouse.pos = (25, 25)? Problem is that a
        # normal Pygame event would have to be gotten before changes take
        # effect.
        mouse._add_rel((25, 25))
        self.assertEqual(mouse.last_called_rel, (25, 25))

    def test_recent_rel(self):
        """Recent position changes can be gotten."""
        mouse._recent_rel = deque(maxlen=60)
        # TODO: Can this be done via mouse.pos = (1, 1) etc.? Problem is that a
        # normal Pygame event would have to be gotten before changes take
        # effect.
        mouse._add_rel((2, 2))
        mouse._add_rel((-1, -1))
        self.assertEqual(mouse.recent_rel, ((-1, -1), (2, 2)))

    def test_recent_rel_max(self):
        """We can change the number of recent position changes."""
        mouse.recent_rel_max = 120
        self.assertEqual(mouse._recent_rel.maxlen, 120)

    def test_get_visibility(self):
        """We can get whether the mouse cursor is visible."""
        self.assertFalse(mouse.visible)

    def test_change_visibility(self):
        """We can change mouse visibility."""
        mouse.visible = True
        self.assertTrue(pygame.mouse.get_visible())

    def test_get_cursor_name(self):
        """We can check the cursor name."""
        self.assertEqual(mouse.cursor_name, "HAND")

    def test_change_cursor(self):
        """We can change the cursor."""
        mouse.cursor = "IBEAM"
        self.assertTrue("IBEAM" in pygame.mouse.get_cursor().__repr__())

    def test_cursor_hotspot(self):
        """We can check the hotspot of the cursor."""
        self.assertIsNone(mouse.cursor_hotspot)
