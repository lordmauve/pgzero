from unittest import TestCase
from types import SimpleNamespace
import gc
import weakref

from pgzero.animation import animate
from pgzero import clock


class TestObject:
    """A simple object subclass"""


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

    def test_running(self):
        """Test getting the running attribute."""
        obj = SimpleNamespace()
        anim = animate(obj, duration=2)
        self.assertTrue(anim.running)
        clock.tick(1)
        self.assertTrue(anim.running)
        clock.tick(1.1)  # Add extra time to make sure it's done.
        self.assertFalse(anim.running)

    def test_running_read_only(self):
        """Test that the running attribute is read only."""
        obj = SimpleNamespace()
        anim = animate(obj)

        for running in (False, True):
            with self.assertRaises(AttributeError, msg="can't set attribute"):
                anim.running = running


class AnimationStopTest(TestCase):
    """Tests for stopping animation."""
    attr_start_val = 0
    attr_finish_val = 1
    stop_loop_cnt = 5
    complete_values = (False, True)  # Possible stop(complete) values.

    def setUp(self):
        self.test_obj = SimpleNamespace()

    def _multiple_stop(self, anim, complete, exp_attr_val):
        """Method to reduce code duplication in the test cases."""
        # Stop multiple times to ensure it can be handled.
        for _ in range(self.stop_loop_cnt):
            anim.stop(complete=complete)

            # Animation has stopped and attr updated as expected.
            self.assertFalse(anim.running)
            self.assertEqual(self.test_obj.attr, exp_attr_val)

    def test_stop_after_creation(self):
        """Test stopping an animation right after it is created."""
        for complete in self.complete_values:
            self.test_obj.attr = self.attr_start_val
            exp_attr_val = self.attr_start_val
            anim = animate(self.test_obj, attr=self.attr_finish_val)

            # Animation is running and attr hasn't changed.
            self.assertTrue(anim.running)
            self.assertEqual(self.test_obj.attr, exp_attr_val)

            if complete:
                # The animation will update the attr value when the complete
                # flag is True.
                exp_attr_val = self.attr_finish_val

            self._multiple_stop(anim, complete, exp_attr_val)

    def test_stop_after_tick(self):
        """Test stopping an animation after it has run a bit."""
        anim_duration = 5
        tick_duration = 1

        for complete in self.complete_values:
            self.test_obj.attr = self.attr_start_val
            exp_attr_val = self.attr_start_val
            anim = animate(self.test_obj, duration=anim_duration,
                    attr=self.attr_finish_val)

            # Animation is running and attr hasn't changed.
            self.assertTrue(anim.running)
            self.assertEqual(self.test_obj.attr, exp_attr_val)

            clock.tick(tick_duration)

            # Update the expected value after the tick.
            exp_attr_val = self.attr_finish_val * tick_duration / anim_duration

            # Animation is running and attr updated as expected.
            self.assertTrue(anim.running)
            self.assertEqual(self.test_obj.attr, exp_attr_val)

            if complete:
                # The animation will update the attr value when the complete
                # flag is True.
                exp_attr_val = self.attr_finish_val

            self._multiple_stop(anim, complete, exp_attr_val)

    def test_stop_after_finished(self):
        """Test stopping an animation after it has finished."""
        anim_duration = 1
        tick_duration = 1.1  # Add extra time to make sure it's done.

        for complete in self.complete_values:
            self.test_obj.attr = self.attr_start_val
            exp_attr_val = self.attr_start_val
            anim = animate(self.test_obj, duration=anim_duration,
                    attr=self.attr_finish_val)

            # Animation is running and attr hasn't changed.
            self.assertTrue(anim.running)
            self.assertEqual(self.test_obj.attr, exp_attr_val)

            clock.tick(tick_duration)

            # Update the expected value after the tick.
            exp_attr_val = self.attr_finish_val

            # Animation has stopped and attr updated as expected.
            self.assertFalse(anim.running)
            self.assertEqual(self.test_obj.attr, exp_attr_val)

            self._multiple_stop(anim, complete, exp_attr_val)
