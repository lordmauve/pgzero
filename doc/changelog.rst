Changelog
=========

1.1 - pending
-------------

* Added a spell checker that will point out hook or parameter names that have
  been misspelled when the program starts.
* New ZRect built-in class, API compatible with Rect, but which accepts
  coordinates with floating point precision.
* Refactor of built-in ``keyboard`` object to fix attribute case consistency.
  This also allows querying key state by ``keys`` constants, eg.
  ``keyboard[keys.LEFT]``.
* Provide much better information when sound files are in an unsupported
  format.
* It is now possible to assign arbitrary attibutes on the built-in Rect object.
* ``screen.blit()`` now accepts an image name string as well as a Surface
  object, for consistency with Actor.
* Fixed a bug with non-focusable windows and other event bugs when running in
  a virtualenv on Mac OS X.
* Actor can now be positioned by any of its border points (eg. ``topleft``,
  ``midright``) directly in the constructor.


1.0.2 - 2015-06-04
------------------

* Fix: ensure compatibility with Python 3.2

1.0.1 - 2015-05-31
------------------

This is a bugfix release.

* Fix: Actor is now positioned to the top left of the window if ``pos`` is
  unspecified, rather than appearing partially off-screen.

* Fix: repeating clock events can now unschedule/reschedule themselves

  Previously a callback that tried to unschedule itself would have had no
  effect, because after the callback returns it was rescheduled by the clock.

  This applies also to ``schedule_unique``.

* Fix: runner now correctly displays tracebacks from user code

* New: Eliminate redraws when nothing has changed

  Redraws will now happen only if:

      * The screen has not yet been drawn
      * You have defined an update() function
      * An input event has been fired
      * The clock has dispatched an event


1.0 - 2015-05-29
----------------

* New: Added ``anchor`` parameter to Actor, offering control over where its
  ``pos`` attribute refers to. By default it now refers to the center.

* New: Added Ctrl-Q/⌘-Q as a hard-coded keyboard shortcut to exit a game.

* New: ``on_mouse_*`` and ``on_key_*`` receive ``IntEnum`` values as ``button``
  and ``key`` parameters, respectively. This simplifies debugging and enables
  usage like::

        if button is button.LEFT:


1.0beta1 - 2015-05-19
---------------------

Initial public (preview) release.
