import unittest
from unittest.mock import patch

import pygame

from pgzero.actor import Actor
from pgzero.loaders import set_root


TEST_MODULE = "pgzero.actor"
TEST_DISP_W, TEST_DISP_H = (200, 100)


pygame.init()
pygame.display.set_mode((TEST_DISP_W, TEST_DISP_H))


class ActorTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        set_root(__file__)

    def test_sensible_init_defaults(self):
        a = Actor("alien")

        self.assertEqual(a.image, "alien")
        self.assertEqual(a.topleft, (0, 0))

    def test_setting_absolute_initial_pos(self):
        a = Actor("alien", pos=(100, 200), anchor=("right", "bottom"))

        self.assertEqual(
            a.topleft,
            (100 - a.width, 200 - a.height),
        )

    def test_setting_relative_initial_pos_topleft(self):
        a = Actor("alien", topleft=(500, 500))
        self.assertEqual(a.topleft, (500, 500))

    def test_setting_relative_initial_pos_center(self):
        a = Actor("alien", center=(500, 500))
        self.assertEqual(a.center, (500, 500))

    def test_setting_relative_initial_pos_bottomright(self):
        a = Actor("alien", bottomright=(500, 500))
        self.assertEqual(a.bottomright, (500, 500))

    def test_setting_absolute_pos_and_relative_raises_typeerror(self):
        with self.assertRaises(TypeError):
            Actor("alien", pos=(0, 0), bottomright=(500, 500))

    def test_setting_anchor_and_relative_raises_typeerror(self):
        with self.assertRaises(TypeError):
            Actor("alien", anchor=("left", "bottom"), topleft=(500, 500))

    def test_setting_multiple_relative_pos_raises_typeerror(self):
        with self.assertRaises(TypeError):
            Actor("alien", topleft=(500, 500), bottomright=(600, 600))

    def test_unexpected_kwargs(self):
        with patch("builtins.print") as mock_print:
            Actor("alien", toplift=(0, 0))

        mock_print.assert_called_once_with(
            "Unexpected keyword argument 'toplift', did you mean 'topleft'")
