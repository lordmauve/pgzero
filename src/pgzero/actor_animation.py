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
        self._running_queue = False
        self._base_animation = None
        self._paused = False
        self._pause_info = None

    # Properties are defined to allow reading of values but not setting them.
    # Some of these include aliases for properties to allow easier or more
    # intuitive use.
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
        if self._base_animation:
            return self._base_animation.name
        else:
            return None

    @base_animation.setter
    def base_animation(self, name):
        # Check if the former base animation is currently running.
        swap = self._current_animation == self._base_animation
        # Since base_animation can be None, check_animation_name() cannot be
        # used here to validate the given name.
        # If the name is in the pool, set the base animation.
        if name in self._animation_pool:
            # Swap in the new animation.
            if swap:
                self._run(name)
            # Update the base animation.
            self._base_animation = self._animation_pool[name]
        # If None was set, do that too.
        elif name == None:
            # If the former base animation was running, stop it.
            if swap:
                self.stop()
            self._base_animation = None
        # Otherwise raise the same error as check_animation_name()
        else:
            raise ValueError("Given animation name is not part of the available "
                             "animation pool. Valid animation names are the following: {}"
                             .format(", ".join(self._animation_pool)))

    base = base_animation

    @property
    def paused(self):
        return self._paused

    # Checks whether the given name is actually a key for the animation pool.
    # If not, an error is raised that also lists available animations.
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
    def _run(self, name):
        # Reset pause state.
        self._paused = False
        self._pause_info = None

        # Set the currently running animation.
        self._current_animation = self._animation_pool[name]
        # Set the frame index of the animation to the starting
        # point incase for some reason it was not there already.
        # Same for resetting the new frame flag.
        self._current_animation._frame_index = -1
        self._current_animation._new_frame = False
        # Run the animation.
        self._current_animation._next_frame()

    def _resume(self):
        pass

    def play(self, name):
        # Check if the animation name is valid.
        self.check_animation_name(name)

        # Only do something if this animation is not already running.
        if not self._current_animation or self._current_animation.name != name:
            self._run(name)

    def start(self, name):
        # Check if the animation name is valid.
        self.check_animation_name(name)

        # Start the given animation, even if it was already running.
        self._run(name)

    def play_queue(self):
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
    def enqueue(self, *names):
        for n in names:
            self.check_animation_name(n)
            self._queue.append(n)

    def dequeue(self, *elems):
        # If no arguments were supplied, error.
        if not elems:
            raise ValueError("No animation name to dequeue supplied.")
        # If tuples were supplied, elements are dequeued either by
        # first, last or all elements.
        if isinstance(elems[0], tuple):
            for name, mode in elems:
                match mode:
                    case "first":
                        self._queue.remove(name)
                    case "last":
                        # Never in my life have I been so embarassed to
                        # write code that doesn't have any performance
                        # downside except for lists of length magnitudes
                        # greater than we expect here...
                        self._queue.reverse()
                        self._queue.remove(name)
                        self._queue.reverse()
                    case "all":
                        self._queue = [n for n in self._queue if n != name]
                    # If an invalid mode was given, error.
                    case _:
                        raise ValueError("Invalid mode for removal supplied. "
                                         "Valid modes are 'first', 'last' and "
                                         "'all'.")
        # If only names were supplied, default to mode 'first'.
        else:
            for name in elems:
                self._queue.remove(name)


    def empty_queue(self):
        self._queue = []

    # Ending animations
    def _done(self, name):
        """Function called by the running animation when it finishes."""
        # If the queue is playing and there are animations left in it,
        # play the next one.
        if self._running_queue and self._queue:
            self._run(self._queue.pop(0))
        # If there's no queue but a base animation, play it.
        elif self._base_animation:
            self._run(self._base_animation.name)
        # If the queue is empty and there's no base animation, stop
        # animating (this returns to the static image of the actor).
        else:
            self._current_animation = None

    def stop(self):
        # If we are running the base animation, this function does nothing.
        if self._current_animation == self._base_animation:
            return
        # Reset the state of the running animation and unschedule it.
        self._current_animation._reset()
        # If we were running the queue, stop it.
        if self._running_queue:
            self._running_queue = False
        # If there is a base animation, return to playing it.
        if self._base_animation:
            self._run(self._base_animation.name)
        else:
            self._current_animation = None

    def stop_all(self):
        # Reset the state of the running animation and unschedule it.
        self._current_animation._reset()
        # If we were running the queue, stop it.
        if self._running_queue:
            self._running_queue = False
        # TODO: Refine this. Should base be set to None or instead
        # should a way be implemented to retain base but not play it?
        self._current_animation = None
        self._base_animation = None

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
    def _next_frame(self):
        self._frame_index += 1

        # If the animation has finished, reset the frame counter and call
        # the function telling the animation manager that the animation is done.
        if self._frame_index >= len(self._frames):
            self._frame_index = -1
            # TODO: Necessary? Counterproductive? : self._new_frame = False
            self._actor._done(self._name)
            # If there was a function callback set for the animation, call it.
            if self._callback:
                self._callback()
        # If the animation is not done, schedule the next frame advancement.
        else:
            self._new_frame = True
            clock.schedule(self._next_frame, self._durations[self._frame_index])

    # Function to reset the state of the animation and unschedule its advance-
    # ment if it was running.
    def _reset(self):
        clock.unschedule(self._next_frame)
        self._frame_index = -1
        self._new_frame = False

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

