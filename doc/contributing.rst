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

It's possible to create a locally-editable install using pip. From the root directory of the checked out source, run::

    pip3 install --editable .

The installed version will now reflect any local changes you make.

Alternatively, if you don't want to install it at all, it may be run with:

   python3 -m pgzero <name of pgzero script>

For example:

   python3 -m pgzero examples/basic/demo1.py


How to run tests
----------------

The tests can be run with

    python3 setup.py test
