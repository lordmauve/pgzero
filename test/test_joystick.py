import unittest

from pgzero.joystick import JoystickManager, GenericJoystick, Joystick

class JoystickTest(unittest.TestCase):
    def setUp(self):
        global joysticks
        # Clears any previous state of the joysticks instance.
        joysticks = JoystickManager()

        # Create two generic joysticks to test with.
        joysticks._sticks[999] = GenericJoystick()
        joysticks._default = 999

        # Setup of the states of both controllers and the union joystick.
        joysticks._press(999, 3)
        joysticks._set_axis(999, 0, -0.5)
        joysticks._set_axis(999, 5, 0)

    def test_never_pressed(self):
        """A button value is false if never pressed."""
        self.assertFalse(joysticks[999].face_left)

    def test_press(self):
        """We can check for depressed buttons."""
        self.assertTrue(joysticks[999].face_right)

    def test_release(self):
        """We can release previously held buttons."""
        joysticks._release(999, 3)
        self.assertFalse(joysticks[999].face_right)

    def test_axis_neutral(self):
        """An axis is in neutral position if it was never used."""
        self.assertEqual(joysticks[999].left_y, 0)
        # Since trigger values are converted, they are checked separately here.
        self.assertEqual(joysticks[999].left_trigger, 0)

    def test_axis_moved(self):
        """We can check for the position of axes."""
        self.assertEqual(joysticks[999].left_x, -0.5)

    def test_axis_trigger_moved(self):
        """Trigger axes report their value correctly."""
        self.assertEqual(joysticks[999].right_trigger, 0.5)

    def test_stick_tuple(self):
        """The state of both stick axes can be gotten with one command."""
        self.assertEqual(joysticks[999].left_stick, (-0.5, 0))

    def test_stick_angle(self):
        """We can get the angle a stick is held at."""
        self.assertEqual(joysticks[999].left_angle, 180)

    def test_stick_angle_None(self):
        """If a stick is centered, the angle reports None."""
        self.assertIsNone(joysticks[999].right_angle)

    def test_name(self):
        """The joysticks name can be gotten."""
        self.assertEqual(joysticks[999].name, "GENERIC PGZERO CONTROLLER")

    def test_guid(self):
        """The joysticks guid can be gotten."""
        self.assertEqual(joysticks[999].guid, "00000000000000000000000000000000")

    def test_iid(self):
        """The joysticks instance ID can be gotten."""
        self.assertEqual(joysticks[999].instance_id, 999)

    def test_simultaneous_inputs(self):
        """With multiple devices, the union stick reports all changes."""
        joysticks._sticks[888] = GenericJoystick()
        joysticks._press(888, 0)
        joysticks._set_axis(888, 4, 1.0)
        joy = joysticks._union_stick

        self.assertTrue(joy.face_up)
        self.assertTrue(joy.face_right)
        self.assertEqual(joy.right_y, 1)
        self.assertEqual(joy.left_x, -0.5)

    def test_joysticks_keys(self):
        """We can get all current instance ids via the joystick managers
        keys."""
        self.assertEqual(tuple(joysticks.keys()), (999, ))

    def test_joysticks_values(self):
        """We can get all Joystick objects from the manager."""
        self.assertIsInstance(tuple(joysticks.values())[0], Joystick)

    def test_joysticks_items(self):
        """We can get both IDs and objects together."""
        i = tuple(joysticks.items())
        self.assertIsInstance(i[0][0], int)
        self.assertIsInstance(i[0][1], Joystick)

    def test_num(self):
        """We can get the number of connected joysticks."""
        self.assertEqual(joysticks.num, 1)

    def test_default(self):
        """We can get the earliest connected controller as a default."""
        self.assertIsInstance(joysticks.get_default(), Joystick)

    def test_last_used(self):
        """We can get a reference to the joystick last accessed."""
        joysticks._sticks[888] = GenericJoystick()
        joysticks._press(888, 0)

        # Since GenericJoysticks always report IID 999, we use a different
        # criteria to check which one is reported as last used.
        self.assertEqual(joysticks.last_used.left_x, 0)

        joysticks._set_axis(999, 1, 0.8)
        self.assertEqual(joysticks.last_used.left_y, 0.8)
