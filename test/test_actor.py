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

    def test_no_scaling(self):
        actor = Actor('alien')
        originial_size = (actor.width, actor.height)

        actor.scale = 1
        self.assertEqual((actor.width, actor.height), originial_size)

    def test_scale_horizontal(self):
        actor = Actor('alien')
        originial_size = (actor.width, actor.height)

        actor.scale_x = 2
        self.assertEqual((actor.width, actor.height), (originial_size[0] * 2, originial_size[1]))

    def test_scale_vertical(self):
        actor = Actor('alien')
        originial_size = (actor.width, actor.height)

        actor.scale_y = 2
        self.assertEqual((actor.width, actor.height), (originial_size[0], originial_size[1] * 2))

    def test_scale_down(self):
        actor = Actor('alien')
        originial_size = (actor.width, actor.height)

        actor.scale = (.5, .5)
        self.assertEqual((actor.width, actor.height), (originial_size[0]/2, originial_size[1]/2))

    def test_scale_different(self):
        actor = Actor('alien')
        originial_size = (actor.width, actor.height)

        actor.scale = (.5, 3)
        self.assertEqual((actor.width, actor.height), (originial_size[0]/2, originial_size[1]*3))

    def test_scale_from_float(self):
        actor1 = Actor('alien')
        actor2 = Actor('alien')

        actor1.scale = .5
        actor2.scale = (.5, .5)

        self.assertEqual(actor1.width, actor2.width)
        self.assertEqual(actor1.height, actor2.height)

    def test_scaling_on_x_and_y(self):
        actor1 = Actor('alien')
        actor2 = Actor('alien')

        actor1.scale = .5
        actor2.scale_x = .5
        actor2.scale_y = .5

        self.assertEqual(actor1.width, actor2.width)
        self.assertEqual(actor1.height, actor2.height)

    def test_rotate_and_scale(self):
        actor = Actor('alien')
        original_size = (actor.width, actor.height)

        actor.angle = 90
        actor.scale = .5
        self.assertEqual(actor.angle, 90)
        self.assertEqual((actor.width, actor.height), (original_size[1]/2, original_size[0]/2))
        self.assertEqual(actor.topleft, (-13, 13))

    def test_exception_invalid_scale_params(self):
        actor = Actor('alien')

        with self.assertRaises(InvalidScaleException) as cm:
            actor.scale = (0, -2)
        self.assertEqual(cm.exception.args[0], 'Invalid scale values. They should be not equal to 0.')

    def test_exception_invalid_types(self):
        actor = Actor('alien')

        with self.assertRaises(TypeError) as cm:
            actor.scale = ('something', 1)
        self.assertEqual(cm.exception.args[0], 'Invalid type of scale values. Expected "int/ float", got "str".')

    def test_horizontal_flip(self):
        actor = Actor('alien')
        orig = images.load('alien')
        exp = pygame.transform.flip(orig, True, False)

        actor.scale = (-1, 1)
        self.assertImagesEqual(exp, actor._surf)

    def test_vertical_flip(self):
        actor = Actor('alien')
        orig = images.load('alien')

        exp = pygame.transform.flip(orig, False, True)
        actor.scale = (1, -1)
        self.assertImagesEqual(exp, actor._surf)

    def test_flip_both_axes(self):
        actor = Actor('alien')
        orig = images.load('alien')

        exp = pygame.transform.flip(orig, True, True)
        actor.scale = -1
        self.assertImagesEqual(exp, actor._surf)

    def test_flip_and_scale(self):
        actor = Actor('alien')
        orig = images.load('alien')

        exp = pygame.transform.scale(orig, (orig.get_size()[0]*3, orig.get_size()[1]*2))
        exp = pygame.transform.flip(exp, True, True)
        actor.scale = (-3, -2)
        self.assertImagesEqual(exp, actor._surf)
