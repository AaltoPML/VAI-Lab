from vai_lab._plugin_templates import ModellingPluginT
from sklearn.linear_model import Lasso as model

_PLUGIN_READABLE_NAMES = {"Lasso":"default"}        # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "regression"}     # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                      # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"alpha": "float"}      # type:ignore
_PLUGIN_REQUIRED_DATA = {"X","Y"}                   # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}          # type:ignore

class Lasso(ModellingPluginT):
    """
    Linear Model trained with L1 prior as regularizer
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model()