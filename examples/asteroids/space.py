import random

from pygame import Surface, Rect

from pygame.constants import HWSURFACE, SRCALPHA


def create_star_scape(width, height):
    surf = Surface((width, height), flags=SRCALPHA | HWSURFACE)
    for i in range(random.randint(250, 350)):
        color = random.randint(100, 255)
        alpha = random.randint(0, 50)
        topleft = (random.randint(0, width), random.randint(0, height))
        surf.fill(
            color=([color] * 3) + [alpha],
            rect=Rect(
                (topleft[0] - 1, topleft[1] - 1),
                (3, 3),
            )
        )
        surf.fill(
            color=[color] * 3,
            rect=Rect(topleft, (1, 1))
        )
    return surf
