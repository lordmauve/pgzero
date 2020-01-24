import sys
import unittest
from pathlib import Path

import numpy as np
import pygame
import pygame.image
import pygame.surfarray

from pgzero.screen import Screen
from pgzero.loaders import set_root, images


class ScreenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialise the display and set loaders to target the current dir."""
        pygame.init()
        cls.surf = pygame.display.set_mode((200, 100))
        set_root(__file__)

    @classmethod
    def tearDownClass(cls):
        """Shut down the display."""
        pygame.display.quit()

    def setUp(self):
        self.screen = Screen(self.surf)
        self.screen.clear()

    def assertImagesAlmostEqual(self, computed, expected):
        """Check that 2 images are approximately equal."""
        comp_surf = pygame.surfarray.array3d(computed)
        exp_surf = pygame.surfarray.array3d(expected)

        if np.allclose(comp_surf, exp_surf, atol=2):
            return

        name = sys._getframe(1).f_code.co_name
        tmpdir = Path(__file__).parent / 'failed-image'
        tmpdir.mkdir(exist_ok=True)
        pygame.image.save(
            computed,
            str(tmpdir / '{}-computed.png'.format(name))
        )
        pygame.image.save(
            expected,
            str(tmpdir / '{}-expected.png'.format(name))
        )

        raise AssertionError(
            "Images differ; saved comparison images to {}".format(tmpdir)
        )

    def test_blit_surf(self):
        """We can blit a surface to the screen."""
        self.screen.blit(images.alien, (0, 0))
        self.assertImagesAlmostEqual(self.surf, images.expected_alien_blit)

    def test_blit_name(self):
        """screen.blit() accepts an image name instead of a Surface."""
        self.screen.blit('alien', (0, 0))
        self.assertImagesAlmostEqual(
            self.screen.surface,
            images.expected_alien_blit
        )

    def test_bounds(self):
        """test that the bounds method is present / works and that the return
        value is minimally correct (top-left should equal 0, bottom-right
        greater than 0)"""
        b = self.screen.bounds()
        self.assertEqual(b.left, 0)
        self.assertEqual(b.top, 0)
        self.assertGreater(b.width, 0)
        self.assertGreater(b.height, 0)

    def test_fill_gradient(self):
        """We can fill the screen with a gradient."""
        self.screen.fill('black', gcolor='blue')
        self.assertImagesAlmostEqual(
            self.screen.surface,
            images.expected_gradient
        )

    def test_line(self):
        yellow = (255, 255, 0)
        """We can draw a line."""
        self.screen.draw.line(start=(0, 50), end=(100, 30), color=yellow, width=9)
        self.assertImagesAlmostEqual(
            self.screen.surface,
            images.expected_line
        )

    def test_line_errors(self):
        """draw.line raises errors as expected."""
        yellow = (255, 255, 0)
        with self.assertRaises(TypeError):
            self.screen.draw.line(2, yellow)
        with self.assertRaises(TypeError):
            self.screen.draw.line([2], yellow)

    def test_circle(self):
        yellow = (255, 255, 0)
        """We can draw a circle."""
        self.screen.draw.circle(pos=(50, 50), radius=50, color=yellow, width=9)
        self.assertImagesAlmostEqual(
            self.screen.surface,
            images.expected_circle
        )

    def test_filled_circle(self):
        yellow = (255, 255, 0)
        """We can draw a filled circle."""
        self.screen.draw.filled_circle(pos=(50, 50), radius=50, color=yellow)
        self.assertImagesAlmostEqual(
            self.screen.surface,
            images.expected_filled_circle
        )

    def test_circle_errors(self):
        """draw.circle raises errors as expected."""
        yellow = (255, 255, 0)
        with self.assertRaises(TypeError):
            self.screen.draw.circle(2, yellow)
        with self.assertRaises(TypeError):
            self.screen.draw.circle([2], yellow)

    def test_polygon(self):
        poly = [(0, 99), (49, 0), (99, 99)]
        yellow = (255, 255, 0)
        """We can draw a polygon."""
        self.screen.draw.polygon(poly, yellow)
        self.assertImagesAlmostEqual(
            self.screen.surface,
            images.expected_polygon
        )

    def test_filled_polygon(self):
        poly = [(0, 99), (49, 0), (99, 99)]
        yellow = (255, 255, 0)
        """We can draw a filled polygon."""
        self.screen.draw.filled_polygon(poly, yellow)
        self.assertImagesAlmostEqual(
            self.screen.surface,
            images.expected_filled_polygon
        )

    def test_polygon_errors(self):
        """draw.polygon raises errors as expected."""
        yellow = (255, 255, 0)
        with self.assertRaises(TypeError):
            self.screen.draw.polygon(2, yellow)
        with self.assertRaises(TypeError):
            self.screen.draw.polygon([2], yellow)

    def test_rect(self):
        yellow = (255, 255, 0)
        """We can draw a rectangle."""
        self.screen.draw.rect(rect=Rect((0, 0), (100, 100)), color=yellow, width=9)
        self.assertImagesAlmostEqual(
            self.screen.surface,
            images.expected_rect
        )

    def test_filled_rect(self):
        yellow = (255, 255, 0)
        """We can draw a filled rectangle."""
        self.screen.draw.filled_rect(rect=Rect((0, 0), (100, 100)), color=yellow)
        self.assertImagesAlmostEqual(
            self.screen.surface,
            images.expected_filled_rect
        )

    def test_rect_errors(self):
        """draw.rect raises errors as expected."""
        yellow = (255, 255, 0)
        with self.assertRaises(TypeError):
            self.screen.draw.rect(2, yellow)
        with self.assertRaises(TypeError):
            self.screen.draw.rect([2], yellow)

    def test_wrapped_gradient_text(self):
        """We can draw wrapped gradient text.

        Relates to issue #165 https://github.com/lordmauve/pgzero/issues/165

        """
        self.screen.draw.text(
            'gradient\ntext',
            (0, 0),
            fontname='eunomia_regular',
            fontsize=18,
            color='red',
            gcolor='blue'
        )
        self.assertImagesAlmostEqual(
            self.screen.surface,
            images.expected_wrapped_gradient_text
        )


if __name__ == '__main__':
    unittest.main()
