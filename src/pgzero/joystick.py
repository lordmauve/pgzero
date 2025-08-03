import pygame
from enum import IntEnum
from dataclasses import dataclass
import platform
from . import clock


@dataclass
class ButtonMap:
    face_up: int = 99
    face_down: int = 99
    face_left: int = 99
    face_right: int = 99
    dpad_up: int = 99
    dpad_down: int = 99
    dpad_left: int = 99
    dpad_right: int = 99
    shoulder_left: int = 99
    shoulder_right: int = 99
    push_left: int = 99
    push_right: int = 99
    center_left: int = 99
    center_middle: int = 99
    center_middle_alt: int = 99
    center_right: int = 99


@dataclass
class AxisMap:
    left_x: int = 99
    left_y: int = 99
    left_trigger: int = 99
    right_x: int = 99
    right_y: int = 99
    right_trigger: int = 99


SDL_ASSOCIATIONS = {"a": "face_down", "b": "face_right", "x": "face_left",
                    "y": "face_up", "dpup": "dpad_up",
                    "dpdown": "dpad_down", "dpleft": "dpad_left",
                    "dpright": "dpad_right", "leftshoulder": "shoulder_left",
                    "rightshoulder": "shoulder_right",
                    "rightstick": "push_right", "leftstick": "push_left",
                    "guide": "center_middle", "back": "center_left",
                    "start": "center_right", "misc1": "center_middle_alt",
                    "lefttrigger": "left_trigger",
                    "righttrigger": "right_trigger", "leftx": "left_x",
                    "lefty": "left_y", "rightx": "right_x", "righty": "right_y"}

BTN_NAMES = ("face_up", "face_down", "face_left", "face_right", "dpad_up",
             "dpad_down", "dpad_left", "dpad_right", "shoulder_left",
             "shoulder_right", "push_left", "push_right", "center_left",
             "center_middle", "center_right")

AXIS_NAMES = {"left_x", "left_y", "left_trigger", "right_x", "right_y",
              "right_trigger"}

def _get_map_dict(guid):
    from importlib.resources import files

    # Use the correct file per system type.
    system = platform.system()
    if system == "Windows":
        filename = "controllers_windows.txt"
    elif system == "Darwin":
        filename = "controllers_macos.txt"
    else:
        # Linux mappings are also used as a fallback default.
        filename = "controllers_linux.txt"

    filepath = files().joinpath("data").joinpath(filename)

    # Go through the mapping file searching for the given GUID.
    with open(filepath) as mapfile:
        for line in mapfile:
            # If we find the GUID, save the whole line for disection.
            if line.startswith(guid):
                raw_map = line
                break
        else:
            # If no mapping is available, a default one for an Xbox 360 is
            # used in hopes it somewhat matches since the 360 layout seems to
            # be the most common on older third party controllers for PC.
            raw_map = ("030000005e0400008e02000001000000,Microsoft Xbox 360,"
                       "a:b0,b:b1,back:b6,dpdown:h0.1,dpleft:h0.2,"
                       "dpright:h0.8,dpup:h0.4,leftshoulder:b4,leftstick:b9,"
                       "lefttrigger:a2,leftx:a0,lefty:a1,rightshoulder:b5,"
                       "rightstick:b10,righttrigger:a5,rightx:a3,righty:a4,"
                       "start:b7,x:b2,y:b3,platform:Linux,")

    parts = raw_map.split(",")[2:-2]
    map_dict = {}
    for p in parts:
        k, v = p.split(":")
        map_dict[k] = v

    return map_dict

def _get_mappings_from_guid(guid):
    # Remove the CRC component from the GUID
    generic_guid = guid[:4] + "0000" + guid[8:]

    # Gets an automatic mapping from the right file and creates a dict from it.
    map_dict = _get_map_dict(generic_guid)

    # So far empty instances of dataclasses to hold the mappings.
    btn_map = ButtonMap()
    axis_map = AxisMap()

    for k, v in map_dict.items():
        if k in ("a", "b", "x", "y", "back", "guide", "start", "misc1",
                 "leftshoulder", "rightshoulder", "leftstick", "rightstick"):
            setattr(btn_map, SDL_ASSOCIATIONS[k], int(v[1:]))
        elif k in ("dpup", "dpdown", "dpleft", "dpright"):
            if v[0] == "b":
                setattr(btn_map, SDL_ASSOCIATIONS[k], int(v[1:]))
            else:
                # If the controller treats the DPad like a Hat-Switch, we
                # create a (hopefully) unique int from the Hat-Identifier,
                # the direction and a preceding 9 to not have collisions with
                # other mapping numbers like 11, 14, 18 etc.
                num = int("9" + v[1] + v[-1])
                setattr(btn_map, SDL_ASSOCIATIONS[k], num)
        elif k in ("lefttrigger", "righttrigger", "leftx", "lefty", "rightx",
                   "righty"):
            setattr(axis_map, SDL_ASSOCIATIONS[k], int(v[1:]))

    return btn_map, axis_map


class Joystick:
    """PGZero wrapper class for joystick use."""

    def __init__(self, stick):
        self._stick = stick
        guid = stick.get_guid()
        self._btn_map, self._axis_map = _get_mappings_from_guid(guid)

        self._initialize_state_tracking()

        self._initialize_debounce_gates()
    
    # Since writing out each button and axis creates a lot of redundant code,
    # all logic to simply check if a button is pressed or where an axis is
    # held is handled here dynamically.
    def __getattr__(self, name):
        if name in BTN_NAMES:
            return self._pressed[getattr(self._btn_map, name)]
        elif name in AXIS_NAMES:
            return self._axis[getattr(self._axis_map, name)]
        else:
            raise AttributeError("'Joystick' object has no attribute '{}'"
                                 .format(name))

    def _initialize_state_tracking(self):
        self._pressed = {getattr(self._btn_map, b): False for b in BTN_NAMES}
        self._axis = {getattr(self._axis_map, a): 0 for a in AXIS_NAMES}
        # Since triggers don't start centered but rather unpressed,
        # their starting values are -1.
        self._axis[self._axis_map.right_trigger] = -1
        self._axis[self._axis_map.left_trigger] = -1

        # These lookup dicts are used to determine the semantic button pressed
        # from the integer button gotten by Pygame.
        self._btn_lookup = {getattr(self._btn_map, b): b for b in BTN_NAMES}
        self._axis_lookup = {getattr(self._axis_map, a): a for a in AXIS_NAMES}

    def _initialize_debounce_gates(self):
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
    def name(self):
        """Returns the human readable name of the controller."""
        return self._stick.get_name()

    @property
    def guid(self):
        """Returns the GUID of the controller."""
        return self._stick.get_guid()

    @property
    def instance_id(self):
        """Returns the instance id of the controller."""
        return self._stick.get_instance_id()

    @property
    def left_stick(self):
        """Returns a tuple of the axis values for the left stick."""
        return (self._axis[self._axis_map.left_x],
                self._axis[self._axis_map.left_y])

    @property
    def left_angle(self):
        """Returns the angle the left stick is held to or None if it is
        centered."""
        if self.left_stick == (0, 0):
            return None
        _, p = pygame.math.Vector2(self.left_stick).as_polar()
        degrees = (360 - p) % 360
        return degrees

    @property
    def left_trigger(self):
        """Returns the axis value for the left trigger.
        Since triggers are monodirectional, their value ranges
        are recalculated from [-1, 1] to [0, 1] to represent them
        being depressed."""
        return (self._axis[self._axis_map.left_trigger] + 1) / 2

    @property
    def right_stick(self):
        """Returns a tuple of the axis values for the right stick."""
        return (self._axis[self._axis_map.right_x],
                self._axis[self._axis_map.right_y])

    @property
    def right_angle(self):
        """Returns the angle the right stick is held to or None if it is
        centered."""
        if self.right_stick == (0, 0):
            return None
        _, p = pygame.math.Vector2(self.right_stick).as_polar()
        degrees = (360 - p) % 360
        return degrees

    @property
    def right_trigger(self):
        """Returns the axis value for the right trigger.
        Since triggers are monodirectional, their value ranges
        are recalculated from [-1, 1] to [0, 1] to represent them
        being depressed."""
        return (self._axis[self._axis_map.right_trigger] + 1) / 2


class GenericJoystick(Joystick):
    """PGZero joystick wrapper with a predefined generic mapping."""

    def __init__(self):
        self._btn_map = ButtonMap(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                                  15, 14)
        self._axis_map = AxisMap(0, 1, 2, 3, 4, 5)

        self._initialize_state_tracking()

        # When this class is used for the all-in-one controller of the
        # JoystickManager, the gates aren't actually used. They are still
        # initialized for full compatibility however, in case other uses for a
        # generic Joystick come up.
        self._initialize_debounce_gates()

    @property
    def name(self):
        """Returns the human readable name of the controller."""
        return "GENERIC PGZERO CONTROLLER"

    @property
    def guid(self):
        """Returns the GUID of the controller."""
        return "00000000000000000000000000000000"

    @property
    def instance_id(self):
        """Returns the instance id of the controller."""
        return 999


class JoystickManager:
    """Interface to pygame joystick support. Holds all active joysticks
    and modifies their states based on pygame events."""

    def __init__(self):
        self._sticks = {}
        self._union_stick = GenericJoystick()
        self._default = None
        self._deadzone = 0.065

    def _press(self, iid, button):
        s = self._sticks[iid]
        us = self._union_stick
        # A press of an alternate middle button gets converted to the standard
        # middle button.
        if button == s._btn_map.center_middle_alt:
            button = s._btn_map.center_middle
        s._pressed[button] = True
        # If a button is not recognized, None is returned.
        try:
            identifier = s._btn_lookup[button]

            # We also press the corresponding button on the all-in-one
            # controller.
            us._pressed[getattr(us._btn_map, identifier)] = True
        except ValueError:
            identifier = None
        return identifier

    def _release(self, iid, button):
        s = self._sticks[iid]
        us = self._union_stick
        if button == s._btn_map.center_middle_alt:
            button = s._btn_map.center_middle
        s._pressed[button] = False
        try:
            identifier = s._btn_lookup[button]

            us._pressed[getattr(us._btn_map, identifier)] = False
        except ValueError:
            identifier = None
        return identifier

    def _set_axis(self, iid, axis, value):
        """Sets the axis value of a stick or trigger. Enforces the set
        deadzone to prevent jittery results from slightly drifting or
        uncentered sticks."""
        s = self._sticks[iid]
        us = self._union_stick
        ax = s._axis_lookup[axis]
        changed = True
        if ax == "left_trigger" or ax == "right_trigger":
            if value < -1 + self._deadzone:
                # If no change was made, no user joy motion event should be
                # triggered.
                if s._axis[axis] == -1:
                    changed = False
                s._axis[axis] = -1
            elif value > 1 - self._deadzone:
                if s._axis[axis] == 1:
                    changed = False
                s._axis[axis] = 1
            else:
                s._axis[axis] = value
        elif value > self._deadzone or value < self._deadzone * -1:
            s._axis[axis] = value
        else:
            if s._axis[axis] == 0:
                changed = False
            s._axis[axis] = 0
        try:
            identifier = s._axis_lookup[axis]

            # Since deadzones are in play, we make sure the all-in-one stick
            # has the right value by simply aligning it with the change made
            # to the individual joystick.
            us._axis[getattr(us._axis_map, identifier)] = s._axis[axis]
        except ValueError:
            identifier = None
        return identifier, s._axis[axis], changed

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
            if not s.dpad_right and s._DR_open:
                pressed.append(s._btn_map.dpad_right)
                s._DR_open = False
                clock.schedule(s._unlock_DR, 0.05)
            if s.dpad_left and s._DL_open:
                released.append(s._btn_map.dpad_left)
                s._DL_open = False
                clock.schedule(s._unlock_DL, 0.05)
        elif vx == 0:
            if s.dpad_right and s._DR_open:
                released.append(s._btn_map.dpad_right)
                s._DR_open = False
                clock.schedule(s._unlock_DR, 0.05)
            if s.dpad_left and s._DL_open:
                released.append(s._btn_map.dpad_left)
                s._DL_open = False
                clock.schedule(s._unlock_DL, 0.05)
        elif vx == -1:
            if not s.dpad_left and s._DL_open:
                pressed.append(s._btn_map.dpad_left)
                s._DL_open = False
                clock.schedule(s._unlock_DL, 0.05)
            if s.dpad_right and s._DR_open:
                pressed.append(s._btn_map.dpad_right)
                s._DR_open = False
                clock.schedule(s._unlock_DR, 0.05)

        if vy == 1:
            if not s.dpad_up and s._DU_open:
                pressed.append(s._btn_map.dpad_up)
                s._DU_open = False
                clock.schedule(s._unlock_DU, 0.05)
            if s.dpad_down and s._DD_open:
                released.append(s._btn_map.dpad_down)
                s._DD_open = False
                clock.schedule(s._unlock_DD, 0.05)
        elif vy == 0:
            if s.dpad_up and s._DU_open:
                released.append(s._btn_map.dpad_up)
                s._DU_open = False
                clock.schedule(s._unlock_DU, 0.05)
            if s.dpad_down and s._DD_open:
                released.append(s._btn_map.dpad_down)
                s._DD_open = False
                clock.schedule(s._unlock_DD, 0.05)
        elif vy == -1:
            if not s.dpad_down and s._DD_open:
                pressed.append(s._btn_map.dpad_down)
                s._DD_open = False
                clock.schedule(s._unlock_DD, 0.05)
            if s.dpad_up and s._DU_open:
                pressed.append(s._btn_map.dpad_up)
                s._DU_open = False
                clock.schedule(s._unlock_DU, 0.05)

        # The all-in-one joystick doesn't have its debounce gates triggered
        # since jittery input from one controller is avoided by its own gating
        # whereas jitters can't be prevented if multiple gamepads have their
        # hats pressed in a very close timespan.

        return pressed, released

    def _add(self, device_index):
        """Adds Joystick instances to the management dictionary."""
        pygame_joystick = pygame.joystick.Joystick(device_index)
        joy = Joystick(pygame_joystick)
        if len(self._sticks) == 0:
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
joy = joysticks_instance._union_stick
