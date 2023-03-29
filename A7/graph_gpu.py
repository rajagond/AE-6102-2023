# Time taken(y-axis) vs size of the matrix(x-axis) vs for openmp, cuda and opencl.

import os
import matplotlib.pyplot as plt

sz = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
backend = ['openmp', 'cuda', 'opencl']

plt.figure((8, 6))
for b in backend:
    time = []
    for s in sz:
        # run the file mandelbrot_cpu.py with n = s and backend = b
        # and store the time taken in time
        # time.append(....)
        output = os.popen('python mandelbrot_cpu.py -n {} --{}'.format(s, b)).read()
        time.append(float(output.split()[-1]))
    plt.plot(sz, time, label=b)
plt.legend()
plt.xlabel('Size of matrix(num_rows x num_columns)')
plt.ylabel('Time (s)')
plt.imread()
