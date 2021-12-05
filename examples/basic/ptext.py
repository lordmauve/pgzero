# Example game using text rendering

WIDTH = sx = 854
HEIGHT = sy = 480
TITLE = "Clooky Clunker"

score, totalscore, clunkers = 0, 0, 0
nextgoal = 0
tgoal = -100
clunks = []
tbuy, buytext = -100, ""
t = 0

buttonrects = [Rect((50, 120 + 85 * j, 180, 70)) for j in range(4)]
buttonnames = ["auto-clunker", "clunkutron",
               "turbo enclunkulator", "clunx capacitor"]
buttoncosts = [10, 400, 12000, 250000]


def on_key_down(key):
    if key == keys.ESCAPE:
        exit()


def on_mouse_down(button, pos):
    global score, totalscore, clunkers, tbuy, buytext
    if button != 1:
        return

    x, y = pos
    # Click on the central circle
    if (x - sx / 2) ** 2 + (y - sy / 2) ** 2 < 100 ** 2:
        score += 1
        totalscore += 1
        # Add a "clunk" indicator at a pseudorandom place near the center
        ix = sx / 2 + 12345678910. / (1 + t) % 1 * 200 - 100
        iy = sy / 2 + 45678910123. / (1 + t) % 1 * 200 - 100
        clunks.append((t, ix, iy))

    # Click on one of the buttons
    for j in range(len(buttonrects)):
        rect, cost = buttonrects[j], buttoncosts[j]
        if rect.collidepoint(x, y) and score >= cost:
            score -= cost
            clunkers += 10 ** j
            tbuy = t
            buytext = "+%s clunk/s" % (10 ** j)
            buttoncosts[j] += int(round(cost * 0.2))


def update(dt):
    global t
    global score, totalscore, goaltext, tgoal, nextgoal
    t += dt
    score += clunkers * dt
    totalscore += clunkers * dt

    # Check for next achievement
    if totalscore > 100 * (1 << nextgoal):
        goaltext = "Achievement unlocked:\nCL%sKY!" % ("O" * (nextgoal + 2))
        tgoal = t
        nextgoal += 1

    clunks[:] = [c for c in clunks if t - c[0] < 1]


def draw():
    screen.fill((0, 30, 30))

    # Draw the circle in the middle
    screen.draw.filled_circle((sx // 2, sy // 2), 106, 'black')
    screen.draw.filled_circle((sx // 2, sy // 2), 100, '#884400')

    # Draw the buttons using screen.draw.textbox
    for rect, name, cost in zip(buttonrects, buttonnames, buttoncosts):
        screen.draw.filled_rect(rect, "#553300")
        screen.draw.filled_rect(rect.inflate(-8, -8), "#332200")
        text = u"%s: %d\u00A0clunks" % (name, cost)
        color = "white" if cost <= score else "#666666"
        box = rect.inflate(-16, -16)
        screen.draw.textbox(
            text, box,
            fontname="bubblegum_sans",
            lineheight=0.9,
            color=color,
            owidth=0.5
        )

    # Draw the HUD
    hudtext = "\n".join([
        "time played: %d" % t,
        "clunks: %d" % score,
        "all-time clunks: %d" % totalscore,
        "clunks per second: %d" % clunkers,
    ])
    screen.draw.text(
        hudtext,
        right=sx - 10,
        top=120,
        fontname="roboto_condensed",
        fontsize=32,
        color=(0, 200, 0),
        scolor=(0, 50, 0),
        shadow=(-1, 1),
        lineheight=1.3
    )

    # Draw the title using a gradient
    screen.draw.text(
        "Clooky Clunker",
        midtop=(sx / 2, 10),
        fontname="cherrycreamsoda",
        fontsize=64,
        owidth=1.2,
        color="#884400",
        gcolor="#442200"
    )

    # Draw "clunk" indicators
    for it, ix, iy in clunks:
        dt = t - it
        pos = ix, iy - 60 * dt
        screen.draw.text(
            "clunk",
            center=pos,
            fontname=None,
            fontsize=28,
            alpha=1 - dt,
            shadow=(1, 1)
        )

    # Draw purchase indicator
    if t - tbuy < 1:
        dt = t - tbuy
        pos = sx / 2, sy / 2
        fontsize = 32 * (1 + 60 * dt) ** 0.2
        screen.draw.text(
            buytext, pos,
            anchor=(0.5, 0.9),
            fontname="bubblegum_sans",
            fontsize=fontsize,
            alpha=1 - dt,
            shadow=(1, 1)
        )

    # Draw achievement unlocked text (text is centered even though we specify
    # bottom right).
    if t - tgoal < 2:
        alpha = min(2 - (t - tgoal), 1)
        screen.draw.text(
            goaltext,
            fontname="boogaloo",
            fontsize=48,
            bottom=sy - 20,
            right=sx - 40,
            color="#AAAAFF",
            gcolor="#4444AA",
            shadow=(1.5, 1.5),
            alpha=alpha,
            align="center"
        )
