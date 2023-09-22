from vai_lab._plugin_templates import ModellingPluginT
from sklearn.gaussian_process import GaussianProcessRegressor as model

_PLUGIN_READABLE_NAMES = {"GPRegressor": "default",
                          "GPR": "alias",
                          "GaussianProcessRegressor": "alias"}      # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "regression"}                     # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                                      # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"n_restarts_optimizer": "int",
                             "random_state": "int"}                 # type:ignore
_PLUGIN_REQUIRED_DATA = {"X", "Y"}                                  # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}                          # type:ignore


class GPRegressor(ModellingPluginT):
    """
    Gaussian process regressor
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model()