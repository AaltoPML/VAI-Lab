from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
from matplotlib import pyplot as plt

_PLUGIN_CLASS_NAME = "Regression"
_PLUGIN_CLASS_DESCRIPTION = "Regression ML model placeholder"
_PLUGIN_READABLE_NAMES = {"default":"regression","aliases":["reg"]}
_PLUGIN_MODULE_OPTIONS = {}
_PLUGIN_REQUIRED_SETTINGS = {}
_PLUGIN_OPTIONAL_SETTINGS = {}

class Regression(object):
    def __init__(self):
        self.input_data = None
        self.target_data = None
        self.fit_degree = 1
        self.regression_function = linear_model.LinearRegression()

    def set_input_data(self,data):
        self.input_data = data

    def set_target_data(self,data):
        self.target_data = data

    def _reshape(self,data,shape):
        return data.reshape(shape[0],shape[1])

    def _is_shape_allowed(self,arr):
        return len(arr.shape) > 1 and len(arr.shape) <= 2

    def _convert_to_poly(self,data):
        self.poly = PolynomialFeatures(degree=self.fit_degree)
        if not self._is_shape_allowed(data):
            data = self._reshape(data,[len(data),1])
        return self.poly.fit_transform(data)

    def solve(self):
        in_data_poly = self._convert_to_poly(self.input_data)
        self.regression_function.fit(in_data_poly,self.target_data)

    def predict(self,data):
        data = self._convert_to_poly(data)
        return self.regression_function.predict(data)
        

# reg = Regression()

# X_train = np.array([1,2,3,4,5,6,7,8,9])
# y = X_train ** 5
# print(X_train)
# print(y)

# reg.set_input_data(X_train)
# reg.fit_degree = 1
# reg.set_target_data(y)
# reg.solve()

# X_test = X_train
# pred = reg.predict(X_test)
# print(pred)

# plt.figure()
# plt.plot(X_test,pred,c='r',label="Test Data. Degree: {0}".format(reg.fit_degree))
# plt.scatter(X_train,y,label="Training Data")
# plt.legend()
# plt.show()