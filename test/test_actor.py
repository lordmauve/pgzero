import unittest

import pygame

from pgzero.actor import calculate_anchor, Actor
from pgzero.loaders import set_root


TEST_MODULE = "pgzero.actor"
TEST_DISP_W, TEST_DISP_H = (200, 100)


class ModuleTest(unittest.TestCase):
    def test_calculate_anchor_with_float(self):
        self.assertEqual(
            calculate_anchor(1.23, "x", 12345),
            1.23
        )

    def test_calculate_anchor_centre(self):
        self.assertEqual(
            calculate_anchor("center", "x", 100),
            50
        )

    def test_calculate_anchor_bottom(self):
        self.assertEqual(
            calculate_anchor("bottom", "y", 100),
            100
        )


class ActorTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pygame.init()
        pygame.display.set_mode((TEST_DISP_W, TEST_DISP_H))
        set_root(__file__)

    @classmethod
    def tearDownClass(self):
        pygame.display.quit()

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

    def test_setting_multiple_relative_pos_raises_typeerror(self):
        with self.assertRaises(TypeError):
            Actor("alien", topleft=(500, 500), bottomright=(600, 600))

    def test_unexpected_kwargs(self):
        with self.assertRaises(TypeError) as cm:
            Actor("alien", toplift=(0, 0))

        self.assertEqual(
            cm.exception.args[0],
            "Unexpected keyword argument 'toplift' (did you mean 'topleft'?)",
        )

    def test_set_pos_relative_to_anchor(self):
        a = Actor("alien", anchor=(10, 10))
        a.pos = (100, 100)
        self.assertEqual(a.topleft, (90, 90))

    def test_right_angle(self):
        a = Actor("alien")
        self.assertEqual(a.image, "alien")
        self.assertEqual(a.topleft, (0, 0))
        self.assertEqual(a.pos, (33.0, 46.0))
        self.assertEqual(a.width, 66)
        self.assertEqual(a.height, 92)
        a.angle += 90.0
        self.assertEqual(a.angle, 90.0)
        self.assertEqual(a.topleft, (-13, 13))
        self.assertEqual(a.pos, (33.0, 46.0))
        self.assertEqual(a.width, 92)
        self.assertEqual(a.height, 66)

    def test_rotation(self):
        """An actor's pos must not drift with continued small rotation."""
        a = Actor('alien', pos=(100.0, 100.0))
        for _ in range(360):
            a.angle += 1.0
        self.assertEqual(a.pos, (100.0, 100.0))

    def test_opacity_default(self):
        """Ensure opacity is initially set to its default value."""
        a = Actor('alien')

        self.assertEqual(a.opacity, 1.0)

    def test_opacity_value(self):
        """Ensure opacity gives the value it was set to."""
        a = Actor('alien')
        expected_opacity = 0.54321

        a.opacity = expected_opacity

        self.assertEqual(a.opacity, expected_opacity)

    def test_opacity_min_boundry(self):
        """Ensure opacity is not set below minimum allowable level."""
        a = Actor('alien')

        a.opacity = -0.1

        self.assertEqual(a.opacity, 0.0)

    def test_opacity_max_boundry(self):
        """Ensure opacity is not set above maximum allowable level."""
        a = Actor('alien')

        a.opacity = 1.1

        self.assertEqual(a.opacity, 1.0)

    def test_dir_correct(self):
        """Everything returned by dir should be indexable as an attribute."""
        a = Actor("alien")
        for attribute in dir(a):
            a.__getattr__(attribute)

    def test_move_to_angle(self):
        """Ensure moving towards an arbitrary angle works."""
        # We set the anchor to topleft for easier math.
        a = Actor("alien", anchor=("left", "top"))
        # Pythagoras for necessary distance to reach the target point.
        distance = (50**2 + 50**2)**0.5
        a.move_towards_angle(-45, distance)
        # After moving we always have to round to match the int target point.
        # In actual games, having the position be floats is no problem.
        a.pos = (round(a.x), round(a.y))
        self.assertEqual(a.pos, (50, 50))

    def test_move_to_point(self):
        """Ensure moving towards a point works."""
        a = Actor("alien", anchor=("left", "top"))
        position = (50, 50)
        distance = ((50**2 + 50**2)**0.5)/2
        a.move_towards_point(position, distance)
        a.pos = (round(a.x), round(a.y))
        self.assertEqual(a.pos, (25, 25))

    def test_move_to_point_no_overshoot(self):
        """Ensure moving towards point won't overshoot if distance to target
        is smaller than the given distance to move."""
        a = Actor("alien", anchor=("left", "top"))
        position = (10, 10)
        distance = ((50**2 + 50**2)**0.5)/2
        a.move_towards_point(position, distance)
        a.pos = (round(a.x), round(a.y))
        self.assertEqual(a.pos, (10, 10))

    def test_move_to_point_with_overshoot(self):
        """Ensure position overshoots correctly if given the parameter."""
        a = Actor("alien", anchor=("left", "top"))
        position = (10, 10)
        distance = ((50**2 + 50**2)**0.5)/2
        a.move_towards_point(position, distance, overshoot=True)
        a.pos = (round(a.x), round(a.y))
        self.assertEqual(a.pos, (25, 25))

    def test_move_forward(self):
        """Test whether moving forward by the actor angle works."""
        a = Actor("alien", anchor=("left", "top"))
        a.angle = -45
        distance = (50**2 + 50**2)**0.5
        a.move_forward(distance)
        a.pos = (round(a.x), round(a.y))
        self.assertEqual(a.pos, (50, 50))

    def test_move_backward(self):
        """Test whether moving backwards by the actor angle works."""
        a = Actor("alien", anchor=("left", "top"))
        a.angle = 135
        distance = (50**2 + 50**2)**0.5
        a.move_backward(distance)
        a.pos = (round(a.x), round(a.y))
        self.assertEqual(a.pos, (50, 50))

    def test_move_left(self):
        """Test whether moving left by the actor angle works."""
        a = Actor("alien", anchor=("left", "top"))
        a.angle = -135
        distance = (50**2 + 50**2)**0.5
        a.move_left(distance)
        a.pos = (round(a.x), round(a.y))
        self.assertEqual(a.pos, (50, 50))

    def test_move_right(self):
        """Test whether moving right by the actor angle works."""
        a = Actor("alien", anchor=("left", "top"))
        a.angle = 45
        distance = (50**2 + 50**2)**0.5
        a.move_right(distance)
        a.pos = (round(a.x), round(a.y))
        self.assertEqual(a.pos, (50, 50))
