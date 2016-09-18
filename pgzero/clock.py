"""Clock/event scheduler.

This is a Pygame implementation of a scheduler inspired by the clock
classes in Pyglet.

"""
import heapq
from weakref import ref
from functools import total_ordering
from types import MethodType

__all__ = [
    'Clock', 'schedule', 'schedule_interval', 'unschedule'
]


def weak_method(method):
    """Quick weak method ref in case users aren't using Python 3.4"""
    selfref = ref(method.__self__)
    funcref = ref(method.__func__)

    def weakref():
        self = selfref()
        func = funcref()
        if self is None or func is None:
            return None
        return func.__get__(self)
    return weakref


def mkref(o):
    if isinstance(o, MethodType):
        return weak_method(o)
    else:
        return ref(o)


@total_ordering
class Event:
    """An event scheduled for a future time.

    Events are ordered by their scheduled execution time.

    """
    def __init__(self, time, cb, repeat=None):
        self.time = time
        self.repeat = repeat
        self.cb = mkref(cb)
        self.name = str(cb)
        self.repeat = repeat

    def __lt__(self, ano):
        return self.time < ano.time

    def __eq__(self, ano):
        return self.time == ano.time

    @property
    def callback(self):
        return self.cb()


class Clock:
    """A clock used for event scheduling.

    When tick() is called, all events scheduled for before now will be called
    in order.

    tick() would typically be called from the game loop for the default clock.

    Additional clocks could be created - for example, a game clock that could
    be suspended in pause screens. Your code must take care of calling tick()
    or not. You could also run the clock at a different rate if desired, by
    scaling dt before passing it to tick().

    """
    def __init__(self):
        self.t = 0
        self.fired = False
        self.events = []
        self._each_tick = []

    def schedule(self, callback, delay):
        """Schedule callback to be called once, at `delay` seconds from now.

        :param callback: A parameterless callable to be called.
        :param delay: The delay before the call (in clock time / seconds).

        """
        heapq.heappush(self.events, Event(self.t + delay, callback, None))

    def schedule_unique(self, callback, delay):
        """Schedule callback to be called once, at `delay` seconds from now.

        If it was already scheduled, postpone its firing.

        :param callback: A parameterless callable to be called.
        :param delay: The delay before the call (in clock time / seconds).

        """
        self.unschedule(callback)
        self.schedule(callback, delay)

    def schedule_interval(self, callback, delay):
        """Schedule callback to be called every `delay` seconds.

        The first occurrence will be after `delay` seconds.

        :param callback: A parameterless callable to be called.
        :param delay: The interval in seconds.

        """
        heapq.heappush(self.events, Event(self.t + delay, callback, delay))

    def unschedule(self, callback):
        """Unschedule the given callback.

        If scheduled multiple times all instances will be unscheduled.

        """
        self.events = [e for e in self.events if e.callback != callback and e.callback is not None]
        heapq.heapify(self.events)
        self._each_tick = [e for e in self._each_tick if e() != callback]

    def each_tick(self, callback):
        """Schedule a callback to be called every tick.

        Unlike the standard scheduler functions, the callable is passed the
        elapsed clock time since the last call (the same value passed to tick).

        """
        self._each_tick.append(mkref(callback))

    def _fire_each_tick(self, dt):
        dead = [None]
        for r in self._each_tick:
            cb = r()
            if cb is not None:
                self.fired = True
                try:
                    cb(dt)
                except Exception:
                    import traceback
                    traceback.print_exc()
                    dead.append(cb)
        self._each_tick = [e for e in self._each_tick if e() not in dead]

    def tick(self, dt):
        """Update the clock time and fire all scheduled events.

        :param dt: The elapsed time in seconds.

        """
        self.fired = False
        self.t += float(dt)
        self._fire_each_tick(dt)
        while self.events and self.events[0].time <= self.t:
            ev = heapq.heappop(self.events)
            cb = ev.callback
            if not cb:
                continue

            if ev.repeat is not None:
                self.schedule_interval(cb, ev.repeat)

            self.fired = True
            try:
                cb()
            except Exception:
                import traceback
                traceback.print_exc()
                self.unschedule(cb)


# One instance of a clock is available by default, to simplify the API
clock = Clock()
tick = clock.tick
schedule = clock.schedule
schedule_interval = clock.schedule_interval
schedule_unique = clock.schedule_unique
unschedule = clock.unschedule
each_tick = clock.each_tick
