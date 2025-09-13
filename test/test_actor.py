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

    def test_velocity_starts_at_Zero(self):
        """An Actors velocity starts at zero in both axes."""
        a = Actor("alien")
        self.assertEqual(a.vel, (0, 0))

    def test_velocity_components(self):
        """We can use the Actors velocity by individual components."""
        a = Actor("alien")
        a.vx = 15
        a.vy = -5
        self.assertEqual(a.vx, 15)
        self.assertEqual(a.vy, -5)
        self.assertEqual(a.vel, (15, -5))

    def test_velocity_together(self):
        """We can use the Actors velocity as a tuple."""
        a = Actor("alien")
        a.vel = (15, -5)
        self.assertEqual(a.vx, 15)
        self.assertEqual(a.vy, -5)
        self.assertEqual(a.vel, (15, -5))

    def test_move_by_vel(self):
        """We can move an actor by its velocity."""
        a = Actor("alien", (10, 10))
        a.vel = (15, -5)
        a.move_by_vel()
        self.assertEqual(a.pos, (25, 5))

    def test_interception_velocity(self):
        """We can get a valid interception vector from a starting Actor to
        a moving target Actor."""
        a = Actor("alien", (0, 10))
        b = Actor("alien", (10, 0))
        b.vy = 5
        # Due to floating point inaccuracy, if we simply give 5 as the speed,
        # no intersection will be found even though it should be.
        a.vel = a.intercept_velocity(b, 5.0001)
        # For the same reason, the result must be rounded to compare.
        self.assertEqual((round(a.vx), round(a.vy)), (5, 0))

    def test_no_interception(self):
        """If no valid interception vector exists, None is returned."""
        a = Actor("alien", (0, 10))
        b = Actor("alien", (10, 0))
        b.vy = 5
        v = a.intercept_velocity(b, 1)
        self.assertIsNone(v)
