from vai_lab._plugin_templates import ModellingPluginT
from sklearn.cluster import MeanShift as model

_PLUGIN_READABLE_NAMES = {"MeanShift":"default"}        # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "clustering"}         # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                          # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"bandwidth": "float"}      # type:ignore
_PLUGIN_REQUIRED_DATA = {"X"}                           # type:ignore
_PLUGIN_OPTIONAL_DATA = {"Y", "X_tst", 'Y_tst'}         # type:ignore

class MeanShift(ModellingPluginT):
    """
    Mean shift clustering using a flat kernel.
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model()