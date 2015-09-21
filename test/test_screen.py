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
        surf.fill((0, 0, 0))
        self.screen = Screen(surf)

    def assertImagesEqual(self, a, b):
        adata, bdata = (pygame.image.tostring(i, 'RGB') for i in (a, b))

        if adata != bdata:
            raise AssertionError("Images differ")

    def test_blit_surf(self):
        """We can blit a surface to the screen."""
        self.screen.blit(images.alien, (0, 0))
        self.assertImagesEqual(surf, images.expected_alien_blit)

    def test_blit_name(self):
        """screen.blit() accepts an image name instead of a Surface."""
        self.screen.blit('alien', (0, 0))
        self.assertImagesEqual(surf, images.expected_alien_blit)


if __name__ == '__main__':
    unittest.main()
