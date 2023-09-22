from vai_lab._plugin_templates import ModellingPluginT
from sklearn.cluster import Birch as model

_PLUGIN_READABLE_NAMES = {"Birch": "default"}       # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "clustering"}     # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                      # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"n_clusters": "int",   # type:ignore
                             "threshold": "float"}  # type:ignore
_PLUGIN_REQUIRED_DATA = {"X"}                       # type:ignore
_PLUGIN_OPTIONAL_DATA = {"Y", "X_tst", 'Y_tst'}     # type:ignore


class Birch(ModellingPluginT):
    """
    Implements the BIRCH clustering algorithm
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model()