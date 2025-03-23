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
        self._playing_queue = False
        self._queue_index = None
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
    def queue(self):
        return tuple(self._queue)

    @property
    def playing_queue(self):
        return self._playing_queue

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
        # If the name is in the pool, set the base animation.
        if name in self._animation_pool:
            # Run this animation if base animation was running
            # or no animation was running.
            if swap or not self._current_animation:
                self._run(name)
            # Update the base animation.
            self._base_animation = self._animation_pool[name]
        # If None was set, do that too.
        elif name == None:
            # If the former base animation was running, stop it.
            if swap:
                self.stop_all()
            # stop_all() already sets the base animation to None
            # so this can be in an else block.
            else:
                self._base_animation = None
        # Otherwise raise the same error as check_animation_name().
        # Since base_animation can be None, check_animation_name() cannot be
        # used here to validate the given name.
        else:
            raise ValueError("Given animation name is not part of the available "
                             "animation pool. Valid animation names are the following: {}"
                             .format(", ".join(self._animation_pool)))

    base = base_animation

    @property
    def paused(self):
        return self._paused

    @property
    def current_type(self):
        if self._current_animation == self._base_animation.name:
            return "base"
        elif self._playing_queue:
            return "queue"
        elif self._current_animation:
            return "single"
        else:
            return None
            
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

        # The length of offsets is used either to check whether the correct
        # number of individual offsets were given or if the single offset
        # tuple contains the correct number of values (2).
        num_offsets = len(offsets)
        # Basically same check for offsets but the condition checks whether the
        # first element of offsets is also a tuple, since a single offset would
        # already satisfy the condition otherwise.
        if isinstance(offsets[0], tuple):
            if num_offsets != num_frames:
                raise ValueError("Number of supplied offsets ({}) does "
                                 "not match number of animation frames ({})."
                                 .format(num_offsets, num_frames))
            # Check each offset for correct number of values.
            for o in offsets:
                l = len(o)
                if l != 2:
                    raise ValueError("Offset tuples must have exactly two "
                                     "integer values for x and y, not {} "
                                     "values.".format(l))
        # If only a single tuple was supplied, also check number of values.
        elif num_offsets != 2:
            raise ValueError("Offset tuples must have exactly two integer "
                             "values for x and y, not {} values."
                             .format(num_offsets))
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
    def _run(self, name, resume = False):
        # If an animation is currently running, unschedule its
        # frame advancement.
        if self._current_animation:
            clock.unschedule(self._current_animation._next_frame)
        # Set the new currently running animation.
        self._current_animation = self._animation_pool[name]
        # If an animation should not be started but resumed,
        # get the remaining information from the pause state
        # and call the animations function to resume playing.
        if resume:
            self._current_animation._resume_frame(self._pause_info[1])
        # Otherwise, reset the progress states of the animation
        # in case they hadn't been already and run it.
        else:
            self._current_animation._frame_index = None
            self._current_animation._new_frame = False
            
            self._current_animation._next_frame()

        # Reset pause state.
        self._paused = False
        self._pause_info = None

    def play(self, name):
        # Check if the animation name is valid.
        self.check_animation_name(name)

        # Only do something if this animation is not already running.
        if not self._current_animation or self._current_animation.name != name:
            # If the queue was playing before, pause it.
            self.pause_queue()
            # Start the animation.
            self._run(name)

    def start(self, name):
        # Check if the animation name is valid.
        self.check_animation_name(name)

        # Pause the queue, if it was playing.
        self.pause_queue()

        # Start the given animation, even if it was already running.
        self._run(name)

    def play_queue(self):
        # If the queue is already playing, do nothing.
        if self._playing_queue:
            return
        # Start playing the animation at the current position in the queue.
        self._advance_queue()

    def start_queue(self):
        self.queue_jump(1)

        self._advance_queue()

    # Pausing animations
    def pause(self):
        # If we are paused, do nothing.
        if self._paused:
            return
        # Calculate the remaining time the frame should be shown after
        # unpausing.
        started = self._current_animation._frame_started
        paused = clock.time()
        remaining = paused - started

        # Unschedule advancing the current animation.
        clock.unschedule(self._current_animation._next_frame)

        # Record information about the animation before the pause for 
        # unpausing and unset the current animation.
        self._paused = True
        self._pause_info = (self._current_animation._name, remaining, self.current_type)
        # Unset any state indicating current animation.
        self._playing_queue = False
        self._current_animation = None

    def unpause(self):
        # If we aren't paused, do nothing.
        if not self._paused:
            return
        # Get the name of the animation before the pause.
        p_name = self._pause_info[0]

        # Makes sure the animation that should be unpaused is still
        # in the animation pool.
        self.check_animation_name(p_name)

        # Running _run() with True makes it resume the animation 
        # instead of starting it from scratch.
        self._run(p_name, True)
        # If the animation was from the queue, also set the
        # queue boolean again.
        if self._pause_info[2] == "queue":
            self._playing_queue = True

    def pause_queue(self):
        # TODO: WRITE THIS...
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
    def queue_position(self):
        """Returns the current position in the queue. None means the
        queue hasn't started yet, 1 is the first and so on."""
        if self._queue_index != None:
            return self._queue_index + 1
        return None

    def enqueue(self, *names):
        if not names:
            raise ValueError("No animation names to enqueue supplied.")
        # Check for valid names and add them to the queue.
        for n in names:
            self.check_animation_name(n)
            self._queue.append(n)

    # TODO: Function needs a better but not too long name.
    def _dequeue_adjust_index(self, name, local_queue_index, q_reversed = False):
        # If the queue is not started, no checks or adjustments have to be
        # made.
        if not local_queue_index:
            return False
        elem_index = self._queue.index(name)
        # If the currently playing queue animation should be removed,
        # note this and reset it.
        if self._playing_queue and local_queue_index == self._queue.index(name):
            self._queue[local_queue_index]._reset()
            return True
        # If the animation to be removed lies in front of the queue index,
        # it must be adjusted to still play the correct animation after removals.
        elif (q_reversed and local_queue_index < elem_index) or elem_index < local_queue_index:
            self._queue_index -= 1
        return False

    # TODO: If the animation to be dequeued is currently playing in the
    # queue, reset it, remove it and play the animation the at the next
    # position after all dequeuing is done.
    def dequeue(self, *elems):
        # If no arguments were supplied, error.
        if not elems:
            raise ValueError("No animation name to dequeue supplied.")

        # TODO: Rework comments to include the fact that queue_index is
        # None if there is no position in the queue and that 
        # dequeue_adjust_index checks for this.
        removed_playing = False
        # Go through each supplied animation to dequeue. If
        # they are tuples, apply the correct mode of removal,
        # if not default to "first".
        for e in elems:
            # TODO: Separate this into its own function for readability.
            if isinstance(e, tuple):
                name, mode = e
                # If a name is not in the queue, error descriptively.
                if name in self._queue:
                    match mode:
                        case "first":
                            # Checks if the playing animation gets removed and
                            # adjusts the queue index in case the removed
                            # animation is before the current one.
                            if self._dequeue_adjust_index(name, self._queue_index):
                                removed_playing = True
                            # Remove the animation from the queue.
                            self._queue.remove(name)
                        case "last":
                            # Reverse-remove-reverse is not efficient, but this
                            # shouldn't really matter for lists as small as queues
                            # are likely to be.
                            self._queue.reverse()
                            # Calculate the index of the playing animation in the
                            # reversed queue.
                            if self._queue_index != None:
                                rev_queue_index = len(self._queue) - self._queue_index - 1
                            else:
                                rev_queue_index = None
                            # Same check above, last parameter tells the function the
                            # queue is reversed.
                            if self._dequeue_adjust_index(name, rev_queue_index, True):
                                removed_playing = True
                            # Remove the animation.
                            self._queue.remove(name)
                            # Flip the queue back.
                            self._queue.reverse()
                        case "all":
                            # Cheking for removal of current animation is simpler
                            # because all instances of this animation are removed,
                            # meaning the index doesn't matter.
                            if self._queue_index and name == self._queue[self._queue_index].name:
                                self._queue[self._queue_index]._reset()
                                removed_playing = True
                            # List to fill with animations to keep in the queue.
                            keep_queue = []
                            # Since the actual queue index could change, we need
                            # a static one to compare against.
                            og_queue_index = self._queue_index
                            # Go through the queue, keeping all animations not
                            # targeted by this removal. Wherever one is removed
                            # that's before the queue index, adjust it down.
                            for i, n in enumerate(self._queue):
                                if n != name:
                                    keep_queue.append(n)
                                elif og_queue_index and i < og_queue_index:
                                    self._queue_index -= 1
                            # TODO: Should this get a copy of keep_queue instead?
                            #       Not really I think but should make sure.
                            # Set the queue to the version with all occurences
                            # of current target removed.
                            self._queue = keep_queue
                        case _:
                            raise ValueError("Invalid mode for removal supplied. "
                                             "Valid modes are 'first', 'last' and "
                                             "'all'.")
                else:
                    raise ValueError("Given name {} isn't part of the queue: {}"
                                     .format(name, ",".join(self._queue)))
            else:
                if e in self._queue:
                    if self._dequeue_adjust_index(name, self._queue_index):
                        removed_playing = True
                    self._queue.remove(e)
                else:
                    raise ValueError("Given name {} isn't part of the queue: {}"
                                     .format(name, ",".join(self._queue)))

            # If the playing animation was removed and the queue still has
            # animations play the one after where the playing animation was
            # removed.
            if removed_playing:
                # TODO: Does this work?!?
                self._queue_index -= 1
                self.play_queue()

    # TODO: Better name for this function?
    def queue_jump(self, position):
        """Jump to a specific animation in the queue by position."""
        index = position - 1
        # Error descriptively in case of a bad given position.
        if index < 0 or index >= len(self._queue):
            raise ValueError("Position {} to jump to is not in the queue. "
                             "Minimum position is 1 and maximum position is"
                             " currently {}".format(position, len(self._queue)))

        # If the queue is currently playing, reset the animation and
        # play from where the new position is.
        if self._playing_queue:
            self._queue[self._queue_index].reset()

            self._queue_index = index - 1
            self._advance_queue()
        # Otherwise, only set the position without starting to play.
        # TODO: Should this be changed? Should queue_jump always play?
        else:
            self._queue_index = index - 1

    def _check_queue_steps(self, steps = 1, forward = True):
        """Function to check whether a given amount of steps to change
        the queue position by is in bounds based on the direction to move."""
        if steps < 1:
            raise ValueError("queue_next() accepts only positive integer "
                             "values (the number of animations to go forward "
                             "in the queue), not {}.".format(steps))
        elif forward and self._queue_index + steps >= len(self._queue):
            raise IndexError("Given steps ({}) go out of bounds of the animation "
                             "queue, maximum steps forward at this point would be {}."
                             .format(steps, len(self._queue) - self._queue_index - 1))
        elif self._queue_index - steps < -1:
            raise IndexError("Given steps ({}) go out of bounds of the animation "
                             "queue, maximum steps backward at this point would be {}."
                             .format(steps, self._queue_index))


    def queue_next(self, steps = 1):
        # Catch possible bad value for steps.
        self._check_queue_steps(steps)

        # If the queue is playing, advance by the given number of
        # animations.
        if self._playing_queue:
            self._queue[self._queue_index].reset()
            # Since _advance_queue() already increments the index by
            # one, we reduce it by one here to have more intuitive
            # values to use with the function.
            self._queue_index += steps - 1
            self._advance_queue()
        # Otherwise, simply start playing it from the correct position.
        else:
            if self._queue_index != None:
                self._queue_index += steps - 1
            else:
                self._queue_index = steps - 1
            self.play_queue()

    def queue_previous(self, steps = 1):
        # Catch possible bad value for steps.
        self._check_queue_steps(steps, False)

        # If the queue is playing, move back by the given number of
        # animations.
        if self._playing_queue:
            self._queue[self._queue_index].reset()

            self._queue_index -= steps - 1
            self._advance_queue()
        else:
            print("WARNING: Queue is not playing, can't move back"
                  " to former animations.")

    # Advance the index for the queue by one and react to the
    # resulting state.
    def _advance_queue(self):
        if self._queue_index != None:
            self._queue_index += 1
        else:
            self._queue_index = 0

        # If the queue is done, reset the index, turn off playing
        # the queue and return to the base animation if there is
        # one.
        if self._queue_index >= len(self._queue):
            self._queue_index = None
            self._playing_queue = False
            # TODO: Is this the best solution? Getting to the end
            # of the queue calls _done() twice. Not a performance
            # problem but maybe a design problem?
            self._done(queue_finished = True)
        else:
            # Run the now current animation from the queue and set
            # the boolean keeping track if the queue is playing.
            self._run(self._queue[self._queue_index])
            self._playing_queue = True

    def empty_queue(self):
        # If the queue is playing while it should be emptied, stop
        # playing it.
        if self._playing_queue:
            self.stop()
        self._queue = []

    # Ending animations
    def _done(self, name = "", queue_finished = False):
        """Function called by the running animation when it finishes."""
        # If the queue is playing and there are animations left in it,
        # play the next one.
        if self._playing_queue:
            self._advance_queue()
        # If there's no queue but a base animation, play it.
        elif self._base_animation:
            self._run(self._base_animation.name)
        # If the queue is empty and there's no base animation, stop
        # animating (this returns to the static image of the actor).
        else:
            self._current_animation = None

    def stop(self):
        # If no animations are running or we are running the base
        # animation, do nothing.
        if not self._current_animation or self._current_animation == self._base_animation:
            return

        # Reset the state of the running animation and unschedule it.
        self._current_animation._reset()
        # If we were running the queue, stop it.
        if self._playing_queue:
            self._playing_queue = False
        # If there is a base animation, return to playing it.
        if self._base_animation:
            self._run(self._base_animation.name)
        else:
            self._current_animation = None

    def stop_all(self):
        # If no animations are running, do nothing.
        if not self._current_animation:
            return
        # Reset the state of the running animation and unschedule it.
        self._current_animation._reset()
        # If we were running the queue, stop it.
        if self._playing_queue:
            self._playing_queue = False
        # TODO: Refine this. Should base be set to None or instead
        # should a way be implemented to retain base but not play it?
        self._current_animation = None
        self._base_animation = None

    def __repr__(self):
        return "<ActorAnimationSystem={}>".format(self.__dir__())


class ActorAnimation:

    def __init__(self, actor, name, frames, durations, offsets, callback):
        self._actor = actor # Actor object that holds the animation.
        self._name = name # Name of the animation.
        self._frames = frames # Tuple of frames of the animation.
        self._frame_index = None # Index of the current frame.
        self._new_frame = False # Indicator whether draw() of the actor
                                # should load the current image.
        self._frame_started = None # Time when this frame started being shown.
        self._durations = durations # Tuple of frame durations.
        self._offsets = offsets # Tuple of spacial offsets for frames.
        self._callback = callback # Callback function for the animation.

    # Function to advance the current frame and schedule the next advancement
    def _next_frame(self):
        if self._frame_index != None:
            self._frame_index += 1
        else:
            self._frame_index = 0

        # If the animation has finished, reset the frame counter and call
        # the function telling the animation manager that the animation is done.
        if self._frame_index >= len(self._frames):
            self._frame_index = None
            # TODO: Necessary? Counterproductive? : self._new_frame = False
            self._actor._done(self._name)
            # If there was a function callback set for the animation, call it.
            if self._callback:
                self._callback()
        # If the animation is not done, schedule the next frame advancement.
        else:
            # Indicates actor.draw() should get the new frame.
            self._new_frame = True
            # Records when this frame was started to be shown.
            self._frame_started = clock.time()
            # Schedules the next frame advancement.
            clock.schedule(self._next_frame, self._durations[self._frame_index])

    def _resume_frame(self, remaining_duration):
        self._new_frame = True
        self._frame_started = clock.time()
        clock.schedule(self._next_frame, remaining_duration)

    # Function to reset the state of the animation and unschedule its advance-
    # ment if it was running.
    def _reset(self): 
        # Unscheduling does not error even if _next_frame was not scheduled.
        clock.unschedule(self._next_frame)
        # Reset the tracking values for animation progress.
        self._frame_index = None
        self._new_frame = False
        self._frame_started = None

    @property
    def name(self):
        return self._name

    @property
    def frames(self):
        return self._frames

    @property
    def frame(self):
        # TODO: What's the best behaviour when the user asks for
        # info about the current frame when the animation isn't
        # running? Currently, some return None and others neutral
        # values for their operations. Better ideas?
        if self._frame_index:
            return self._frames[self._frame_index]
        return None

    @property
    def durations(self):
        return self._durations

    @property
    def duration(self):
        if self._frame_index:
            return self._durations[self._frame_index]
        return None

    @property
    def offsets(self):
        return self._offsets

    @property
    def offset(self):
        if self._frame_index:
            return self.offsets[self._frame_index]
        return (0, 0)

    @property
    def offset_x(self):
        if self._frame_index:
            return self._offsets[self._frame_index][0]
        return 0

    @property
    def offset_y(self):
        if self._frame_index:
            return self._offsets[self._frame_index][1]
        return 0

    @property
    def callback(self):
        return self._callback
    
    def __repr__(self):
        return "<ActorAnimation={}>".format(self.__dir__())

