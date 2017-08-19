from unittest import TestCase
from types import SimpleNamespace

from pgzero.animation import animate
from pgzero import clock


class SuggestionTest(TestCase):
    def test_basic_animation(self):
        """Test that animation works"""
        obj = SimpleNamespace()
        obj.attribute = 0
        animate(obj, attribute=2, duration=2)
        self.assertEqual(obj.attribute, 0)
        clock.tick(1)
        self.assertEqual(obj.attribute, 1)
        clock.tick(1)
        self.assertEqual(obj.attribute, 2)
        clock.tick(1)
        self.assertEqual(obj.attribute, 2)

    def test_some_tween(self):
        """Test that tweening does something"""
        obj = SimpleNamespace()
        obj.attribute = 0
        animate(obj, attribute=2, tween='accelerate', duration=2)
        self.assertEqual(obj.attribute, 0)
        clock.tick(1)
        assert 0 < obj.attribute < 1
        clock.tick(1)
        self.assertEqual(obj.attribute, 2)
        clock.tick(1)
        self.assertEqual(obj.attribute, 2)

    def test_tuple_animation(self):
        """Test that you can animate a tuple"""
        obj = SimpleNamespace()
        obj.attribute = 0, 2
        animate(obj, attribute=(2, 0), duration=2)
        self.assertEqual(obj.attribute, (0, 2))
        clock.tick(1)
        self.assertEqual(obj.attribute, (1, 1))
        clock.tick(1)
        self.assertEqual(obj.attribute, (2, 0))
        clock.tick(1)
        self.assertEqual(obj.attribute, (2, 0))

    def test_list_animation(self):
        """Test that you can animate a list"""
        obj = SimpleNamespace()
        obj.attribute = [0, 2]
        animate(obj, attribute=[2, 0], duration=2)
        self.assertEqual(obj.attribute, [0, 2])
        clock.tick(1)
        self.assertEqual(obj.attribute, [1, 1])
        clock.tick(1)
        self.assertEqual(obj.attribute, [2, 0])
        clock.tick(1)
        self.assertEqual(obj.attribute, [2, 0])

    def test_on_finished(self):
        """Test the on_finished callback works"""
        obj = SimpleNamespace()
        obj.attribute = 0
        endlist = ['in progress']
        animate(obj, attribute=2, duration=2, on_finished=endlist.clear)
        self.assertEqual(obj.attribute, 0)
        self.assertEqual(endlist, ['in progress'])
        clock.tick(1)
        self.assertEqual(obj.attribute, 1)
        self.assertEqual(endlist, ['in progress'])
        clock.tick(1)
        self.assertEqual(obj.attribute, 2)
        clock.tick(1)
        self.assertEqual(obj.attribute, 2)
        self.assertEqual(endlist, [])

    def test_cancel_old(self):
        """Test an old animation is cancelled when overwritten"""
        obj = SimpleNamespace()
        obj.attribute = 0
        animate(obj, attribute=-4, duration=4)
        animate(obj, attribute=2, duration=2)
        self.assertEqual(obj.attribute, 0)
        clock.tick(1)
        self.assertEqual(obj.attribute, 1)
        clock.tick(1)
        self.assertEqual(obj.attribute, 2)
        clock.tick(1)
        self.assertEqual(obj.attribute, 2)

    def test_cancel_some(self):
        """Test only the overwritten target of an old animation is cancelled"""
        obj = SimpleNamespace()
        obj.attr1 = 0
        obj.attr2 = 0
        animate(obj, attr1=-4, attr2=-4, duration=4)
        animate(obj, attr1=2, duration=2)
        self.assertEqual(obj.attr1, 0)
        self.assertEqual(obj.attr2, 0)
        clock.tick(1)
        self.assertEqual(obj.attr1, 1)
        self.assertEqual(obj.attr2, -1)
        clock.tick(1)
        self.assertEqual(obj.attr1, 2)
        self.assertEqual(obj.attr2, -2)
        clock.tick(1)
        self.assertEqual(obj.attr1, 2)
        self.assertEqual(obj.attr2, -3)
