import unittest
import pygame
from pgzero.mouse import set_visible

class MouseTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pygame.init()
    def test_set_visible(self):
        set_visible(False)
        self.assertFalse(pygame.mouse.get_visible())
        set_visible(True)
        self.assertTrue(pygame.mouse.get_visible())
