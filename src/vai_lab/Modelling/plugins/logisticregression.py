from vai_lab._plugin_templates import ModellingPluginTClass
from sklearn.linear_model import LogisticRegression as model

_PLUGIN_READABLE_NAMES = {"LogisticRegression": "default",
                          "logit": "alias",
                          "MaxEnt": "alias"}                    # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "classification"}             # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                                  # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                                  # type:ignore
_PLUGIN_REQUIRED_DATA = {"X", "Y"}                              # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}                      # type:ignore


class LogisticRegression(ModellingPluginTClass):
    """
    Logistic regression classification.
    """

    def __init__(self, config = {}, data_in = [None], ini = False):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        if not ini:
            # Model configuration
            self.set_data_in(data_in)
            self.configure(config)
            # Model initialisation    
            try:    
                self.model = model(**self._config["options"])
            except Exception as exc:
                print('The plugin encountered an error on the parameters of '
                        +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+': '+str(exc)+'.')
                raise
        else:
            self.model = model
            
        self.fit_plugin = self.model.fit
        self.predict_plugin = self.model.predict
        self.predict_proba_plugin = self.model.predict_proba
        self.score_plugin = self.model.score