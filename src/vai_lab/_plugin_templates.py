from typing import Dict
from vai_lab._types import DataInterface
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

class MissingDataError(Exception):
    def __init__(self, msg):
        self.msg = msg


class PluginTemplate:
    def __init__(self, plugin_globals: dict) -> None:
        """Instantiates data containers and parses plugin-specific options

        param: plugin_globals:dict dictionary representing the global symbol table of the plugin script
        """
        self.X = None
        self.Y = None
        self.X_test = None
        self.Y_test = None

        self._PLUGIN_READABLE_NAMES: dict
        self._PLUGIN_MODULE_OPTIONS: dict
        self._PLUGIN_REQUIRED_SETTINGS: dict
        self._PLUGIN_OPTIONAL_SETTINGS: dict
        self._PLUGIN_REQUIRED_DATA: dict
        self._PLUGIN_OPTIONAL_DATA: dict

        self._parse_plugin_requirements(plugin_globals)

    def configure(self, config: dict) -> None:
        """Sets and parses plugin configurations options
        :param config: dict of internal tags set in the XML config file 
        """
        self._config = config
        self._parse_config()

    def set_data_in(self, data_in: DataInterface) -> None:
        """Sets and parses incoming data
        :param data_in: saves data as class variable
                        expected type: vai_lab.Data.Data_core.Data
        """
        req_check = [
            r for r in self._PLUGIN_REQUIRED_DATA if r not in data_in.keys()]
        if len(req_check) > 0:
            self._data_missing_error(req_check)
        self._data_in = data_in

    def _parse_plugin_requirements(self, plugin_globals: dict):
        """Get all plugin options from child plugin.
        """
        for key in plugin_globals.keys():
            if key.startswith("_PLUG"):
                self.__setattr__(key, plugin_globals[key])
        self._get_plugin_deafult_name(plugin_globals)

    def _get_plugin_deafult_name(self, plugin_globals: dict):
        """Parse self._PLUGIN_READABLE_NAMES for default name and set to self.default_name"""
        self.default_name = None
        for name in self._PLUGIN_READABLE_NAMES:
            if self._PLUGIN_READABLE_NAMES[name] == "default":
                if self.default_name is not None:
                    print("Multiple deafult names specified in " +
                          plugin_globals["__file__"])
                self.default_name = name

    def _data_missing_error(self, req):
        """If incoming data does not match required data, raise Exception and print"""
        raise MissingDataError("Minimal Data Requirements not met"
                        + "\n\t{0} ".format(self.default_name)
                        + "requires data: {0}".format(self._PLUGIN_REQUIRED_DATA)
                        + "\n\tThe following data is missing:"
                        + "\n\t\u2022 {}".format(",\n\t\u2022 ".join([*req])))

    def _parse_config(self):
        """Parse incoming data and args, sets them as class variables"""
        self.X = self._get_data_if_exist(self._data_in, "X")
        self.Y = np.array(self._get_data_if_exist(self._data_in, "Y")).ravel()
        self.X_test = self._get_data_if_exist(self._data_in, "X_test")
        self.Y_test = np.array(self._get_data_if_exist(self._data_in, "Y_test")).ravel()
        self._clean_options()

    def _get_data_if_exist(self, data_dict: dict, key: str, default=None):
        """Returns data from incoming data if exists, else returns None

        :param data_dict:dict of all incoming data
        :param key:str: name of data being searched for

        :returns result:dict OR None: dict of data if exists, else None
        """
        return data_dict[key] if key in data_dict.keys() and data_dict[key] is not None else default

    def _reshape(self, data, shape):
        """Reshapes data to shape. Primarily used for arrays with shape (n,)

        :param data: data to reshape
        :param shape: shape to reshape to

        :returns reshaped data: reshaped data
        """
        return data.reshape(shape[0], shape[1])

    def _parse_options_dict(self,options_dict:Dict):
        for key, val in options_dict.items():
            if type(val) == str:
                if val.replace('.', '').replace(',', '').isnumeric():
                    cleaned_opts = []
                    for el in val.split(","):
                        val = float(el)
                        if val.is_integer():
                            val = int(val)
                        cleaned_opts.append(val)
                    options_dict[key] = cleaned_opts
                elif val.lower() in ('yes', 'true'):
                    options_dict[key] = True
                elif val.lower() in ('no', 'false'):
                    options_dict[key] = False
                elif val.lower() in ('none'):
                    options_dict[key] = None
                elif val == 'X':
                    options_dict[key] = self.X
                elif val == 'Y':
                    options_dict[key] = self.Y
                elif val == 'X_test':
                    options_dict[key] = self.X_test
                elif val == 'Y_test':
                    options_dict[key] = self.Y_test
                elif key.lower() == 'x':
                    options_dict[key] = self.X
                elif key.lower() == 'y':
                    options_dict[key] = self.Y
        return options_dict

    def _clean_options(self):
        """Parses incoming plugin options in self._config["options"] 
                and modifies DataInterface in-place
                str options which only contain numeric data are converted to float OR int
        """
        return self._parse_options_dict(self._config["options"])

    def _test(self, data: DataInterface) -> DataInterface:
        """Run debug tests on data operations
        TODO: Investigate if all plugins need a score and predict method
        """
        if self._PLUGIN_MODULE_OPTIONS['Type'] == 'classification':
            print('Training accuracy: %.2f%%' %
                  (self.score([self.X, self.Y])*100))  # type: ignore
            if self.Y_test is not None:
                print('Test accuracy: %.2f%%' %
                      (self.score([self.X_test, self.Y_test])*100))
            if self.X_test is not None:
                data.append_data_column("Y_pred", self.predict(self.X_test))
            return data
        elif self._PLUGIN_MODULE_OPTIONS['Type'] == 'regression':
            print('Training R2 score: %.3f' %
                  (self.score([self.X, self.Y])))  # type: ignore
            if self.Y_test is not None:
                print('Test R2 score: %.3f' %
                      (self.score([self.X_test, self.Y_test])))
            if self.X_test is not None:
                data.append_data_column("Y_pred", self.predict_plugin(self.X_test))
            return data
        elif self._PLUGIN_MODULE_OPTIONS['Type'] == 'clustering':
            print('Clustering completed')
            if self.X_test is not None:
                data.append_data_column("Y_pred", self.predict(self.X_test))
            return data
        else:
            return data


class DataProcessingT(PluginTemplate, ABC):
    def __init__(self, plugin_globals: dict) -> None:
        super().__init__(plugin_globals)
        self._options_to_ignore = ["Data"]

    def configure(self, config: dict):
        """Extended from PluginTemplate.configure"""
        super().configure(config)
        if type(self.X) is None and type(self.Y) is None:
            print('Invalid Data name. Indicate whether to use `X` or `Y`')

    def _clean_solver_options(self):
        """XML tags that specify data to be processed should not be sent to solver
        TODO: in future, reverse the direction of this function - instead pull all options
                that are directly required by the solver
        """
        _cleaned =  {i[0]: i[1]
                for i in self._config["options"].items()
                if i[0] not in self._options_to_ignore}
        for key, val in _cleaned.items():
            if val == 'True':
                _cleaned[key] = True
            elif val == 'False':
                _cleaned[key] = False
            elif val == 'X':
                _cleaned[key] = self.X
            elif val == 'Y':
                _cleaned[key] = self.Y
            elif val == 'X_test':
                _cleaned[key] = self.X_test
            elif val == 'Y_test':
                _cleaned[key] = self.Y_test
            elif key.lower() == 'x':
                _cleaned[key] = self.X
            elif key.lower() == 'y':
                _cleaned[key] = self.Y
        return _cleaned

    def fit(self, options={}):
        try:
            if isinstance(options, list):
                return self.fit_plugin(*options)
            if isinstance(options, dict):
                return self.fit_plugin(**options)
            else:
                return self.fit_plugin(options)
        except Exception as exc:
            print('The plugin encountered an error when fitting '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+': '+str(exc)+'.')
            raise

    def transform(self, options={}) -> DataInterface:
        try:
            if isinstance(options, list):
                return pd.DataFrame(self.transform_plugin(*options))
            elif isinstance(options, dict):
                return pd.DataFrame(self.transform_plugin(**options)), options.keys()
            else:
                return pd.DataFrame(self.transform_plugin(options))
        except Exception as exc:
            print('The plugin encountered an error when transforming the data with '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+': '+str(exc)+'.')
            raise

class ModellingPluginT(PluginTemplate, ABC):
    def __init__(self, plugin_globals: dict) -> None:
        super().__init__(plugin_globals)

    def fit(self, options={}):
        """Sends params to fit, then runs fit"""
        try:
            if isinstance(options, list):
                return self.fit_plugin(*options)
            if isinstance(options, dict):
                return self.fit_plugin(**options)
            else:
                return self.fit_plugin(options)
        except Exception as exc:
            print('The plugin encountered an error when fitting '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+': '+str(exc)+'.')
            raise

    def predict(self, options={}):
        """Uses fitted model to predict output of a given Y
        :param data: array-like or sparse matrix, shape (n_samples, n_features)
                    Samples
                    expected type: vai_lab.Data.Data_core.Data
        :returns: array, shape (n_samples,)
                    Returns predicted values.
        """
        try:
            if isinstance(options, list):
                return self.predict_plugin(*options)
            elif isinstance(options, dict):
                return self.predict_plugin(**options)
            else:
                return self.predict_plugin(options)

        except Exception as exc:
            print('The plugin encountered an error when predicting with '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+': '+str(exc)+'.')
            raise

    def score(self, options={}):
        """Return the coefficient of determination
        :param  X : array-like of shape (n_samples, n_features)
        :param  Y :  array-like of shape (n_samples,) or (n_samples, n_outputs)

        :returns: score : float of ``self.predict(X)`` wrt. `y`.
        """
        try:
            if isinstance(options, list):
                return self.score_plugin(*options)
            elif isinstance(options, dict):
                return self.score_plugin(**options)
            else:
                return self.score_plugin(options)
        except Exception as exc:
            print('The plugin encountered an error when calculating the score with '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+'.')
            raise

class ModellingPluginTClass(ModellingPluginT, ABC):
    def __init__(self, plugin_globals: dict) -> None:
        super().__init__(plugin_globals)

    def predict_proba(self, options={}):
        """Uses fitted model to predict the probability of the output of a given Y
        :param data: array-like or sparse matrix, shape (n_samples, n_features)
                    Samples
                    expected type: vai_lab.Data.Data_core.Data
        :returns: array, shape (n_samples,)
                    Returns predicted values.
        """
        try:
            if isinstance(options, list):
                return self.predict_proba_plugin(*options)
            if isinstance(options, dict):
                return self.predict_proba_plugin(**options)
            else:
                return self.predict_proba_plugin(options)
        except Exception as exc:
            print('The plugin encountered an error when predicting the probability with '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+'.')
            raise

class DecisionMakingPluginT(PluginTemplate, ABC):
    def __init__(self, plugin_globals: dict) -> None:
        super().__init__(plugin_globals)
    
    def configure(self, config: dict):
        """Extended from PluginTemplate.configure"""
        super().configure(config)
        if type(self.X) is None and type(self.Y) is None:
            print('Invalid Data name. Indicate whether to use `X` or `Y`')
    
    def run_optimization(self, options={}):
        """Sends parameters to optimizer, then runs Bayesian Optimization for a number 'max_iter' of iterations"""
        try:
            if isinstance(options, list):
                return self.opt_plugin(*options)
            if isinstance(options, dict):
                return self.opt_plugin(**options)
            else:
                return self.opt_plugin(options)
        except Exception as exc:
            print('The plugin encountered an error when running the optimization '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+'.')
            raise

    def suggest_next_locations(self, options={}):
        """Run a single optimization step and return the next locations to evaluate the objective. 
        Number of suggested locations equals to batch_size.
        :returns: array, shape (n_samples,)
                    Returns suggested values.
        """
        try:
            if isinstance(options, list):
                return self.suggest_plugin(*options)
            if isinstance(options, dict):
                return self.suggest_plugin(**options)
            else:
                return self.suggest_plugin(options)
        except Exception as exc:
            print('The plugin encountered an error when suggesting points with '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+'.')
            raise


class UI(PluginTemplate, ABC):
    @property
    def class_list(self):
        pass
        # """Set the class list"""

    @class_list.setter  # type: ignore
    @abstractmethod
    def class_list(self, value):
        pass

    @abstractmethod
    def save_file(self):
        pass

    @abstractmethod
    def save_file_as(self):
        pass


class InputDataPluginT(PluginTemplate, ABC):
    def __init__(self, plugin_globals: dict) -> None:
        super().__init__(plugin_globals)

    def import_data(self, options={}):
        """Sends params to import data, then import data"""
        try:
            if isinstance(options, list):
                return self.import_plugin(*options)
            if isinstance(options, dict):
                return self.import_plugin(**options), options.keys()
            else:
                return self.import_plugin(options)
        except Exception as exc:
            print('The plugin encountered an error when importing '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+': '+str(exc)+'.')
            raise

    def append_data_column(self, options={}):
        """ Appends a column to the dataframe
        :returns: array, shape (n_samples,)
                    Returns predicted values.
        """
        try:
            if isinstance(options, list):
                return self.append_plugin(*options)
            elif isinstance(options, dict):
                return self.append_plugin(**options)
            else:
                return self.append_plugin(options)

        except Exception as exc:
            print('The plugin encountered an error when appending '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+': '+str(exc)+'.')
            raise

class EnvironmentPluginT(PluginTemplate, ABC):
    
    @abstractmethod
    def load_model(self) -> None:
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def set_gui(self,use_gui:bool=True) -> None:
        pass

    def configure(self, config: dict):
        """Extended from PluginTemplate.configure"""
        super().configure(config)
        self.set_gui(self._config["options"]["usegui"])