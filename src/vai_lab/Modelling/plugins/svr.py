from vai_lab._plugin_templates import ModellingPluginT
from sklearn.svm import SVR as model

_PLUGIN_READABLE_NAMES = {"SVR": "default",
                          "SupportVectorRegression": "alias"}   # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "regression"}                 # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                                  # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"C": "float",
                             "kernel": "str",
                             "gamma": "float",
                             "degree": "int"}                   # type:ignore
_PLUGIN_REQUIRED_DATA = {"X", "Y"}                              # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}                      # type:ignore


class SVR(ModellingPluginT):
    """
    Epsilon-Support Vector Regression
    """

    def __init__(self, config = {}, data_in = [None]):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.set_data_in(data_in)
        self.configure(config)
        
        try:
            self.model = model(**self._config["options"])
        except Exception as exc:
            print('The plugin encountered an error on the parameters of '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+': '+str(exc)+'.')
            raise
        
        self.fit_plugin = self.model.fit
        self.predict_plugin = self.model.predict
        self.score_plugin = self.model.score