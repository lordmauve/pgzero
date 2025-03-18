from . import loaders
from . import clock

"""
Manages animations for actor objects.
"""

class ActorAnimationSystem:
    """
    Management class. Each actor holds an instance of this class in the property anim.
    Direct write access to the important properties is restricted and use of anim should
    occur only through functions.

    TODOTODOTODO this isn't clear yet!!!
    Base animation and paused could be implemented as accessible properties, but in order
    to avoid confusion, they are not. This way, the user knows that actor.anim always
    has to be used with a function.
    """

    def __init__(self):
        """Initializes the system with an empty state. This is always the starting
        point for a new actor."""
        self._animation_pool = {}
        self._current_animation = None
        self._queue = []
        self._base_animation = None
        self._paused = False
        self._pause_info = None

    @property
    def animation_pool(self):
        return list(self._animation_pool.keys())

    animations = animation_pool

    @property
    def current(self):
        return self._current_animation

    current_animation = current
    running = current

    @property
    def base_animation(self):
        return self._base_animation

    @base_animation.setter
    def base_animation(self, name):
        if name in self._animation_pool or name == None:
            self._base_animation = name
        else:
            raise ValueError("Given animation name is not part of the available "
                             "animation pool. Valid animation names are the following: {}"
                             .format(", ".join(self._animation_pool)))

    base = base_animation

    @property
    def paused(self):
        return self._paused

    def check_animation_name(self, name):
        if not name in self._animation_pool:
            raise ValueError("Given animation name is not part of the available "
                             "animation pool. Valid animation names are the following: {}"
                             .format(", ".join(self._animation_pool)))

    # Managing animations in the pool
    def add(self, name, durations=1.0, offsets=(0, 0), callback=None):
        """Adds a given animation to the animation pool by its name.
            
        :param name: Name of the animation to be added. 
        """
        # Load the animation frames via ResourceLoader
        frames = loaders.animations.load(name)
        num_frames = len(frames)

        # If multiple durations were supplied, check if their number
        # matches the number of frames and error if not.
        if isinstance(durations, (list, tuple)):
            num_durations = len(durations)
            if num_durations != num_frames:
                raise ValueError("Number of supplied durations ({}) does "
                                 "not match number of animation frames ({})."
                                 .format(num_durations, num_frames))
            # Make sure that durations is now a tuple if it was a list before.
            durations = tuple(durations)
        # If a single duration was supplied, divide it equally among
        # all frames.
        else:
            each_duration = durations / num_frames
            durations = tuple([each_duration] * num_frames)

        # Basically same check for offsets but the condition checks whether the
        # first element of offsets is also a tuple, since a single offset would
        # already satisfy the condition otherwise.
        if isinstance(offsets, list) or isinstance(offsets[0], tuple):
            num_offsets = len(offsets)
            if num_offsets != num_frames:
                raise ValueError("Number of supplied offsets ({}) does "
                                 "not match number of animation frames ({})."
                                 .format(num_offsets, num_frames))
        # If a single offset was supplied, give it to every frame.
        else:
            offsets = tuple([offsets] * num_frames)
        
        # Create the new animation and add it to the available pool.
        a = ActorAnimation(self, name, frames, durations, offsets, callback)
        self._animation_pool[name] = a

    def remove(self, name):
        """Removes the named animation from the animation pool.

        :param name: Name of the animation to be removed.
        """
        # If the animation is part of the pool, remove it an unload the
        # cached animation frames.
        self.check_animation_name(name)

        del self._animation_pool[name]
        loaders.animations.unload(name)

    # Playing animations
    def play(self, name):
        # Check if the animation name is valid.
        self.check_animation_name(name)

        # Only do something if this animation is not already running.
        if not self._current_animation or self._current_animation.name != name:
            self._paused = False
            self._pause_info = None

            self._current_animation = self._animation_pool[name]
            self._current_animation.next_frame()

    def start(self, name):
        pass

    # Pausing animations
    def pause(self):
        pass

    def unpause(self):
        pass

    # Base animation
    # set_base() is a courtesy function to make working with anim easier.
    # Since the user mostly makes something happen with anim through
    # functions, the base animation can also be manipulated with functions.
    def set_base(self, name):
        self.base_animation = name

    def remove_base(self, name):
        self.base_animation = None

    # Animation queue
    def queue(self, *name):
        pass

    def dequeue(self, *name):
        pass

    def empty_queue(self):
        self._queue = []

    # Ending animations
    def _done(self, name):
        """Function called by the running animation when it finishes."""
        self._current_animation = None

    def stop(self):
        pass

    def stop_all(self):
        pass

    def __repr__(self):
        return "<ActorAnimationSystem={}>".format(self.__dir__())


class ActorAnimation:

    def __init__(self, actor, name, frames, durations, offsets, callback):
        self._actor = actor
        self._name = name
        self._frames = frames
        self._frame_index = -1
        self._new_frame = False
        self._durations = durations
        self._offsets = offsets
        self._callback = callback

    # Function to advance the current frame and schedule the next advancement
    def next_frame(self):
        self._frame_index += 1

        # If the animation has finished, reset the frame counter and call
        # the function telling the animation manager that the animation is done.
        if self._frame_index >= len(self._frames):
            self._frame_index = 0
            # self._new_frame = False
            self._actor._done(self._name)
            # If there was a function callback set for the animation, call it.
            if self._callback:
                self._callback()
        # If the animation is not done, schedule the next frame advancement.
        else:
            self._new_frame = True
            clock.schedule(self.next_frame, self._durations[self._frame_index])

    @property
    def name(self):
        return self._name

    @property
    def frames(self):
        return self._frames

    @property
    def frame(self):
        return self._frames[self._frame_index]

    @property
    def durations(self):
        return self._durations

    @property
    def duration(self):
        return self._durations[self._frame_index]

    @property
    def offsets(self):
        return self._offsets

    @property
    def offset(self):
        return self.offsets[self._frame_index]

    @property
    def offset_x(self):
        return self._offset[self._frame_index][0]

    @property
    def offset_y(self):
        return self._offset[self._frame_index][1]

    @property
    def callback(self):
        return self._callback
    
    def __repr__(self):
        return "<ActorAnimation={}>".format(self.__dir__())

