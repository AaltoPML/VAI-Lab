from vai_lab._plugin_templates import ModellingPluginT
from sklearn.linear_model import BayesianRidge as model

_PLUGIN_READABLE_NAMES = {"BayesianRidge": "default"}   # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "regression"}         # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                          # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"n_iter": "int"}           # type:ignore
_PLUGIN_REQUIRED_DATA = {"X", "Y"}                      # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}              # type:ignore


class BayesianRidge(ModellingPluginT):
    """
    Bayesian ridge regression
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.clf = model()