from vai_lab._plugin_templates import ModellingPluginTClass
from sklearn.linear_model import Perceptron as model

_PLUGIN_READABLE_NAMES = {"Perceptron": "default",
                          "LinearPerceptron": "alias"}      # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "classification"}         # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                              # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"alpha": "float",
                             "penalty": "str"}              # type:ignore
_PLUGIN_REQUIRED_DATA = {"X", "Y"}                          # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}                  # type:ignore


class Perceptron(ModellingPluginTClass):
    """
    Linear perceptron classification
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.clf = model()