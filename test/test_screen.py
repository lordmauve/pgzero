import sys
import unittest
import pygame
import pygame.image
import numpy as np
from pathlib import Path

from pgzero.screen import Screen
from pgzero.loaders import set_root, images

pygame.init()
surf = pygame.display.set_mode((200, 100))


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

        if np.allclose(comp_surf, exp_surf, atol=7):
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
        self.assertImagesAlmostEqual(surf, images.expected_alien_blit)

    def test_blit_name(self):
        """screen.blit() accepts an image name instead of a Surface."""
        self.screen.blit('alien', (0, 0))
        self.assertImagesAlmostEqual(surf, images.expected_alien_blit)


if __name__ == '__main__':
    unittest.main()
