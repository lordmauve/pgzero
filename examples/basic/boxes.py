WIDTH = 300
HEIGHT = 300


def make_rects():
    r = 255
    g = 0
    b = 0

    width = WIDTH
    height = HEIGHT - 200

    rects = []
    for i in range(20):
        rect = Rect((0, 0), (width, height))
        rect.color = (r, g, b)
        rect.center = 150, 150
        rects.append(rect)
        r -= 10
        g += 10

        width -= 10
        height += 10
    return rects


rects = make_rects()


def draw():
    for r in rects:
        screen.draw.rect(r, r.color)
