from vai_lab._plugin_templates import DecisionMakingPluginT
from  GPyOpt.methods import BayesianOptimization as model
from typing import Dict

_PLUGIN_READABLE_NAMES = {"GPyOpt": "default",
                          "BayesianOptimisation": "alias",
                          "BayesianOptimisation_GPy": "alias",} # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "decision making"}            # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"f": "function"}                   # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                                  # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                      # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X","Y"}                               # type:ignore

class GPyOpt(DecisionMakingPluginT):
    """
    Bayesian optimisation model using GPyOpt. Compatible with no objective function using tabular data.
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

        self.opt_plugin = self.model.run_optimization
        self.suggest_plugin = self.model.suggest_next_locations
    
    def _parse_options_dict(self, options_dict:Dict):
        super()._parse_options_dict(options_dict)
        if self.X is not None:
            options_dict['X'] = self.X
        if self.Y is not None:
            options_dict['Y'] = self.Y.reshape(-1,1)
        return options_dict