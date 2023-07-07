from vai_lab._plugin_templates import ModellingPluginTClass
from sklearn.svm import SVC as model

_PLUGIN_READABLE_NAMES = {"SVC": "default",
                          "SupportVectorClassification": "alias"}   # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "classification"}                 # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                                      # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"C": "float",
                             "kernel": "str",
                             "gamma": "float",
                             "degree": "int"}                       # type:ignore
_PLUGIN_REQUIRED_DATA = {"X", "Y"}                                  # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}                          # type:ignore


class SVC(ModellingPluginTClass):
    """
    C-Support Vector Classification
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model()