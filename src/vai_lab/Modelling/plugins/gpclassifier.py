from vai_lab._plugin_templates import ModellingPluginTClass
from sklearn.gaussian_process import GaussianProcessClassifier as model

_PLUGIN_READABLE_NAMES = {"GPClassifier": "default",
                          "GPC": "alias",
                          "GaussianProcessClassifier": "alias"}     # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "classification"}                 # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                                      # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"n_restarts_optimizer": "int",
                             "random_state": "int"}                 # type:ignore
_PLUGIN_REQUIRED_DATA = {"X", "Y"}                                  # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}                          # type:ignore


class GPClassifier(ModellingPluginTClass):
    """
    Gaussian process Classifier (GPC) based on Laplace approximation
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.clf = model()