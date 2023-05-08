from vai_lab._plugin_templates import DecisionMakingPluginT
from bayes_opt import BayesianOptimization as model

_PLUGIN_READABLE_NAMES = {"bayes_opt": "default",
                          "BayesOpt": "alias",}           # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "decision making"}       # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"f": "function",
                             "pbounds": "dict"}              # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {
                            #  "constraint": "ConstraintModel",
                             "random_state ": "int",
                             "verbose": "bool",
                            #  "bounds_transformer": "DomainTransformer",
                             "allow_duplicate_points": "str"} # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                  # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X","Y"}                           # type:ignore

class bayes_opt(DecisionMakingPluginT):
    """
    Bayesian optimisation model using bayes_opt.
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model
    
    def optimise(self):
        """Probes the target space to find the parameters that yield the maximum value for the given function."""
        try:
            self.BO.maximize()
        except Exception as exc:
            print('The plugin encountered an error when running the optimization '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+'.')
            raise

    def suggest_locations(self, utility_function):
        """Run a single optimization step and return the next locations to evaluate the objective. 
        :returns: array, shape (n_samples,)
                    Returns suggested values.
        """
        try:
            return self.BO.suggest(utility_function)
        except Exception as exc:
            print('The plugin encountered an error when suggesting points with '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+'.')
            raise