import unittest
import tempfile
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

        if np.allclose(comp_surf, exp_surf, atol=1):
            return

        tmpdir = Path(tempfile.mkdtemp())
        pygame.image.save(computed, str(tmpdir / 'computed.png'))
        pygame.image.save(expected, str(tmpdir / 'expected.png'))

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
        self.assertImagesAlmostEqual(self.screen.surface, images.expected_alien_blit)

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


if __name__ == '__main__':
    unittest.main()
