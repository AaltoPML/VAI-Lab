from vai_lab._plugin_templates import ModellingPluginT
from sklearn.linear_model import ElasticNet as model

_PLUGIN_READABLE_NAMES = {"ElasticNet": "default"}      # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "regression"}         # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                          # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"l1_ratio": "float"}       # type:ignore
_PLUGIN_REQUIRED_DATA = {"X", "Y"}                      # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}              # type:ignore


class ElasticNet(ModellingPluginT):
    """
    Linear regression with combined L1 and L2 priors as regularizer
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model()