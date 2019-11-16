"""Generate plots of the tweeners, to include in docs."""

from matplotlib import pyplot as plt
import numpy as np

from pgzero import animation

IMAGE_SIZE = 64, 64


def plot(f, filename):
    num_points = 256
    x = np.linspace(0, 1, num_points)
    y = np.vectorize(f)(x)
    plt.figure(figsize=(3, 1.5), dpi=num_points)
    plt.axis('off')
    plt.plot(x, y, color='#3a76a8')
    plt.tight_layout()
    plt.savefig(filename, dpi=num_points)
    plt.close()


if __name__ == '__main__':
    for name, f in animation.TWEEN_FUNCTIONS.items():
        filename = 'images/{}.png'.format(name)
        plot(f, filename)
