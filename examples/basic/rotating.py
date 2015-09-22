WIDTH = HEIGHT = 400

alien = Actor('alien', center=(200, 200), anchor=('center', 30))


def update():
    alien.angle += 1


def draw():
    screen.clear()
    alien.draw()
