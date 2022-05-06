from scipy.io import savemat
import numpy as np
filename = 'randomInputData.mat'
N = 100
D = 5
mydict = {}
mydict['X'] = np.random.rand(N, D)
mydict['Y'] = mydict['X'] @ np.random.rand(D, ) + np.random.normal(0, 0.4, (N,))

savemat(filename, mydict)