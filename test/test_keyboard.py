import unittest
import warnings
from contextlib import contextmanager

from pygame import locals

from pgzero.constants import keys
from pgzero.keyboard import keyboard


@contextmanager
def assert_warning():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        yield
    assert len(w) > 0, \
        "Expected a warning, but no warnings received."


@contextmanager
def assert_no_warning():
    with warnings.catch_warnings(record=True) as w:
        yield
    assert len(w) == 0, \
        "Expected no warnings, but %d warnings received." % len(w)


class KeyboardTest(unittest.TestCase):
    def setUp(self):
        keyboard._press(locals.K_a)
        keyboard._press(locals.K_RIGHT)

    def test_never_pressed(self):
        """A key value is false if never pressed."""
        self.assertFalse(keyboard.q)

    def test_press(self):
        """We can check for depressed keys by enum lookup."""
        with assert_no_warning():
            self.assertTrue(keyboard.a)

    def test_release(self):
        """We can release a previously pressed key."""
        keyboard._release(locals.K_a)
        self.assertFalse(keyboard.a)

    def test_getitem(self):
        """Getting a key press by string lookup works, but warns."""
        with assert_warning():
            self.assertTrue(keyboard['a'])

    def test_getattr_uppercase(self):
        """Uppercase variants of the attribute raise a warning"""
        with assert_warning():
            self.assertTrue(keyboard.A)

    def test_getattr_prefixed(self):
        """Prefixed variants of the attribute names raise a warning"""
        with assert_warning():
            self.assertTrue(keyboard.K_a)

    def test_uppercase_number(self):
        """Uppercase prefixed numbers raise a warning."""
        with assert_warning():
            self.assertFalse(keyboard.K_0)

    def test_getitem_keysenum(self):
        """We can check for depressed keys by enum lookup."""
        with assert_no_warning():
            self.assertTrue(keyboard[keys.A])

    def test_getitem_keysenum_never_pressed(self):
        """We can check for depressed keys by enum lookup."""
        self.assertFalse(keyboard[keys.Q])

    def test_uppercase_constants(self):
        """The uppercase attribute names in the earlier documentation work."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.assertFalse(keyboard.LEFT)
            self.assertTrue(keyboard.RIGHT)

    def test_named_constants(self):
        """The lowercase attribute names work."""
        self.assertFalse(keyboard.left)
        self.assertTrue(keyboard.right)


if __name__ == '__main__':
    unittest.main()
