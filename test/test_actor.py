import unittest

import pygame

from pgzero.actor import calculate_anchor, Actor, InvalidScaleException
from pgzero.loaders import set_root, images


TEST_MODULE = "pgzero.actor"
TEST_DISP_W, TEST_DISP_H = (200, 100)


pygame.init()
pygame.display.set_mode((TEST_DISP_W, TEST_DISP_H))


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
        set_root(__file__)

    def assertImagesEqual(self, a, b):
        adata, bdata = (pygame.image.tostring(i, 'RGB') for i in (a, b))

        if adata != bdata:
            raise AssertionError("Images differ")

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
        """The pos of the actor must not drift with continued small rotation."""
        a = Actor('alien', pos=(100.0, 100.0))
        for _ in range(360):
            a.angle += 1.0
        self.assertEqual(a.pos, (100.0, 100.0))

    def test_scaling(self):
        actor = Actor('alien')
        originial_size = actor.size

        # No scaling
        actor.scale = (1, 1)
        self.assertEqual(actor.size, originial_size)

        # Scaling on x-axis only
        actor.scale_x = 2
        self.assertEqual(actor.size, (originial_size[0] * 2, originial_size[1]))

        # Scaling on y-axis only
        actor.scale_y = 2
        self.assertEqual(actor.size, (originial_size[0], originial_size[1] * 2))

        # Scaling down
        actor.scale = (.5, .5)
        self.assertEqual(actor.size, (originial_size[0]/2, originial_size[1]/2))

        # Test scale getters
        self.assertEqual(actor.scale, (actor.scale_x, actor.scale_y))

        # Rotate and then scale
        actor.angle = 90
        actor.scale = (.5, .5)
        self.assertEqual(actor.angle, 90)
        self.assertEqual((actor.width, actor.height), (originial_size[1]/2, originial_size[0]/2))
        self.assertEqual(actor.topleft, (-13, 13))

        # Test rasing exception for invalid scale parameters
        with self.assertRaises(InvalidScaleException) as cm:
            actor.scale = (0, -2)
        self.assertEqual(cm.exception.args[0], 'Invalid scale values. They should be not equal to 0.')

        # Test horizontal flip
        actor.angle = 0
        orig = images.load('alien')
        exp = pygame.transform.flip(orig, True, False)
        actor.scale = (-1, 1)
        self.assertImagesEqual(exp, actor._surf)

        # Test vertical flip
        exp = pygame.transform.flip(orig, False, True)
        actor.scale = (1, -1)
        self.assertImagesEqual(exp, actor._surf)

        # Test horizontal + vertical flip
        exp = pygame.transform.flip(orig, True, True)
        actor.scale = (-1, -1)
        self.assertImagesEqual(exp, actor._surf)

        # Test flip + scaling
        exp = pygame.transform.scale(orig, (orig.get_size()[0]*3, orig.get_size()[1]*2))
        exp = pygame.transform.flip(exp, True, True)
        actor.scale = (-3, -2)
        self.assertImagesEqual(exp, actor._surf)
