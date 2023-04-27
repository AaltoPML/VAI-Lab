from vai_lab._plugin_templates import DecissionMakingPluginT
from  GPyOpt.methods import BayesianOptimization as model

_PLUGIN_READABLE_NAMES = {"BayesianOptimisation": "default",
                          "BO": "alias",}                   # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "decision making"}        # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"f": "function"}              # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"bounds": "list",
                             "constraints": "list",
                             "acquisition_type ": "str",
                             "files": "list",
                             "normalize_Y": "bool",
                             "evaluator_type": "str",
                             "batch_size": "int",
                             "acquisition_jitter": "float"} # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                  # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X","Y"}                           # type:ignore

class BayesianOptimisation(DecissionMakingPluginT):
    """
    Bayesian optimisation model
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.BO = model()

    def configure(self, config: dict):
        """Sets and parses plugin configurations options
        :param config: dict of internal tags set in the XML config file 
        """
        super().configure(config)

    def set_data_in(self, data_in):
        """Sets and parses incoming data
        :param data_in: saves data as class variable
                        expected type: aidesign.Data.Data_core.Data
        """
        super().set_data_in(data_in)

    def solve(self):
        """Sends params to solver, then runs solver"""
        self.BO.set_params(**self._config["options"])
        self.BO.fit(self.X, self.Y)

    def predict(self):
        """Uses fitted model to suggest next points
        :returns: array, shape (n_samples, n_features)
                    Returns suggested values.
        """
        return self.BO_batch.suggest_next_locations()

    def score(self, X, Y, sample_weight=None):
        """Return the coefficient of determination
        :param  X : array-like of shape (n_samples, n_features)
        :param  Y :  array-like of shape (n_samples,) or (n_samples, n_outputs)
        :param sample_weight : array-like of shape (n_samples,), default=None
                    Sample weights.

        :returns: score : float R^2` of ``self.predict(X)`` wrt. `y`.
        """
        return self.clf.score(X, Y, sample_weight=None)