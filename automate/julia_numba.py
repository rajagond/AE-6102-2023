import argparse
import numpy as np
import numba
import time


@numba.njit
def numba_loop(Z, c, niter_max, div, result):
    for i in range(niter_max):
        for x in range(Z.shape[0]):
            for y in range(Z.shape[1]):
                if not div[x, y]:
                    Z[x, y] = Z[x, y]**2 + c[x, y]
                div[x, y] = np.abs(Z[x, y]) > 2
                if div[x, y] and result[x, y] == (niter_max - 1):
                    result[x, y] = i


def numpy_loop(Z, c, niter_max, div, result):
    for i in range(niter_max):
        Z[div == 0] = Z[div == 0]**2 + c[div == 0]
        div = np.abs(Z) > 2
        result[(div == 1) & (result == (niter_max - 1))] = i


def julia_set(x_pixels, niter_max=100, procedure=None, output_file=None):
    y_pixels = int(x_pixels * 0.75)
    nx, ny = x_pixels, y_pixels
    x, y = np.mgrid[-2.0:2.0:nx*1j, -1.5:1.5:ny*1j]
    Z = x + 1j*y
    c = np.full(Z.shape, -0.8 + 0.156j)
    result = np.ones((nx, ny))*(niter_max-1)
    div = np.ones_like(Z, dtype=bool)
    if procedure == "numba":
        # warm up
        z_copy = Z.copy()
        div_copy = div.copy()
        result_copy = result.copy()
        numba_loop(z_copy, c, 5, div_copy, result_copy)
        start = time.time()
        numba_loop(Z, c, niter_max, div, result)
        end = time.time()
        print(end - start)
    elif procedure == "numpy":
        # warm up
        z_copy = Z.copy()
        div_copy = div.copy()
        result_copy = result.copy()
        numpy_loop(z_copy, c, 5, div_copy, result_copy)
        start = time.time()
        numpy_loop(Z, c, niter_max, div, result)
        end = time.time()
        print(end - start)
    else:
        raise ValueError("No procedure specified")
    if output_file:
        np.savez(output_file, result)


# main function
if __name__ == "__main__":
    # parser
    parser = argparse.ArgumentParser(description="AE6102 - A5")
    # arguments
    parser.add_argument("-x", "--x-pixels", type=int, required=True)
    parser.add_argument("-n", "--niter-max", type=int, default=100)
    parser.add_argument("-o", type=str, help="output file")
    parser.add_argument("--procedure", choices=["numba", "numpy"])

    # Parse the arguments
    args = parser.parse_args()

    # Run the function
    julia_set(args.x_pixels, args.niter_max, args.procedure, args.o)
