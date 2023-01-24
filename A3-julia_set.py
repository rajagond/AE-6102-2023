import argparse
import numpy as np
import matplotlib.pyplot as plt


def set_julia(x_pixels, niters_max, output_file):
    y_pixels = int(x_pixels * 0.75)
    nx, ny = x_pixels, y_pixels
    result = np.zeros((nx, ny))
    x, y = np.mgrid[-2.0:2.0:nx*1j, -1.5:1.5:ny*1j]
    Z = x + 1j*y
    c = -0.8 + 0.156j  # constant value for Julia set
    for count in range(niters_max):
        Z = Z**2 + c
        cond = (np.abs(Z) >= 2) & (result < 1)
        result[cond] = count
        Z[np.abs(Z) >= 2] = 0.0
    result[(result < 1)] = niters_max - 1
    plt.figure(figsize=(8, 12))
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
    parser.add_argument("-n", "--niters-max", type=int, default=100)
    parser.add_argument("-o", type=str, help="output file")

    # Parse the arguments
    args = parser.parse_args()
    set_julia(args.x_pixels, args.niters_max, args.o)
