Principles of Pygame Zero
=========================


Please read the following carefully before contributing.

Because Pygame Zero is aimed at beginners we must take extra care to avoid
introducting hurdles for programmers who have not yet learned to deal with
them.


Make it accessible
------------------

The main aim of Pygame Zero is to be accessible to beginner programmers.
The design of the API is, of course, influenced by this.

This also applies to things like hardware requirements: Pygame Zero chose
originally to support only keyboard and mouse input, in order to be accessible
to any user.


Be conservative
---------------

Early in the development of Pygame Zero, Richard and I (Daniel) went backwards
and forwards over various features. We put them in, tried them and took them
out again.

Features should be rejected if they are too experimental, or if they might
cause confusion.

This also applies to things like OS support: we disallow filenames that are
not likely to be compatible across operating systems.


Just Work
---------

Pygame Zero wraps Pygame almost completely - but we don't expose all the
features. We expose only the features that work really well without extra fuss,
and hide some of the other features that work less well or need extra steps.


Minimise runtime cost
---------------------

At the end of the day, Pygame Zero is a games framework and performance is an
issue.

Doing expensive checking every frame to catch a potential pitfall is not really
acceptable. Instead, we might check at start up time, or check only when an
exception is raised to diagnose it and report more information.


Error clearly
-------------

When exceptions are thrown by Pygame Zero, they should have clear error
messages that explain the problem.


Document well
-------------

Like all projects, Pygame Zero needs good documentation. Pull requests are more
likely to be accepted if they include the necessary documentation.

Try to avoid complicated sentences and technical terms in the documentation, so
that it is more easily readable by inexperienced programmers.


Minimise breaking changes
-------------------------

In educational environments, users don't always have control of the version of
a library they use. They don't know how to install or upgrade to the latest
version.

It is more important to get the features right first time than in many other
projects.
