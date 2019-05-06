"""Generate plots of the tweeners, to include in docs."""

from matplotlib import pyplot as plt
import numpy as np

from pgzero import animation

IMAGE_SIZE = 64, 64

def plot(f, filename):
    num_points = 64
    ix = np.array(range(num_points))
    x = ix/num_points
    y = np.vectorize(f)(x)
    plt.tight_layout()
    plt.figure(figsize=(1,1), dpi=num_points)
    plt.axis('off')
    plt.plot(x, y)
    plt.savefig(filename, dpi=num_points)
    plt.close()


if __name__ == '__main__':
    for name, f in animation.TWEEN_FUNCTIONS.items():
        filename = 'doc/images/{}.png'.format(name)
        plot(f, filename)
        #resize(filename)
