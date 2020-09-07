from unittest import TestCase
from types import SimpleNamespace
import pygame

from pgzero import joysticks
from pgzero import clock

class JoysticksTest(TestCase):

    def setUp(self):
        joysticks.load_joysticks_types()
        joysticks.load_joy_key_bindings()
        joysticks.build_joystick_mapping()
    
    def tearDown(self):
        pass

    def test_joysticks_0_joy_right_event(self):
        """ pressing first controller joystick right axis event is converted """
        # pressed
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=0, axis=0, value=1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_RIGHT)
        # released
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=0, axis=0, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_RIGHT)

    def test_joysticks_1_joy_right_event(self):
        """ pressing second controller joystick right axis event is converted  """
        # pressed
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=1, axis=0, value=1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_d)
        # released
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=1, axis=0, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_d)

    def test_joysticks_2_joy_right_event(self):
        """ there's no third controller mapped, try joy right """
        # pressed
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=2, axis=0, value=1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertTrue(result is None)
        # released
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=2, axis=0, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertTrue(result is None)

    def test_joysticks_0_joy_left_event(self):
        """ pressing first controller joystick left axis event is converted """
        # pressed
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=0, axis=0, value=-1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_LEFT)
        # released
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=0, axis=0, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_LEFT)

    def test_joysticks_1_joy_left_event(self):
        """ pressing second controller joystick left axis event is converted  """
        # pressed
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=1, axis=0, value=-1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_a)
        # released
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=1, axis=0, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_a)

    def test_joysticks_2_joy_left_event(self):
        """ there's no third controller mapped, try joy left """
        # pressed
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=2, axis=0, value=-1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertTrue(result is None)
        # released
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=2, axis=0, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertTrue(result is None)

    def test_joysticks_0_joy_down_event(self):
        """ pressing first controller joystick down axis event is converted to keyboard down"""
        # pressed
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=0, axis=1, value=1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_DOWN)
        # released
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=0, axis=1, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_DOWN)

    def test_joysticks_1_joy_down_event(self):
        """ pressing second controller joystick down axis event is converted."""
        # pressed
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=1, axis=1, value=1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_s)
        # released
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=1, axis=1, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_s)

    def test_joysticks_2_joy_down_event(self):
        """ there's no third controller mapped, try joy down axis """
        # pressed
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=2, axis=1, value=1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertTrue(result is None)
        # released
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=2, axis=1, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertTrue(result is None)

    def test_joysticks_0_joy_up_event(self):
        """ pressing first controller joystick up axis event is converted """
        # pressed
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=0, axis=1, value=-1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_UP)
        # released
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=0, axis=1, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_UP)

    def test_joysticks_1_joy_up_event(self):
        """ pressing second controller joystick up axis event is converted  """
        # pressed
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=1, axis=1, value=-1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_w)
        # released
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=1, axis=1, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_w)

    def test_joysticks_2_joy_up_event(self):
        """ there's no third controller mapped, try joy up axis """
        # pressed
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=2, axis=1, value=-1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertTrue(result is None)
        # released
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=2, axis=1, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertTrue(result is None)

    def test_joy0_same_axis_sequence_events(self):
        """ press&release first controller joystick left axis, then right axis."""
        # press & release left
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=0, axis=0, value=-1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_LEFT)
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=0, axis=0, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_LEFT)
        # press & release right
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=0, axis=0, value=1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_RIGHT)
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=0, axis=0, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_RIGHT)

    def test_joy1_same_axis_sequence_events(self):
        """ press&release first controller joystick left axis, then right axis."""
        # press & release A
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=1, axis=0, value=-1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_a)
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=1, axis=0, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_a)
        # press & release D
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=1, axis=0, value=1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_d)
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=1, axis=0, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_d)

    def test_joy0_diff_axis_sequence_events(self):
        """ pressing second controller joystick up axis event is converted  """
        # press left&down
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=0, axis=0, value=-1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_LEFT)
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=0, axis=1, value=1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_DOWN)
        # release down&left
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=0, axis=1, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_DOWN)
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=0, axis=0, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_LEFT)

    def test_joy1_diff_axis_sequence_events(self):
        """ pressing second controller joystick up axis event is converted  """
        # press left&down
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=1, axis=0, value=-1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_a)
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=1, axis=1, value=1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_s)
        # release down&left
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=1, axis=1, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_s)
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=1, axis=0, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_a)

    def test_joy0_mix_axis_button_sequence_events(self):
        # press LEFT and SPACE
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=0, axis=0, value=-1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_LEFT)
        event = pygame.event.Event(pygame.JOYBUTTONDOWN, joy=0, button=3)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_SPACE)
        # release LEFT and SPACE
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=0, axis=0, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_LEFT)
        event = pygame.event.Event(pygame.JOYBUTTONUP, joy=0, button=3)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_SPACE)

    def test_joy1_mix_axis_button_sequence_events(self):
        # press A and ENTER
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=1, axis=0, value=-1)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_a)
        event = pygame.event.Event(pygame.JOYBUTTONDOWN, joy=1, button=3)
        result = joysticks.map_joy_event_key_down(event)
        self.assertEqual(result, pygame.K_RETURN)
        # release A and ENTER
        event = pygame.event.Event(pygame.JOYAXISMOTION, joy=1, axis=0, value=0)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_a)
        event = pygame.event.Event(pygame.JOYBUTTONUP, joy=1, button=3)
        result = joysticks.map_joy_event_key_up(event)
        self.assertEqual(result, pygame.K_RETURN)