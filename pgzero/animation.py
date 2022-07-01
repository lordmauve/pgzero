# Easing Functions ported from the Clutter Project via http://kivy.org/
#  http://www.clutter-project.org/docs/clutter/stable/ClutterAlpha.html


from math import sin, pow, pi

from .clock import each_tick, unschedule
from .spellcheck import suggest

TWEEN_FUNCTIONS = {}


def tweener(f):
    TWEEN_FUNCTIONS[f.__name__] = f
    return f


@tweener
def linear(n):
    return n


@tweener
def accelerate(n):
    return n * n


@tweener
def decelerate(n):
    return -1.0 * n * (n - 2.0)


@tweener
def accel_decel(n):
    p = n * 2
    if p < 1:
        return 0.5 * p * p
    p -= 1.0
    return -0.5 * (p * (p - 2.0) - 1.0)


@tweener
def in_elastic(n):
    p = .3
    s = p / 4.0
    q = n
    if q == 1:
        return 1.0
    q -= 1.0
    return -(pow(2, 10 * q) * sin((q - s) * (2 * pi) / p))


@tweener
def out_elastic(n):
    p = .3
    s = p / 4.0
    q = n
    if q == 1:
        return 1.0
    return pow(2, -10 * q) * sin((q - s) * (2 * pi) / p) + 1.0


@tweener
def in_out_elastic(n):
    p = .3 * 1.5
    s = p / 4.0
    q = n * 2
    if q == 2:
        return 1.0
    if q < 1:
        q -= 1.0
        return -.5 * (pow(2, 10 * q) * sin((q - s) * (2.0 * pi) / p))
    else:
        q -= 1.0
        return pow(2, -10 * q) * sin((q - s) * (2.0 * pi) / p) * .5 + 1.0


def _out_bounce_internal(t, d):
    p = t / d
    if p < (1.0 / 2.75):
        return 7.5625 * p * p
    elif p < (2.0 / 2.75):
        p -= (1.5 / 2.75)
        return 7.5625 * p * p + .75
    elif p < (2.5 / 2.75):
        p -= (2.25 / 2.75)
        return 7.5625 * p * p + .9375
    else:
        p -= (2.625 / 2.75)
        return 7.5625 * p * p + .984375


def _in_bounce_internal(t, d):
    return 1.0 - _out_bounce_internal(d - t, d)


@tweener
def bounce_end(n):
    return _out_bounce_internal(n, 1.)


@tweener
def bounce_start(n):
    return _in_bounce_internal(n, 1.)


@tweener
def bounce_start_end(n):
    p = n * 2.
    if p < 1.:
        return _in_bounce_internal(p, 1.) * .5
    return _out_bounce_internal(p - 1., 1.) * .5 + .5


def tween(n, start, end):
    return start + (end - start) * n


def tween_attr(n, start, end):
    if isinstance(start, tuple):
        return tuple(tween(n, a, b) for a, b in zip(start, end))
    elif isinstance(start, list):
        return [tween(n, a, b) for a, b in zip(start, end)]
    else:
        return tween(n, start, end)


class Animation:
    """An animation manager for object attribute animations.

    Each keyword argument given to the Animation on creation (except
    "type" and "duration") will be *tweened* from their current value
    on the object to the target value specified.

    If the value is a list or tuple, then each value inside that will
    be tweened.

    The update() method is automatically scheduled with the clock for
    the duration of the animation.

    """
    animations = []  # Stores strong references to objects being animated.

    # Animations are stored in _animation_dict under (object id, target
    # attribute) keys. Objects may not be hashable, so the id, rather than
    # the object itself, is needed.
    # Animations with multiple targets will appear here multiple times.
    # Newly scheduled animations will overwrite new ones. Once an animation
    # ends, it is removed from this dict.
    # Note that Animation keeps a reference to "its" object, so the id in the
    # key will be valid as long as the animation lives.
    _animation_dict = {}

    def __init__(self, object, tween='linear', duration=1, on_finished=None,
                 **targets):
        self.targets = targets
        try:
            self.function = TWEEN_FUNCTIONS[tween]
        except KeyError:
            suggested_tween = suggest(tween, TWEEN_FUNCTIONS.keys())
            if len(suggested_tween) > 0:
                raise KeyError(
                    'No tween called %s found, did you mean %s?'
                    % (tween, suggested_tween[0])
                )
            else:
                raise KeyError('No tween called %s found.' % tween)
        self.duration = duration
        self.on_finished = on_finished
        self.t = 0
        self.object = object
        self.initial = {}
        self._running = True
        for k in self.targets:
            try:
                a = getattr(object, k)
            except AttributeError:
                raise ValueError(
                    'object %r has no attribute %s to animate' % (object, k)
                )
            self.initial[k] = a
            key = id(object), k
            previous_animation = self._animation_dict.get(key)
            if previous_animation is not None:
                previous_animation._remove_target(k)
            self._animation_dict[key] = self
        each_tick(self.update)
        self.animations.append(self)

    @property
    def running(self):
        """Running state of the animation.

        True if the animation is running.
        False if the duration has elapsed or the stop() method was called.
        """
        return self._running

    def update(self, dt):
        self.t += dt
        n = self.t / self.duration
        if n > 1:
            n = 1
            self.stop(complete=True)
            if self.on_finished is not None:
                self.on_finished()
            return
        n = self.function(n)
        for k in self.targets:
            v = tween_attr(n, self.initial[k], self.targets[k])
            setattr(self.object, k, v)

    def stop(self, complete=False):
        """Stop the animation, optionally completing the transition to the final
        property values.

        :param complete: If True, the object will have its targets
            set to their final values for the animation. If not, the
            targets will be set to some value between the start and
            end values.
        """
        if not self._running:
            # Don't do anything if already stopped.
            return

        self._running = False
        if complete:
            for k in self.targets:
                setattr(self.object, k, self.targets[k])
        for k in list(self.targets):
            self._remove_target(k, stop=False)
        unschedule(self.update)
        self.animations.remove(self)

    def _remove_target(self, target, stop=True):
        del self.targets[target]
        del self._animation_dict[id(self.object), target]
        if not self.targets and stop:
            self.stop()

class ImageAnimation:
    _ACTOR_PROPERTIES = {'actor_x', 'actor_y'}
    def __init__(self, actor, images, alt_images=None, every=1.0, source=None,
            autostart=True, limit=None, on_finished=None):
        self.actor = actor
        self.main_images = images
        self.alt_images = alt_images or []
        self._images = images
        self.freq = every
        self.value = 0
        self.count = len(images)
        self._update_value = self._update_direct
        self.running = False
        self.limit = limit
        self.on_finished = on_finished
        self.finished = False
        self.source = source
        if not source:
            # No external source - update() must be called manually
            return
        elif source in self._ACTOR_PROPERTIES:
            self._update_value = self._update_property(source)
        elif source != 'clock':
            raise TypeError("invalid source: {}".format(source))
        self.direct_updates_only = False
        if autostart:
            self.start()

    def update(self, dv=1):
        last_value = self.value
        self._update_value(dv)
        if self.alt_images:
            if self.value > last_value:
                self._images = self.alt_images
            elif self.value < last_value:
                self._images = self.main_images
        index = int(self.value // self.freq) % self.count
        self.actor.image = self._images[index]
        if self.limit \
                and self.value / (self.count * self.freq - dv) >= self.limit:
            self._stop(finished=True)

    def start(self):
        if not self.source:
            raise ValueError("start() not supported without a source")
        if not self.finished:
            each_tick(self.update)
            self.running = True

    def stop(self):
        if not self.source:
            raise ValueError("stop() not supported without a source")
        self._stop(finished=False)

    def next(self):
        self.update(self.freq)

    def prev(self):
        self.update(-self.freq)

    def _update_direct(self, dv):
        self.value += dv

    def _update_property(self, actor_property):
        _, prop_name = actor_property.split('_', 1)
        def update_func(dv):
            self.value = getattr(self.actor, prop_name)
        return update_func

    def _stop(self, finished):
        if not self.finished:
            unschedule(self.update)
            self.running = False
        if finished and self.on_finished:
            self.on_finished()
            self.finished = True


def animate(object, tween='linear', duration=1, on_finished=None, **targets):
    return Animation(object, tween, duration, on_finished=on_finished,
                     **targets)

def _images(actor, images, alt_images=None, every=1.0, source=None,
        autostart=True, limit=None, on_finished=None):
    return ImageAnimation(actor, images, alt_images, every, source,
            autostart, limit, on_finished)
animate.images = _images
