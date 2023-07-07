from vai_lab._plugin_templates import ModellingPluginTClass
from sklearn.neighbors import KNeighborsClassifier as model

_PLUGIN_READABLE_NAMES = {"KNNClassifier": "default",
                          "KNN-C": "alias"}             # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "classification"}     # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                          # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"n_neighbors": "int",
                             "weights": "str"}          # type:ignore
_PLUGIN_REQUIRED_DATA = {"X", "Y"}                      # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}              # type:ignore


class KNNClassifier(ModellingPluginTClass):
    """
    Classifier implementing the k-nearest neighbors vote
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model()