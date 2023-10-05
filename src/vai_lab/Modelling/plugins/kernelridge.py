from vai_lab._plugin_templates import ModellingPluginT
from sklearn.kernel_ridge import KernelRidge as model

_PLUGIN_READABLE_NAMES = {"KernelRidge": "default",
                          "KR": "alias"}                # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "regression"}         # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                          # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"kernel": "str",
                             "gamma": "float",
                             "degree": "int"}           # type:ignore
_PLUGIN_REQUIRED_DATA = {"X", "Y"}                      # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}              # type:ignore


class KernelRidge(ModellingPluginT):
    """
    Kernel ridge regression.
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model()