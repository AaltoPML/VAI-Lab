from sklearn.preprocessing import StandardScaler
import numpy as np
from matplotlib import pyplot as plt

_PLUGIN_READABLE_NAMES = {"KNNClassifier":"default","KNN-C":"alias"}
_PLUGIN_MODULE_OPTIONS = {}
_PLUGIN_REQUIRED_SETTINGS = {}
_PLUGIN_OPTIONAL_SETTINGS = {}
_PLUGIN_REQUIRED_DATA = {"X","Y"}
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}

class StandardScaler(object):
    """KNN for supervised classification"""

    def __init__(self):
        self.X = None
        self.Y = None
        self.X_tst = None
        self.Y_tst = None
        self.proc = StandardScaler()

    def set_data_in(self,data_in):
        req_check = [r for r in _PLUGIN_REQUIRED_DATA if r not in data_in.keys()]
        if len(req_check) > 0:
            raise Exception("Minimal Data Requirements not met"   \
                            +"\n\t{0} ".format(StandardScaler) \
                            +"requires data: {0}".format(_PLUGIN_REQUIRED_DATA)\
                            + "\n\tThe following data is missing:"\
                            + "\n\t\u2022 {}".format(",\n\t\u2022 ".join([*req_check])))
        self._data_in = data_in

    def configure(self, config:dict):
        self._config = config
        self._parse_config()

    def _parse_config(self):
        self.X = self._data_in["X"]
        self.Y = np.array(self._data_in["Y"]).ravel()
        self.X_tst = self._is_name_passed(self._data_in, "X_test")
        self.Y_tst = np.array(self._is_name_passed(self._data_in, "Y_test")).ravel()
        print(self._config["options"])

    def _is_name_passed(self, dic: dict, key: str, default = None):
        return dic[key] if key in dic.keys() and dic[key] is not None else default

    def _reshape(self,data,shape):
        return data.reshape(shape[0],shape[1])

    def _check_numeric(self, dict_opt):
        for key, val in dict_opt.items():
            """ 
            TODO: Maybe, if list -> cv
            """
            if type(val) == str and val.replace('.','').replace(',','').isnumeric():
                val = float(val)
                if val.is_integer():
                    val = int(val)
                print(val)
            dict_opt[key] = val
        return dict_opt

    def fit(self):
        self._check_numeric(self._config["options"])
        self.proc.set_params(**self._config["options"])
        self.proc.fit(self.X)

    def transform(self,data):
        data["X"] = self.transform(self.X)
        if self.Y_tst is not None:
            data["X_test"] = self.transform(self.X_tst)
        return data