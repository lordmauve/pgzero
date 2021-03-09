from unittest import TestCase
from types import SimpleNamespace

from pgzero.animation import animate
from pgzero import clock

class AnimationImageTest(TestCase):
    def test_clock_animation(self):
        """Test that animation scheduled via the clock works"""
        obj = SimpleNamespace()
        obj.image = 'img1'

        animate.images(obj, ['img1', 'img2'], every=2, source='clock')

        self.assertEqual(obj.image, 'img1')
        clock.tick(1)
        self.assertEqual(obj.image, 'img1')
        clock.tick(1)
        self.assertEqual(obj.image, 'img2')
        clock.tick(1)
        self.assertEqual(obj.image, 'img2')
        clock.tick(1)
        # The value cycles back around
        self.assertEqual(obj.image, 'img1')

    def test_actor_x_y_animation(self):
        """Test that animation of actor_x and actor_y works"""
        obj1 = SimpleNamespace()
        obj1.image = 'img1'
        obj1.x = 40
        obj2 = SimpleNamespace()
        obj2.image = 'img1'
        obj2.y = 40

        animate.images(obj1, ['img1', 'img2'], every=2, source='actor_x')
        animate.images(obj2, ['img1', 'img2'], every=2, source='actor_y')
        self.assertEqual(obj1.image, 'img1')
        self.assertEqual(obj2.image, 'img1')

        obj1.x = 41
        obj2.y = 42
        clock.tick(1)
        self.assertEqual(obj1.image, 'img1')
        self.assertEqual(obj2.image, 'img2')
        obj1.x = 42
        clock.tick(1)
        self.assertEqual(obj1.image, 'img2')
        self.assertEqual(obj2.image, 'img2')
        obj1.x = 44
        obj2.y = 44
        clock.tick(1)
        # The value cycles back around
        self.assertEqual(obj1.image, 'img1')
        self.assertEqual(obj2.image, 'img1')
