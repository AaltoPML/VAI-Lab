from vai_lab._plugin_templates import ModellingPluginT
from sklearn.cluster import AffinityPropagation as model

_PLUGIN_READABLE_NAMES = {"Birch": "default"}       # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "clustering"}     # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                      # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"damping": "float"}    # type:ignore
_PLUGIN_REQUIRED_DATA = {"X"}                       # type:ignore
_PLUGIN_OPTIONAL_DATA = {"Y", "X_tst", 'Y_tst'}     # type:ignore


class AffinityPropagation(ModellingPluginT):
    """
    Perform Affinity Propagation Clustering of data
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.clf = model()