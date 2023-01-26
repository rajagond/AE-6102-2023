import argparse
import numpy as np
import matplotlib.pyplot as plt


def set_julia(x_pixels, niter_max=100, output_file=None):
    y_pixels = int(x_pixels * 0.75)
    nx, ny = x_pixels, y_pixels
    result = np.ones((nx, ny))*(niter_max-1)
    x, y = np.mgrid[-2.0:2.0:nx*1j, -1.5:1.5:ny*1j]
    Z = x + 1j*y
    c = np.full(Z.shape, -0.8 + 0.156j)
    div = np.ones_like(Z, dtype=bool)
    for i in range(niter_max):
        ndiv = ~div
        Z[ndiv] = Z[ndiv]**2 + c[ndiv]
        div = np.abs(Z) > 2
        result[div & (result == (niter_max - 1))] = i
    plt.figure(dpi=300)
    plt.imshow(result.T, extent=[-2.0, 2.0, -1.5, 1.5])
    plt.savefig("julia_set.png")
    if output_file:
        np.savez(output_file, result)


# main function
if __name__ == "__main__":
    # parser
    parser = argparse.ArgumentParser(description="AE6102 - A3")
    # arguments
    parser.add_argument("-x", "--x-pixels", type=int, required=True)
    parser.add_argument("-n", "--niter-max", type=int, default=100)
    parser.add_argument("-o", type=str, help="output file")

    # Parse the arguments
    args = parser.parse_args()
    set_julia(args.x_pixels, args.niter_max, args.o)
