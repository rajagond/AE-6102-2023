import numpy as np
import time
import matplotlib.pyplot as plt
import numba

@numba.jit
def cal(N):
    a = np.random.rand(N).astype(np.float64)
    b = np.random.rand(N).astype(np.float64)
    x = np.random.rand(N).astype(np.float64)
    y = np.empty(N, dtype=np.float64)
    y = ((a*a*b + a*x*x + b*x*b - y*a*b) + ((b*x*y + a*b)*(x*b + b*a)*(b - a*y)*(a*b - x*y)))*(a*x + b)*(a + b)


def gflops_count(N):
    start_time = time.perf_counter()
    cal(N)
    end_time =  time.perf_counter()
    time_taken = end_time - start_time
    # 32 flops per loop * N loops 
    gflops = ((32 * N) / time_taken) / 1e9 
    return gflops

def graph_gflops():
    #warm up
    cal(1000)
    lst = [pow(2, i) for i in range(3, 27)]
    gflops_list = [gflops_count(N) for N in lst]
    plt.plot(lst, gflops_list, 'o-', color='r')
    plt.xscale('log')
    plt.xlabel('N')
    plt.ylabel('GFLOPS')
    plt.title('GFLOPS vs N')
    plt.grid()
    plt.savefig('gflops.png')


if __name__ == '__main__':
    graph_gflops()
