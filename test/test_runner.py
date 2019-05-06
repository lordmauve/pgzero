"""Tests for Pygame Zero's runner system.

This module is also a Pygame Zero game so that we can run it with pgzero.

"""
import sys
import unittest
from pathlib import Path

from pgzero.runner import load_and_run
from pgzero import clock

game_tests = Path(__file__).parent / 'game_tests'


class RunnerTest(unittest.TestCase):
    """Test that we can load and run the current file."""

    def test_run(self):
        """We can load and run a game saved as UTF-8."""
        clock.schedule_unique(sys.exit, 0.05)
        with self.assertRaises(SystemExit):
            load_and_run(str(game_tests / 'utf8.py'))

    def test_import(self):
        """Games can import other modules, which can acccess the builtins."""
        clock.schedule_unique(sys.exit, 0.05)
        with self.assertRaises(SystemExit):
            load_and_run(str(game_tests / 'importing.py'))
