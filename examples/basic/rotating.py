WIDTH = HEIGHT = 400

alien = Actor('alien', center=(300, 300), anchor=('center', 0.25))


def update():
    alien.angle += 1


def draw():
    screen.clear()
    alien.draw()
