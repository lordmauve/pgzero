import unittest
import pygame
import pygame.image

from pgzero.screen import Screen
from pgzero.loaders import set_root, images

pygame.init()
surf = pygame.display.set_mode((200, 100))


class ScreenTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        set_root(__file__)

    def setUp(self):
        self.screen = Screen(surf)
        self.screen.clear()

    def assertImagesAlmostEqual(self, a, b):
        """Check that 2 images are equal besides 1 bit alpha blending rounding errors"""
        zdata = zip(pygame.image.tostring(a, 'RGB'), pygame.image.tostring(b, 'RGB'))

        for z in zdata:
            if abs(z[0] - z[1]) > 1:
                raise AssertionError("Images differ")

    def test_blit_surf(self):
        """We can blit a surface to the screen."""
        self.screen.blit(images.alien, (0, 0))
        self.assertImagesAlmostEqual(surf, images.expected_alien_blit)

    def test_blit_name(self):
        """screen.blit() accepts an image name instead of a Surface."""
        self.screen.blit('alien', (0, 0))
        self.assertImagesAlmostEqual(self.screen.surface, images.expected_alien_blit)


if __name__ == '__main__':
    unittest.main()
