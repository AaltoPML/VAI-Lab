from sklearn.tree import DecisionTreeClassifier as model
import numpy as np

_PLUGIN_READABLE_NAMES = {"DecissionTreeClassifier":"default","DTClassifier":"alias"}
_PLUGIN_MODULE_OPTIONS = {"Type": "classifier"}
_PLUGIN_REQUIRED_SETTINGS = {}
_PLUGIN_OPTIONAL_SETTINGS = {"max_depth": "int"} # model().get_params()
_PLUGIN_REQUIRED_DATA = {"X","Y"}
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}

class DecisionTreeClassifier(object):
    """
    A decision tree classifier
    """

    def __init__(self):
        self.X = None
        self.Y = None
        self.X_tst = None
        self.Y_tst = None
        self.clf = model()

    def set_data_in(self,data_in):
        req_check = [r for r in _PLUGIN_REQUIRED_DATA if r not in data_in.keys()]
        if len(req_check) > 0:
            raise Exception("Minimal Data Requirements not met"   \
                            +"\n\t{0} ".format(DecisionTreeClassifier) \
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
        # print(self._config["options"])

    def _is_name_passed(self, dic: dict, key: str, default = None):
        return dic[key] if key in dic.keys() and dic[key] is not None else default
    
    def _reshape(self,data,shape):
        return data.reshape(shape[0],shape[1])
    
    def _check_numeric(self, dict_opt):
        for key, val in dict_opt.items():
            """ 
            TODO: maybe, if list -> cv
            """
            if type(val) == str and val.replace('.','').replace(',','').isnumeric():
                val = float(val)
                if val.is_integer():
                    val = int(val)
            dict_opt[key] = val
        return dict_opt

    def solve(self):
        self._check_numeric(self._config["options"])
        self.clf.set_params(**self._config["options"])
        self.clf.fit(self.X, self.Y)

    def predict(self,data):
        return self.clf.predict(data)

    def score(self,X_tst, Y_tst):
        return self.clf.score(X_tst, Y_tst)

    def _test(self):
        if _PLUGIN_MODULE_OPTIONS['Type'] == 'classifier':
            print('Training accuracy: %.2f%%' %(self.score(self.X, self.Y)*100))
            if self.Y_tst is not None:
                print('Test accuracy: %.2f%%' %(self.score(self.X_tst, self.Y_tst)*100))
        elif _PLUGIN_MODULE_OPTIONS['Type'] == 'regressor':
            print('Training R2 score: %.3f' %(self.score(self.X, self.Y)))
            if self.Y_tst is not None:
                print('Training R2 score: %.3f' %(self.score(self.X_tst, self.Y_tst)))