from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
from matplotlib import pyplot as plt

_PLUGIN_READABLE_NAMES = {"regression":"default","reg":"alias"}
_PLUGIN_MODULE_OPTIONS = {}
_PLUGIN_REQUIRED_SETTINGS = {"power":"int","train_name":"str","target_name":"str"}
_PLUGIN_OPTIONAL_SETTINGS = {}
_PLUGIN_REQUIRED_DATA = {"X","Y"}
_PLUGIN_OPTIONAL_DATA = {}

class Regression(object):
    """Regression for supervised training"""

    def __init__(self):
        self.input_data = None
        self.target_data = None
        self.fit_degree = 1
        self.regression_function = linear_model.LinearRegression()

    def set_data_in(self,data_in):
        req_check = [r for r in _PLUGIN_REQUIRED_DATA if r not in data_in.keys()]
        if len(req_check) > 0:
            raise Exception("Minimal Data Requirements not met"   \
                            +"\n\t{0} ".format(Regression) \
                            +"requires data: {0}".format(_PLUGIN_REQUIRED_DATA)\
                            + "\n\tThe following data is missing:"\
                            + "\n\t\u2022 {}".format(",\n\t\u2022 ".join([*req_check])))
        self._data_in = data_in

    def configure(self, config:dict):
        self._config = config
        self._parse_config()

    def _parse_config(self):
        self.input_data = self._data_in["X"]
        self.target_data = self._data_in["Y"]
        self.fit_degree = int(self._config["options"]["power"]["val"])

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
        in_data_poly = self._convert_to_poly(self.input_data.values)
        self.regression_function.fit(in_data_poly,self.target_data)

    def predict(self,data):
        data = self._convert_to_poly(data)
        return self.regression_function.predict(data)
        
    def _test(self):
        in_test = self.input_data.values*4
        pred = self.predict(in_test)
        plt.figure()
        plt.plot(in_test,
                    pred,
                    c='r',
                    label="Test Data. Degree: {0}".format(self.fit_degree))
        plt.scatter(self.input_data,
                    self.target_data.values,
                    label="Training Data")
        plt.legend()
        plt.show()