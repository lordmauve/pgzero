# Easing Functions ported from the Clutter Project via http://kivy.org/
#  http://www.clutter-project.org/docs/clutter/stable/ClutterAlpha.html


from math import sin, pow, pi

from .clock import each_tick, unschedule

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
        return tuple(tween(n, a, b) for a,b in zip(start, end))
    elif isinstance(start, list):
        return [tween(n, a, b) for a,b in zip(start, end)]
    else:
        return tween(n, start, end)


class Animation:
    animations = []

    def __init__(self, object, type='linear', duration=1, **kw):
        self.targets = kw
        self.function = TWEEN_FUNCTIONS[type]
        self.duration = duration
        self.t = 0
        self.object = object
        self.initial = {}
        for k in self.targets:
            try:
                a = getattr(object, k)
            except AttributeError:
                raise ValueError('object %r has no attribute %s to animate' % (object, k))
            self.initial[k] = a
        each_tick(self.update)
        self.animations.append(self)

    def update(self, dt):
        self.t += dt
        n = self.t / self.duration
        if n > 1:
            n = 1
            unschedule(self.update)
            self.animations.remove(self)
        n = self.function(n)
        for k in self.targets:
            v = tween_attr(n, self.initial[k], self.targets[k])
            setattr(self.object, k, v)
