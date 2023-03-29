import time
import numpy as np
import matplotlib.pyplot as plt
from compyle.api import annotate, elementwise, get_config, wrap, declare
from compyle.utils import ArgumentParser

@annotate(i='int', z='intp', xa='doublep', ya='doublep', max_iters='int')
def mandelbrot(i, z, xa, ya, max_iters):
    # x0 = xa[i]
    # y0 = ya[i]
    x = declare('double')
    y = declare('double')
    x = 0.0
    y = 0.0
    iters = declare('int')
    iters = 0
    while (x*x + y*y) < 4 and iters < max_iters:
        xn = x*x - y*y + xa[i]
        y = x*y*2.0 + ya[i]
        x = xn
        iters += 1
    z[i] = iters

def mandelbrot_using_numpy(i, z, xa, ya, max_iters):
    x = 0.0
    y = 0.0
    iters = 0
    while (x*x + y*y) < 4 and iters < max_iters:
        xn = x*x - y*y + xa[i]
        y = x*y*2.0 + ya[i]
        x = xn
        iters += 1
    z[i] = iters

def plot(result):
    plt.figure(figsize=(8, 6))
    plt.imshow(result.T, extent=[-2.5, 1.5, -1.5, 1.5])
    plt.show()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-n', action='store', type=int, dest='n',
                        default=512, help='Number of grid points in x.')
    parser.add_argument(
        '--show', action='store_true', dest='show',
        default=False, help='matplotlib plot')
    parser.add_argument(
        '--max-iters', action='store', dest='max_iters',
        default=20, help='Maximum number of iterations')

    cfg = get_config()
    cfg.suppress_warnings = True
    arg = parser.parse_args()

    mandelbrot = elementwise(mandelbrot)
    nx = arg.n
    ny = int(3*nx//4)
    x, y = np.mgrid[-2.5:1.5:nx*1j, -1.5:1.5:ny*1j]
    x, y = x.ravel(), y.ravel()
    z = np.zeros_like(x, dtype=np.int32)
    max_iters = arg.max_iters
    num_loops = len(x)
    # s = time.perf_counter()
    # for i in range(num_loops):
    #     mandelbrot_using_numpy(i, z, x, y, max_iters)
    # t = time.perf_counter() - s
    # print(t)
    x, y, z = wrap(x, y, z)
    s = time.perf_counter()
    for i in range(num_loops):
        mandelbrot(z, x, y, max_iters)
    t = time.perf_counter() - s
    print(t)
    result = np.array(z).reshape((nx, ny))

    if arg.show:
        plot(result)