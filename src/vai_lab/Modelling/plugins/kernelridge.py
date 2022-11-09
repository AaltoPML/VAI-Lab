from vai_lab._plugin_templates import ModellingPluginT
from sklearn.kernel_ridge import KernelRidge as model

_PLUGIN_READABLE_NAMES = {"KernelRidge": "default",
                          "KR": "alias"}                # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "regression"}         # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                          # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"alpha": "float",
                             "kernel": "str",
                             "gamma": "float",
                             "degree": "int"}           # type:ignore
_PLUGIN_REQUIRED_DATA = {"X", "Y"}                      # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}              # type:ignore


class KernelRidge(ModellingPluginT):
    """
    Kernel ridge regression.
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.clf = model()

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
        self.clf.set_params(**self._config["options"])
        self.clf.fit(self.X, self.Y)

    def predict(self, data):
        """Uses fitted model to predict output of a given Y
        :param data: array-like or sparse matrix, shape (n_samples, n_features)
                    Samples
                    expected type: aidesign.Data.Data_core.Data
        :returns: array, shape (n_samples,)
                    Returns predicted values.
        """
        return self.clf.predict(data)

    def score(self, X, Y, sample_weight=None):
        """Return the coefficient of determination
        :param  X : array-like of shape (n_samples, n_features)
        :param  Y :  array-like of shape (n_samples,) or (n_samples, n_outputs)
        :param sample_weight : array-like of shape (n_samples,), default=None
                    Sample weights.

        :returns: score : float R^2` of ``self.predict(X)`` wrt. `y`.
        """
        return self.clf.score(X, Y, sample_weight=None)