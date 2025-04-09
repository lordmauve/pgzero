import unittest

import pygame

from pgzero.actor import Actor
from pgzero.loaders import set_root


TEST_DISP_W, TEST_DISP_H = (200, 100)


class WebpLoaderTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pygame.init()
        pygame.display.set_mode((TEST_DISP_W, TEST_DISP_H))
        set_root(__file__)

    @classmethod
    def tearDownClass(self):
        pygame.display.quit()

    def test_loader_finds_webp(self):
        actor = Actor("alien_as_webp")

        # Just instantiating the actor shows webp image loading works
        assert actor
