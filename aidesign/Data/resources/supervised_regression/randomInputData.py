import numpy as np
import pandas as pd
from pathlib import Path  

N = 100
D = 5

X = np.random.rand(N, D)
Y = X @ np.random.rand(D, 1) + np.random.normal(0, 2, (N, 1))

X_tr, Y_tr = pd.DataFrame(X[:int(N*0.6),:]), pd.DataFrame(Y[:int(N*0.6)])
X_tst, Y_tst = pd.DataFrame(X[int(N*0.6):,:]), pd.DataFrame(Y[int(N*0.6):])

filepath = Path('Data/X_tr.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
X_tr.to_csv(filepath, index = False)
filepath = Path('Data/Y_tr.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
Y_tr.to_csv(filepath, index = False)
filepath = Path('Data/X_tst.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
X_tst.to_csv(filepath, index = False)
filepath = Path('Data/Y_tst.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
Y_tst.to_csv(filepath, index = False)