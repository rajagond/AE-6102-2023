import argparse
import numpy as np
import time
import numba


@numba.njit
def nloop(T, niter):
    for _ in range(niter):
        N = T.shape[0]
        T_new = np.empty_like(T)
        for i in range(1, N-1):
            for j in range(1, N-1):
                T_new[i, j] = 0.25*(T[i-1, j] + T[i+1, j] + T[i, j-1]
                                              + T[i, j+1])
        for i in range(1, N-1):
            for j in range(1, N-1):
                T[i, j] = T_new[i, j]


@numba.njit
def narray_loop(T, niter):
    for _ in range(niter):
        T[1:-1, 1:-1] = 0.25*(T[2:, 1:-1] + T[:-2, 1:-1] + T[1:-1, 2:]
                                          + T[1:-1, :-2])


def array_loop(T, niter):
    for _ in range(niter):
        T[1:-1, 1:-1] = 0.25*(T[2:, 1:-1] + T[:-2, 1:-1] + T[1:-1, 2:]
                                          + T[1:-1, :-2])


def jacobi(size, niter, procedure, output):
    T = np.zeros((size, size))
    T[0] = 100
    T[:, -1] = 100
    if procedure == "loop":
        T_prime = T.copy()
        nloop(T_prime, 5)  # warm up
        start = time.perf_counter()
        nloop(T, niter)
        end = time.perf_counter()
        print(end-start)
    elif procedure == "numba":
        T_prime = T.copy()
        narray_loop(T_prime, 5)  # warm up
        start = time.perf_counter()
        narray_loop(T, niter)
        end = time.perf_counter()
        print(end-start)
    elif procedure == "numpy":
        T_prime = T.copy()
        array_loop(T_prime, 5)  # warm up
        start = time.perf_counter()
        array_loop(T, niter)
        end = time.perf_counter()
        print(end-start)
    else:
        raise ValueError("Invalid procedure: {}".format(procedure))
    if output:
        np.savez(output, T)


# main function
if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(prog="jacobi", description="AE6102-A5")
    # Add the arguments
    parser.add_argument("--size", type=int, required=True, help="Grid size")
    nIter = "Number of iterations"
    parser.add_argument("-n", "--niter", type=int, required=True, help=nIter)
    choices = ["loop", "numba", "numpy"]
    parser.add_argument("--procedure", choices=choices, required=True)
    parser.add_argument("-o", type=str, help="output file")

    # Parse the arguments
    args = parser.parse_args()

    # Call the function to perform the operation
    jacobi(args.size, args.niter, args.procedure, args.o)
