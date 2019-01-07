from unittest import TestCase
from types import SimpleNamespace
import gc
import weakref

from pgzero.animation import animate
from pgzero import clock


class TestObject:
    """A simple object subclass"""


class AnimationTest(TestCase):
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

    def test_no_linger(self):
        """Test that deleted animations are garbage-collected"""
        anim1_alivelist = ['animation 1 alive']
        anim2_alivelist = ['animation 2 alive']
        obj_alivelist = ['object alive']
        # cannot use SimpleNamespace because it doesn't support weakref
        obj = TestObject()
        obj.attribute = 0
        anim1 = animate(obj, attribute=1, duration=5)
        anim2 = animate(obj, attribute=2, duration=1)
        weakref.finalize(anim1, anim1_alivelist.clear)
        weakref.finalize(anim2, anim2_alivelist.clear)
        weakref.finalize(obj, obj_alivelist.clear)

        del anim1
        del anim2
        del obj
        gc.collect()
        self.assertEqual(anim1_alivelist, [])

        clock.tick(3)
        gc.collect()
        self.assertEqual(anim2_alivelist, [])
        self.assertEqual(obj_alivelist, [])

    def test_running_after_animation_creation(self):
        """Ensure the running attribute is True on creation."""
        anim = animate(None)

        self.assertTrue(anim.running)

    def test_running_before_animation_finished(self):
        """Ensure the running attribute is True before animation finished."""
        anim = animate(None, duration=2)

        clock.tick(1)

        self.assertTrue(anim.running)

    def test_running_after_animation_finished(self):
        """Ensure the running attribute is False after animation finished."""
        anim = animate(None, duration=2)
        clock.tick(1)

        clock.tick(1.1)  # Add extra time to ensure it's done.

        self.assertFalse(anim.running)

    def test_running_read_only(self):
        """Ensure the running attribute is read only."""
        anim = animate(None)

        with self.assertRaises(AttributeError, msg="can't set attribute"):
            anim.running = False

    def test_stop_with_complete_false_after_creation(self):
        """Stop, with complete False, an animation after creation."""
        attr_start_val = 0
        attr_finish_val = 1
        test_obj = SimpleNamespace(attr=attr_start_val)
        anim = animate(test_obj, attr=attr_finish_val)
        expected_attr_val = attr_start_val

        anim.stop(complete=False)

        # Ensure animation stopped and attr as expected.
        self.assertFalse(anim.running)
        self.assertEqual(test_obj.attr, expected_attr_val)

    def test_stop_with_complete_true_after_creation(self):
        """Stop, with complete True, an animation after creation."""
        attr_start_val = 0
        attr_finish_val = 1
        test_obj = SimpleNamespace(attr=attr_start_val)
        anim = animate(test_obj, attr=attr_finish_val)
        expected_attr_val = attr_finish_val

        anim.stop(complete=True)

        # Ensure animation stopped and attr as expected.
        self.assertFalse(anim.running)
        self.assertEqual(test_obj.attr, expected_attr_val)

    def test_stop_with_complete_false_after_stopped(self):
        """Stop, with complete False, an animation that is already stopped."""
        attr_start_val = 0
        attr_finish_val = 1
        test_obj = SimpleNamespace(attr=attr_start_val)
        anim = animate(test_obj, attr=attr_finish_val)
        anim.stop(complete=False)
        expected_attr_val = attr_start_val

        anim.stop(complete=False)

        # Ensure animation stopped and attr as expected.
        self.assertFalse(anim.running)
        self.assertEqual(test_obj.attr, expected_attr_val)

    def test_stop_with_complete_true_after_stopped(self):
        """Stop, with complete True, an animation that is already stopped."""
        attr_start_val = 0
        attr_finish_val = 1
        test_obj = SimpleNamespace(attr=attr_start_val)
        anim = animate(test_obj, attr=attr_finish_val)
        anim.stop(complete=True)
        expected_attr_val = attr_finish_val

        anim.stop(complete=True)

        # Ensure animation stopped and attr as expected.
        self.assertFalse(anim.running)
        self.assertEqual(test_obj.attr, expected_attr_val)

    def test_stop_with_complete_false_after_finished(self):
        """Stop, with complete False, an animation after it has finished."""
        attr_start_val = 0
        attr_finish_val = 1
        anim_duration = 1.0
        test_obj = SimpleNamespace(attr=attr_start_val)
        anim = animate(test_obj, duration=anim_duration, attr=attr_finish_val)
        clock.tick(anim_duration + 0.1)  # Add extra time to ensure it's done.
        expected_attr_val = attr_finish_val

        anim.stop(complete=False)

        # Ensure animation stopped and attr as expected.
        self.assertFalse(anim.running)
        self.assertEqual(test_obj.attr, expected_attr_val)

    def test_stop_with_complete_true_after_finished(self):
        """Stop, with complete True, an animation after it has finished."""
        attr_start_val = 0
        attr_finish_val = 1
        anim_duration = 1.0
        test_obj = SimpleNamespace(attr=attr_start_val)
        anim = animate(test_obj, duration=anim_duration, attr=attr_finish_val)
        clock.tick(anim_duration + 0.1)  # Add extra time to ensure it's done.
        expected_attr_val = attr_finish_val

        anim.stop(complete=True)

        # Ensure animation stopped and attr as expected.
        self.assertFalse(anim.running)
        self.assertEqual(test_obj.attr, expected_attr_val)

    def test_stop_with_complete_false_after_running(self):
        """Stop, with complete False, an animation after it has run a bit."""
        attr_start_val = 0
        attr_finish_val = 1
        anim_duration = 5.0
        tick_duration = 1.0
        test_obj = SimpleNamespace(attr=attr_start_val)
        anim = animate(test_obj, duration=anim_duration, attr=attr_finish_val)
        clock.tick(tick_duration)
        expected_attr_val = attr_finish_val * tick_duration / anim_duration

        anim.stop(complete=False)

        # Ensure animation stopped and attr as expected.
        self.assertFalse(anim.running)
        self.assertEqual(test_obj.attr, expected_attr_val)

    def test_stop_with_complete_true_after_running(self):
        """Stop, with complete True, an animation after it has run a bit."""
        attr_start_val = 0
        attr_finish_val = 1
        anim_duration = 5.0
        tick_duration = 1.0
        test_obj = SimpleNamespace(attr=attr_start_val)
        anim = animate(test_obj, duration=anim_duration, attr=attr_finish_val)
        clock.tick(tick_duration)
        expected_attr_val = attr_finish_val

        anim.stop(complete=True)

        # Ensure animation stopped and attr as expected.
        self.assertFalse(anim.running)
        self.assertEqual(test_obj.attr, expected_attr_val)

