from vai_lab._plugin_templates import ModellingPluginTClass
from sklearn.linear_model import LogisticRegression as model

_PLUGIN_READABLE_NAMES = {"LogisticRegression": "default",
                          "logit": "alias",
                          "MaxEnt": "alias"}                    # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "classification"}             # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                                  # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"penalty": "str", "C": "float"}    # type:ignore
_PLUGIN_REQUIRED_DATA = {"X", "Y"}                              # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}                      # type:ignore


class LogisticRegression(ModellingPluginTClass):
    """
    Logistic regression classification.
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.clf = model()