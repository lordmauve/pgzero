import pygame
from collections import namedtuple
from enum import IntEnum
from . import clock


# Since controllers map different buttons to the SDL provided
# button layer numbers, we have enums for each supported
# controller type mapping generic button identifiers to the
# specific button indices used.
class SwitchBtns(IntEnum):
    NUM = 15
    FU = 2
    FD = 1
    FL = 3
    FR = 0
    DU = 11
    DD = 12
    DL = 13
    DR = 14
    LB = 9
    RB = 10
    LP = 7
    RP = 8
    CL = 4
    CM = 5
    CR = 6


# Same goes for the axis.
class SwitchAxis(IntEnum):
    NUM = 6
    LX = 0
    LY = 1
    LT = 4
    RX = 2
    RY = 3
    RT = 5


class X360Btns(IntEnum):
    NUM = 15
    FU = 3
    FD = 0
    FL = 2
    FR = 1
    DU = 11  # The D-Pad mappings are fake, as the Xbox treats the D-Pad like
    DD = 12  # a hat switch. It acting like normal buttons is a simulation
    DL = 13  # by PGZero to make it easier to work with.
    DR = 14  # This is the last fake button.
    LB = 4
    RB = 5
    LP = 8
    RP = 9
    CL = 6
    CM = 10
    CR = 7


class X360Axis(IntEnum):
    NUM = 6
    LX = 0
    LY = 1
    LT = 2
    RX = 3
    RY = 4
    RT = 5


class XSeriesBtns(IntEnum):
    NUM = 20
    FU = 4
    FD = 0
    FL = 3
    FR = 1
    DU = 16  # Simulated D-Pad like with the Xbox controller.
    DD = 17
    DL = 18
    DR = 19
    LB = 6
    RB = 7
    LP = 13
    RP = 14
    CL = 10
    CM = 15
    CR = 11


class XSeriesAxis(IntEnum):
    NUM = 6
    LX = 0
    LY = 1
    LT = 5
    RX = 2
    RY = 3
    RT = 4


class PS4Btns(IntEnum):
    NUM = 15
    FU = 3
    FD = 0
    FL = 2
    FR = 1
    DU = 11
    DD = 12
    DL = 13
    DR = 14
    LB = 9
    RB = 10
    LP = 7
    RP = 8
    CL = 4
    CM = 5
    CR = 6


class PS4Axis(IntEnum):
    NUM = 6
    LX = 0
    LY = 1
    LT = 4
    RX = 2
    RY = 3
    RT = 5


class PS5Btns(IntEnum):
    NUM = 17
    FU = 3
    FD = 0
    FL = 2
    FR = 1
    DU = 13  # Simulated D-Pad like with the Xbox controller.
    DD = 14
    DL = 15
    DR = 16
    LB = 4
    RB = 5
    LP = 11
    RP = 12
    CL = 8
    CM = 10
    CR = 9


class PS5Axis(IntEnum):
    NUM = 6
    LX = 0
    LY = 1
    LT = 2
    RX = 3
    RY = 4
    RT = 5


BTN_NAMES = ("face_up", "face_down", "face_left", "face_right", "dpad_up",
             "dpad_down", "dpad_left", "dpad_right", "shoulder_left",
             "shoulder_right", "push_left", "push_right", "center_left",
             "center_middle", "center_right")
PressedBtns = namedtuple("PressedBtns", BTN_NAMES)


class Joystick:
    """PGZero wrapper class for joystick use."""

    def __init__(self, stick):
        self._stick = stick
        name = self._stick.get_name()
        print(name)
        # We use the system name of the controller to determine
        # the correct mappings to use.
        if "Series" in name:
            self._type = "XSeries"
            self._btn_map = XSeriesBtns
            self._axis_map = XSeriesAxis
        elif "Xbox" in name:
            self._type = "Xbox"
            self._btn_map = X360Btns
            self._axis_map = X360Axis
        elif "PS4" in name:
            self._type = "PS4"
            self._btn_map = PS4Btns
            self._axis_map = PS4Axis
        elif "Sony Interactive" in name:
            self._type = "PS5"
            self._btn_map = PS5Btns
            self._btn_map = PS5Axis
        elif "Switch" in name:
            self._type = "Switch"
            self._btn_map = SwitchBtns
            self._axis_map = SwitchAxis
        else:
            self._type = "UNKNOWN"
            # If the type is unknown, we fall back to Xbox
            # mappings since these are most common among
            # generic controller layouts.
            self._btn_map = X360Btns
            self._axis_map = X360Axis

        self._pressed = [False] * self._btn_map.NUM
        self._axis = [0] * self._axis_map.NUM
        # Since triggers don't start centered but rather unpressed,
        # their starting values are -1.
        self._axis[self._axis_map.RT] = -1
        self._axis[self._axis_map.LT] = -1

        # These variables are used to give a lockout time for physical
        # HAT button simulation to prevent ghost inputs.
        self._DU_open = True
        self._DD_open = True
        self._DL_open = True
        self._DR_open = True

    # Used with clock.schedule to prevent ghost button presses via timeouts.
    def _unlock_DU(self):
        self._DU_open = True

    def _unlock_DD(self):
        self._DD_open = True

    def _unlock_DL(self):
        self._DL_open = True

    def _unlock_DR(self):
        self._DR_open = True

    @property
    def instance_id(self):
        """Returns the instance id of the controller."""
        return self._stick.get_instance_id()

    @property
    def pressed(self):
        """Returns a named tuple with the current pressed state
        of all buttons on the controller."""
        btns = iter(self._btn_map)
        next(btns)
        states = []
        for b in btns:
            states.append(self._pressed[b])
        return PressedBtns(*states)

    @property
    def face_up(self):
        """Returns whether the upper face button is pressed."""
        return self._pressed[self._btn_map.FU]
    fu = face_up

    @property
    def face_down(self):
        """Returns whether the lower face button is pressed."""
        return self._pressed[self._btn_map.FD]
    fd = face_down

    @property
    def face_left(self):
        """Returns whether the left face button is pressed."""
        return self._pressed[self._btn_map.FL]
    fl = face_left

    @property
    def face_right(self):
        """Returns whether the right face button is pressed."""
        return self._pressed[self._btn_map.FR]
    fr = face_right

    @property
    def dpad_up(self):
        """Returns whether the dpad up button is pressed."""
        return self._pressed[self._btn_map.DU]
    du = dpad_up

    @property
    def dpad_down(self):
        """Returns whether the dpad down button is pressed."""
        return self._pressed[self._btn_map.DD]
    dd = dpad_down

    @property
    def dpad_left(self):
        """Returns whether the dpad left button is pressed."""
        return self._pressed[self._btn_map.DL]
    dl = dpad_left

    @property
    def dpad_right(self):
        """Returns whether the dpad right button is pressed."""
        return self._pressed[self._btn_map.DR]
    dr = dpad_right

    @property
    def shoulder_left(self):
        """Returns whether the left shoulder button is pressed."""
        return self._pressed[self._btn_map.LB]
    sl = shoulder_left

    @property
    def shoulder_right(self):
        """Returns whether the right shoulder button is pressed."""
        return self._pressed[self._btn_map.RB]
    sr = shoulder_right

    @property
    def push_left(self):
        """Returns whether the left stick is pressed in."""
        return self._pressed[self._btn_map.LP]
    pl = push_left

    @property
    def push_right(self):
        """Returns whether the right stick is pressed in."""
        return self._pressed[self._btn_map.RP]
    pr = push_right

    @property
    def center_left(self):
        """Returns whether the left center button is pressed."""
        return self._pressed[self._btn_map.CL]
    cl = center_left

    @property
    def center_middle(self):
        """Returns whether the middle center button is pressed."""
        return self._pressed[self._btn_map.CM]
    cm = center_middle

    @property
    def center_right(self):
        """Returns whether the right center button is pressed."""
        return self._pressed[self._btn_map.CR]
    cr = center_right

    @property
    def left_stick(self):
        """Returns a tuple of the axis values for the left stick."""
        return self._axis[self._axis_map.LX], self._axis[self._axis_map.LY]
    ls = left_stick

    @property
    def left_angle(self):
        """Returns the angle the left stick is held to or None if it is
        centered."""
        if self.left_stick == (0, 0):
            return None
        _, p = pygame.math.Vector2(self.left_stick).as_polar()
        degrees = (360 - p) % 360
        return degrees
    la = left_angle

    @property
    def left_x(self):
        """Returns a single axis value for left-right movement of
        the left stick."""
        return self._axis[self._axis_map.LX]
    lx = left_x

    @property
    def left_y(self):
        """Returns a single axis value for up-down movement of
        the left stick."""
        return self._axis[self._axis_map.LY]
    ly = left_y

    @property
    def left_trigger(self):
        """Returns the axis value for the left trigger.
        Since triggers are monodirectional, their value ranges
        are recalculated from [-1, 1] to [0, 1] to represent them
        being depressed."""
        return (self._axis[self._axis_map.LT] + 1) / 2
    lt = left_trigger

    @property
    def right_stick(self):
        """Returns a tuple of the axis values for the right stick."""
        return self._axis[self._axis_map.RX], self._axis[self._axis_map.RY]
    rs = right_stick

    @property
    def right_angle(self):
        """Returns the angle the right stick is held to or None if it is
        centered."""
        if self.right_stick == (0, 0):
            return None
        _, p = pygame.math.Vector2(self.right_stick).as_polar()
        degrees = (360 - p) % 360
        return degrees
    ra = right_angle

    @property
    def right_x(self):
        """Returns a single axis value for left-right movement of
        the right stick."""
        return self._axis[self._axis_map.RX]
    rx = right_x

    @property
    def right_y(self):
        """Returns a single axis value for up-down movement of
        the right stick."""
        return self._axis[self._axis_map.RY]
    ry = right_y

    @property
    def right_trigger(self):
        """Returns the axis value for the right trigger.
        Since triggers are monodirectional, their value ranges
        are recalculated from [-1, 1] to [0, 1] to represent them
        being depressed."""
        return (self._axis[self._axis_map.RT] + 1) / 2
    rt = right_trigger


class JoystickManager:
    """Interface to pygame joystick support. Holds all active joysticks
    and modifies their states based on pygame events."""

    def __init__(self):
        self._sticks = {}
        self._default = None
        self._deadzone = 0.05

    def _press(self, iid, button):
        s = self._sticks[iid]
        s._pressed[button] = True

    def _release(self, iid, button):
        s = self._sticks[iid]
        s._pressed[button] = False

    def _set_axis(self, iid, axis, value):
        """Sets the axis value of a stick or trigger. Enforces the set
        deadzone to prevent jittery results from slightly drifting or
        uncentered sticks."""
        s = self._sticks[iid]
        ax = s._axis_map(axis).name
        if ax == "LT" or ax == "RT":
            if value < -1 + self._deadzone:
                s._axis[axis] = -1
            elif value > 1 - self._deadzone:
                s._axis[axis] = 1
            else:
                s._axis[axis] = value
        elif value > self._deadzone or value < self._deadzone * -1:
            s._axis[axis] = value
        else:
            s._axis[axis] = 0

    def _convert_hat(self, iid, hat, value):
        """Takes the values of a joystick HAT event and simulates
        button down and button up events for corresponding Dpad buttons.
        This is necessary to have consistent behaviour across
        gamepads that use HATs with those that don't."""
        s = self._sticks[iid]
        vx, vy = value[0], value[1]
        pressed = []
        released = []

        # TODO: Better way to do this?
        if vx == 1:
            # If the physical controller has a HAT, moving it to the diagonal
            # can sometimes give repeated joy down events for a single button
            # instance. To prevent this, a lockout of 0.05 seconds is enforced
            # after shifting each simulated Dpad button before it can be
            # accessed again.
            if not s.dr and s._DR_open:
                pressed.append(s._btn_map.DR)
                s._DR_open = False
                clock.schedule(s._unlock_DR, 0.05)
            if s.dl and s._DL_open:
                released.append(s._btn_map.DL)
                s._DL_open = False
                clock.schedule(s._unlock_DL, 0.05)
        elif vx == 0:
            if s.dr and s._DR_open:
                released.append(s._btn_map.DR)
                s._DR_open = False
                clock.schedule(s._unlock_DR, 0.05)
            if s.dl and s._DL_open:
                released.append(s._btn_map.DL)
                s._DL_open = False
                clock.schedule(s._unlock_DL, 0.05)
        elif vx == -1:
            if not s.dl and s._DL_open:
                pressed.append(s._btn_map.DL)
                s._DL_open = False
                clock.schedule(s._unlock_DL, 0.05)
            if s.dr and s._DR_open:
                pressed.append(s._btn_map.DR)
                s._DR_open = False
                clock.schedule(s._unlock_DR, 0.05)

        if vy == 1:
            if not s.du and s._DU_open:
                pressed.append(s._btn_map.DU)
                s._DU_open = False
                clock.schedule(s._unlock_DU, 0.05)
            if s.dd and s._DD_open:
                released.append(s._btn_map.DD)
                s._DD_open = False
                clock.schedule(s._unlock_DD, 0.05)
        elif vy == 0:
            if s.du and s._DU_open:
                released.append(s._btn_map.DU)
                s._DU_open = False
                clock.schedule(s._unlock_DU, 0.05)
            if s.dd and s._DD_open:
                released.append(s._btn_map.DD)
                s._DD_open = False
                clock.schedule(s._unlock_DD, 0.05)
        elif vy == -1:
            if not s.dd and s._DD_open:
                pressed.append(s._btn_map.DD)
                s._DD_open = False
                clock.schedule(s._unlock_DD, 0.05)
            if s.du and s._DU_open:
                pressed.append(s._btn_map.DU)
                s._DU_open = False
                clock.schedule(s._unlock_DU, 0.05)

        return pressed, released

    def _add(self, device_index):
        """Adds Joystick instances to the management dictionary."""
        pygame_joystick = pygame.joystick.Joystick(device_index)
        joy = Joystick(pygame_joystick)
        if len(self._sticks) == 0:
            print("Brep")
            self._default = joy.instance_id
        self._sticks[joy.instance_id] = joy

    def _remove(self, instance_id):
        """Removes a disconnected joystick."""
        if instance_id in self._sticks:
            del self._sticks[instance_id]
        if len(self._sticks) == 0:
            self._default = None
        elif instance_id == self._default:
            self._default = tuple(self._sticks.keys())[0]

    @property
    def num(self):
        """Returns the number of available joysticks."""
        return len(self._sticks)

    @property
    def ids(self):
        """Returns the currently available ids for joystick access."""
        return tuple(self._sticks.keys())

    # @property
    def get_default(self):
        """Returns a reference to the currently earliest connected
        joystick."""
        if self._default is not None:
            return self._sticks[self._default]
        else:
            return None


joysticks_instance = JoystickManager()
joy = joysticks_instance.get_default
