import numpy as np

tmp = np.load('tmp_numba.npz')
result = tmp['arr_0']
print(result)

tmp2 = np.load('tmp_numpy.npz')
result2 = tmp2['arr_0']
print(result2)