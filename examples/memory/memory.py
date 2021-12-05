#
# TODO: Add sound effects
#       Ignore clicks after displaying second card until
#       either hit or miss is reported.
#       Consider re-casting the data structure as a dict
#       with two-element tuple keys.
#       Configure window size according to COLS and ROWS
#
import random

checkmark = Actor('checkmark')
steve = Actor('card_back', (50, 50))
steve.topleft = (0, 0)

COLS = 4
ROWS = 3
IMSIZE = 200
STATUS = []        # cells that have been clicked on
ignore = []        # cells that have been matches and are no longer in play

# Create two of each card image, then randomize before creating the board
START_IMAGES = ["im" + str(i + 1) for i in range(COLS * ROWS // 2)] * 2
random.shuffle(START_IMAGES)

STATUS = []

board = []                    # initialize the board
for row in range(ROWS):
    new_row = []
    for col in range(COLS):
        image_name = START_IMAGES.pop()
        temp = Actor(image_name, (col*IMSIZE, row*IMSIZE))
        temp.image_name = image_name  # used to verify matches
        temp.topleft = (col*IMSIZE, row*IMSIZE)
        new_row.append(temp)
    board.append(new_row)


def draw():                    # draw the board when pygame-zero says to
    screen.clear()
    for row in range(ROWS):
        for col in range(COLS):
            if (row, col) in ignore:    # already matched
                checkmark.topleft = IMSIZE*col, IMSIZE*row
                checkmark.draw()
            elif (row, col) in STATUS:    # clicked this move: show face
                board[row][col].draw()
            else:                        # regular clickable card
                steve.topleft = IMSIZE*col, IMSIZE*row
                steve.draw()


def find_tile(pos):
    y, x = pos
    result = x // IMSIZE, y // IMSIZE
    return result


def show_tile():
    pass


def on_mouse_down(pos, button):
    if len(STATUS) == 2:  # ignore until timeout redisplays
        return
    if pos in ignore:  # has already been matched
        return
    if button == mouse.LEFT:
        coords = find_tile(pos)
        if coords not in STATUS:
            STATUS.append(coords)  # now they are
            if len(STATUS) == 1:  # 1st click - turn not yet over
                pass
            elif len(STATUS) == 2:  # 2nd click - check for match
                (x1, y1), (x2, y2) = STATUS  # an "unpacking assignment"
                if board[x1][y1].image_name == board[x2][y2].image_name:
                    print("Success sound")
                    # add cards to list of non-clickable positions
                    for pos in STATUS:
                        ignore.append(pos)
                else:
                    print("Failure sound")
                clock.schedule_unique(next_turn, 2.0)


def next_turn():
    del STATUS[:]
