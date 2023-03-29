import numpy as np
from numba import njit
import time
import matplotlib.pyplot as plt

def make_data(n):
    x = np.linspace(0, 2*np.pi, n)
    a, b = np.random.random((2, n))
    y = np.zeros_like(x)
    return y, x, a, b

@njit
def axpb(y, x, a, b):
    for i in range(y.shape[0]):
        y[i] = a[i]*x[i] + b[i]

def main():
    # warmup jit
    y, x, a, b = make_data(1000)
    axpb(y, x, a, b)
    # benchmark
    lst = [pow(2, i) for i in range(3, 27)]
    bandwidth_list = []
    for n in lst:
        y, x, a, b = make_data(n)
        s = time.perf_counter()
        axpb(y, x, a, b)
        e = time.perf_counter()
        elapsed = e - s
        bandwidth = ((n * 8) / elapsed)
        bandwidth_list.append(bandwidth)
    bandwidth_list_gb = [i/1e9 for i in bandwidth_list]
    plt.plot(lst, bandwidth_list, 'o-')
    plt.xscale('log')
    plt.title('Memory Bandwidth vs N')
    plt.xlabel('N')
    plt.yscale('log')
    plt.ylabel('Bandwidth (bytes/sec)')
    plt.grid()
    plt.savefig('memory_bandwidth_bytes.png')
    plt.clf()
    plt.plot(lst, bandwidth_list_gb, 'o-')
    plt.xscale('log')
    plt.title('Memory Bandwidth vs N')
    plt.xlabel('N')
    plt.ylabel('Bandwidth (GB/sec)')
    plt.grid()
    plt.savefig('memory_bandwidth.png')

if __name__ == '__main__':
    main()