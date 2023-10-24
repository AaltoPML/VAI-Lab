from vai_lab._plugin_templates import DecisionMakingPluginT
from  GPyOpt.methods import BayesianOptimization as model
from typing import Dict

_PLUGIN_READABLE_NAMES = {"GPyOpt": "default",
                          "BayesianOptimisation": "alias",
                          "BayesianOptimisation_GPy": "alias",} # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "decision making"}        # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"f": "function"}              # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"domain": "list",
                             "constraints": "list",
                             "acquisition_type ": "str",
                             "files": "list",
                             "normalize_Y": "bool",
                             "evaluator_type": "str",
                             "batch_size": "int",
                             "acquisition_jitter": "float"} # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                  # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X","Y"}                           # type:ignore

class GPyOpt(DecisionMakingPluginT):
    """
    Bayesian optimisation model using GPyOpt. Compatible with no objective function using tabular data.
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
        
        # self.fit_plugin = self.model.fit
        # self.transform_plugin = self.model.transform
    
    def _parse_options_dict(self, options_dict:Dict):
        super()._parse_options_dict(options_dict)
        if self.X is not None:
            options_dict['X'] = self.X
        if self.Y is not None:
            options_dict['Y'] = self.Y.reshape(-1,1)
        return options_dict
    
    def optimise(self):
        """Sends parameters to optimizer, then runs Bayesian Optimization for a number 'max_iter' of iterations"""
        try:
            self.BO.run_optimization()
        except Exception as exc:
            print('The plugin encountered an error when running the optimization '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+'.')
            raise

    def suggest_locations(self):
        """Run a single optimization step and return the next locations to evaluate the objective. 
        Number of suggested locations equals to batch_size.
        :returns: array, shape (n_samples,)
                    Returns suggested values.
        """
        try:
            return self.BO.suggest_next_locations()
        except Exception as exc:
            print('The plugin encountered an error when suggesting points with '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+'.')
            raise