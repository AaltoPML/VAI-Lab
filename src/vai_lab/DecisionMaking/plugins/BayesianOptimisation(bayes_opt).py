from vai_lab._plugin_templates import DecisionMakingPluginT
from bayes_opt import BayesianOptimization as model

_PLUGIN_READABLE_NAMES = {"bayes_opt": "default",
                          "BayesOpt": "alias",}               # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "decision making"}          # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"f": "function",
                             "pbounds": "dict"}               # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {
                            #  "constraint": "ConstraintModel",
                             "random_state ": "int",
                             "verbose": "bool",
                            #  "bounds_transformer": "DomainTransformer",
                             "allow_duplicate_points": "str"} # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                    # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X","Y"}                             # type:ignore

class bayes_opt(DecisionMakingPluginT):
    """
    Bayesian optimisation model using bayes_opt.
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

        self.opt_plugin = self.model.maximize
        self.suggest_plugin = self.model.suggest