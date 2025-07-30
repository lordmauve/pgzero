Contributing to Pygame Zero
===========================

.. highlight:: none

The Pygame Zero project is hosted on GitHub:

    https://github.com/lordmauve/pgzero

.. _report-issue:

Reporting an bug or request
---------------------------

You can report bugs, or request features that you think should be in Pygame
Zero, using the `Github issue tracker`_.

Here are some things to bear in mind before you do this:

* It might not just be you! You should check if someone has already reported
  the issue by searching through the existing issues - both open and closed.

* The developers need to know what version of Pygame Zero you are using, and
  what operating system you are running (Windows, Mac, Linux etc) and version
  (Windows 10, Ubuntu 16.04, etc).


.. _`Github issue tracker`: https://github.com/lordmauve/pgzero/issues


How to do a pull request
------------------------

You can make changes to Pygame Zero by creating a pull request.

It's a good idea to :ref:`report an issue <report-issue>` first, so that we can
discuss whether your change makes sense.

Github has `help on how to create a pull request`__, but here's the quick
version:

.. __: https://help.github.com/articles/creating-a-pull-request/

1. Make sure you are logged into Github.
2. Go to the `Github page for Pygame Zero`_.
3. Click "Fork" to create your own fork of the repository.
4. Clone this fork to your own computer::

        git clone git@github.com:yourusername/pgzero.git

   Remember to change ``yourusername`` to your Github username.

5. Create a branch in which to do your changes. Pick a branch name that
   describes the change you want to make. ::

        git checkout -b my-new-branch master

6. Make the changes you want.
7. Add the files that you want to commit::

        git add pgzero

8. Commit the files with a clear commit message::

        git commit -m "Fixed issue #42 by renaming parameters"

   You can do steps 6 to 8 as many times as you want until you're happy.

9. Push the commit back to your fork. ::

        git push --set-upstream origin my-new-branch

10. Go to the Github page for your fork, and click on the "Create pull request"
    button.


.. _`Github page for Pygame Zero`: https://github.com/lordmauve/pgzero


Development installation
------------------------

It's possible to create a locally-editable install using ``uv``. From the root directory of the checked out source, run::

    uv sync --group dev

The installed version will now reflect any local changes you make.

When adding or upgrading dependencies, regenerate ``uv.lock`` with::

    uv lock

and commit the updated lock file.

Alternatively, if you don't want to install it at all, it may be run with:

   python3 -m pgzero <name of pgzero script>

For example:

   python3 -m pgzero examples/basic/demo1.py


How to run tests
----------------

The tests require an X server and Pulseaudio to be available. On most Linux
systems you can run them with::

    export XDG_RUNTIME_DIR=/tmp
    pulseaudio -D --start
    xvfb-run --auto-servernum pytest


.. _translating:

Helping to translate the documentation
--------------------------------------

Pygame Zero's APIs will always be English, but we can bring Pygame Zero to more
users around the world if the documentation is available in their language.

If you are fluent in another language, please consider contributing by
translating all or part of the documentation.

The documentation is written in reStructuredText_, which is a text-based markup
language for technical documentation. As much as possible, the existing
formatting should be preserved. reStructuredText isn't too difficult once you
get used to it.

Creating a translation is done by creating a separate repository on Github with
a copy of the documentation, rewritten (at least in part) into the language you
would like to support. One advantage of this is that you can work on
translations at your own pace, without having to submit pull requests back to
the ``pgzero`` project itself. Please see the `translation guide`_ on Read The
Docs for details.

If this sounds like something you could tackle, here's how you might go about
it:

1. First, open an issue on the `pgzero issue tracker`_. You should search for
   an existing issue covering the translation you want to do, before opening a
   new one. This will help ensure that you don't do translation work that has
   already been done by someone else (perhaps you can collaborate instead).
2. Create a new Github repository under your user, called pgzero-*language*,
   eg. ``pgzero-spanish`` if you're going to translate into Spanish.
3. Clone the repository to your own computer.
4. Download the Pygame Zero ``doc/`` directory and commit it in your project.
   You can do this by extracting them from `repository ZIP file`_. You only
   need the ``doc/`` directory from the ZIP file. You can delete the other
   files.
5. Now, work through the .rst files in the docs directory, translating, using
   your preferred editor. You should commit regularly, and push your commits to
   Github.
6. Post a link to your repository as a comment in the Github issue you created
   in step 1. You can do this as soon as you have some progress to show; this
   will help people collaborate with you on the translation if they are
   interested.
7. `Set up the documentation to build on Read The Docs`__. Again, post a
   comment on the Github issue when you have this working.
8. We can then link up the new, translated documentation with the Pygame Zero
   documentation.

.. _reStructuredText: http://www.sphinx-doc.org/en/master/rest.html
.. _`translation guide`: https://docs.readthedocs.io/en/latest
                         /localization.html#project-with-multiple-translations
.. _`pgzero issue tracker`: https://github.com/lordmauve/pgzero/issues/new
.. _`repository ZIP file`: https://github.com/lordmauve/pgzero/archive/master.zip

.. __: https://docs.readthedocs.io/en/latest/getting_started.html#import-your-docs

Note that Pygame Zero will have updates, and the documentation will be changed
accordingly. Using Git it is possible to see a diff of what changed in the
English documentation, so that you can make corresponding changes in the
translated documentation.
