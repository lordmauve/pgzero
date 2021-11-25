## “holdenwebs”

This game has been played ever since there were cards.
I don't know how long that is.
As a child I (holdenweb) became aware of the importance of
memory by playing games.

I used to watch a TV programme called "Picture Book" where
one of the regular features showed a scene with about ten objects
in it, and then asked you to name all the ones you could remember.
Because I was in love with the presenter (I was four, and Patricia
Driscoll must have been at least twenty-five) I wanted to do well.

This particular game is often played with cards.
My mother taught it calling it "Remembrance," but it
is also known as "Pairs" and (at least in America) as "Pelmanism."
There are probably many other names.
It's pretty simple: you click on cards to reveal them until you
manage to pair all the cards (I didn't mention there were two of
each card in the deck, did I?)

#### Game Play

The game is played on a rectangular board, with a grid of 200 x 200
"cards". When you click on a card its value is revealed. When you
click on a second card the same thing happens, and if the values
match they are removed from the game.

The object is to match all the cards as quickly as you can.

### Environment

This program started out at the June 2015 London Python Dojo, where we were
challenged to create programs for the "pygame-zero" environment.

[We need to add proper links and so on so someone who just comes
across this can find out how to install Python and pygame-zero.]

So it should run on most things, but it was originally
written on a Macintosh, though it's really targeted at
the Raspberry Pi. It's written in Python 3, as all new educational
Python programs should be, otherwise where are we going to find the
effort to convert all the Python 2? [Evangelism over].

### Architecture

The progam represents the board as a list of lists called `board`.

A list calles `STATUS` contains the co-ordinates of clicked cards.

A list called `ignore` contains the coordinates of cards that have
already been matched in the game and so should be ignored.

The game as originally published establishes a list of lists
to represent the board. The programmer can change the board
size by changing ROWS and COLUMNS, but the will then have to
make sure that they make the window the right size (we were
lucky the default window appears to be 800 x 600).

The `draw()` function clears the screen and then represents each
card as

 * The background image (currently a picture of @holdenweb)
   if it hasn't been matched or clicked on;

 * The card value image (stored in the `board` list) if it has
   been clicked on but not yet matched, or

 * A checkmark if it has been matched and is therefore no longer
   in play.

The `on_mouse_down()` function is activated when the user clicks
a mouse button. It looks at the `STATUS` list to determine
how many clicks the player has made this turn so far.

If the player has already clicked twice this turn it does nothing,
as it is waiting for the turn to be over. Otherwise the card
coordinates are added to `STATUS`.

If this is the first click, the function then simply returns.

If this is the second click, it checks whether the two cells have the
same image. If they don't it should play a depressing sound (though at
the moment it is boringly silent). If they do then it should (but again
doens't) play a cheerful sound, and adds both cells to the `ignore` list
so they cannot be selected in subsequent turns. Finally it sets a
two-second timeout so the player can see what happened.

The rest of the code just supports the functions described above.

### Status

The game as it stands is functionally complete but minimally playable.
The logic is intended to be simple and incomplete enough to it to
be fun for players to extend as they wish.
Some suggestions are listed below.

## Opportunities for Developer Players

The game has no sound effects, though `print` calls indicate where
the sounds should be emitted. This is a rewarding way to change the
game since at the moment it seems boring even to me.

There is no fanfare of trumpets when all cards are matched.
The program just continues to sit there.
It doesn't even terminate, which would be logical once there
is nothing more the player can achieve.

There is no instrumentation or scoring, which would be a major
way to add positive feedback for the player.

At the moment we select the cards on the board using `board[row][col]`.
It would be relatively easy to use a dict and use tuples as
indexes, allowing the use of `board[row, col]` instead.
A player familiar with Python might enjoy trying that as an
alternative.

When two cards are matched they currently turn checked immediately.
It would be better if the player actually saw the matching cards
for a while before play continued.

The graphics are unexciting, and those with an interest in such matters
should find it easy to replace the images with something that suits their
taste better. The programming world needs more people with a good sense
of visual design. You only have to look at the current graphics to see
that as a graphic artist I am quite a respectable plumber.

It's easy to adjust the timings of things, but it would be even easier
if the values were _manifest constants_ the same as ROWS and COLS, and
this would make the program logic easier to understand.
