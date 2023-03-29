import subprocess
import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import argparse

def run(file):
    nx = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400]
    ny = [int(3*ii//4) for ii in nx]
    single_core = []
    for ii in nx:
        cmd = [sys.executable, file, '-n', str(ii)]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output = p.communicate()[0]
        output = output.decode('utf-8')
        single_core.append(float(output.split()[-1]))
        print("Single core: {}".format(ii))
    multi_core = []
    for ii in nx:
        cmd = [sys.executable, file, '-n', str(ii), '--openmp']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output = p.communicate()[0]
        output = output.decode('utf-8')
        multi_core.append(float(output.split()[-1]))
        print("Multi core: {}".format(ii))
    sz = [nx[i]*ny[i] for i in range(len(nx))]
    return sz, single_core, multi_core

def plot(sz, single_core, multi_core):
    plt.figure(figsize=(8, 6))
    plt.plot(sz, single_core, label='Single core')
    plt.plot(sz, multi_core, label='Multi core')
    plt.xlabel('Size of matrix(num_rows x num_columns)')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.savefig('mandelbrot.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', action='store', dest='file',
                        default='mandelbrot_cpu.py', help='File to run')
    
    arg = parser.parse_args()
    file = arg.file
    output = run(file)
    sz, single_core, multi_core = output
    plot(sz, single_core, multi_core)

