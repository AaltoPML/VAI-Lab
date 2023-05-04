from vai_lab._plugin_templates import DecisionMakingPluginT
from  GPyOpt.methods import BayesianOptimization as model

_PLUGIN_READABLE_NAMES = {"BayesianOptimisation": "default",
                          "BO": "alias",}                   # type:ignore
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

class BayesianOptimisation(DecisionMakingPluginT):
    """
    Bayesian optimisation model
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model