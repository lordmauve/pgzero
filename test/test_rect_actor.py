import unittest

import pygame

from pgzero.actor import Actor
from pgzero.loaders import set_root
from pgzero.rect import Rect

# Check that Actor is compatible with PyGame Rect functions
# Note that though the Rect module also contains ZRect, this has not yet been
# put into use

# All methods that take another Rect, no in place modification:

# pygame.Rect.union 	— 	joins two rectangles into one
# pygame.Rect.contains 	— 	test if one rectangle is inside another
# pygame.Rect.colliderect 	— 	test if two rectangles overlap

# All others (TODO)

# pygame.Rect.union_ip 	— 	joins two rectangles into one, in place
# pygame.Rect.unionall 	— 	the union of many rectangles
# pygame.Rect.unionall_ip 	— 	the union of many rectangles, in place
# pygame.Rect.collidelist 	— 	test if one rectangle in a list intersects
# pygame.Rect.collidelistall 	— 	test if all rectangles in a list intersect
# pygame.Rect.collidedict 	— 	test if one rectangle in a dictionary intersects
# pygame.Rect.collidedictall 	— 	test if all rectangles in a dictionary intersect
#
# Note: as Actor should simply masquerade as a Rect, I'd presume that "in place"
# methods will only modify the other rect *not* the Actor

TEST_MODULE = "pgzero.actor"
TEST_DISP_W, TEST_DISP_H = (500, 500)


class RectActorTestSingularNoIp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        set_root(__file__)
        pygame.init()
        pygame.display.set_mode((TEST_DISP_W, TEST_DISP_H))

    @classmethod
    def tearDownClass(cls):
        pygame.display.quit()

    def setUp(self):
        # the Alien should be 66 x 92 px
        self.actor = Actor('alien', pos=(100, 150), anchor=('left', 'top'))
        self.separate_rect = Rect((0, 20), (20, 300))
        self.overlapping_rect = Rect((120, 100), (100, 100))
        self.enclosed_rect = Rect((110, 160), (10, 10))
        self.enclosing_rect = Rect((0, 0), (500, 500))

    def test_union_separate(self):
        self.assertEquals(
            self.separate_rect.union(self.actor),
            Rect((0, 20), (166, 300))
        )

    def test_union_overlapping(self):
        self.assertEquals(
            self.overlapping_rect.union(self.actor),
            Rect((100, 100), (120, 142))
        )

    def test_union_enclosed(self):
        self.assertEquals(
            self.enclosed_rect.union(self.actor),
            Rect((100, 150), (66, 92))
        )

    def test_contains_true(self):
        self.assertTrue(self.enclosing_rect.contains(self.actor))

    def test_contains_false_overlapping(self):
        self.assertFalse(self.overlapping_rect.contains(self.actor))

    def test_contains_false_enclosed(self):
        self.assertFalse(self.enclosed_rect.contains(self.actor))

    def test_contains_false_separate(self):
        self.assertFalse(self.separate_rect.contains(self.actor))

    def test_collide_rect_true_enclosing(self):
        self.assertTrue(self.enclosing_rect.colliderect(self.actor))

    def test_collide_rect_true_enclosed(self):
        self.assertTrue(self.enclosed_rect.colliderect(self.actor))

    def test_collide_rect_true_overlapping(self):
        self.assertTrue(self.overlapping_rect.colliderect(self.actor))

    def test_collide_rect_false_separate(self):
        self.assertFalse(self.separate_rect.colliderect(self.actor))


if __name__ == "__main__":
    unittest.main()
