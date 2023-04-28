from vai_lab._plugin_templates import ModellingPluginTClass
from sklearn.tree import DecisionTreeClassifier as model

_PLUGIN_READABLE_NAMES = {"DecissionTreeClassifier": "default",
                          "DTClassifier": "alias"}              # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "classification"}             # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                                  # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"max_depth": "int"}                # type:ignore
_PLUGIN_REQUIRED_DATA = {"X", "Y"}                              # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}                      # type:ignore


class DecisionTreeClassifier(ModellingPluginTClass):
    """
    A decision tree classifier
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.clf = model()