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
        self.X_tst = None
        self.Y_tst = None

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
        self.X = np.array(self._get_data_if_exist(self._data_in, "X"))
        self.Y = np.array(self._get_data_if_exist(self._data_in, "Y")).ravel()
        self.X_tst = self._get_data_if_exist(self._data_in, "X_test")
        self.Y_tst = np.array(self._get_data_if_exist(
            self._data_in, "Y_test")).ravel()
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
            if type(val) == str and val.replace('.', '').replace(',', '').isnumeric():
                cleaned_opts = []
                for el in val.split(","):
                    val = float(el)
                    if val.is_integer():
                        val = int(val)
                    cleaned_opts.append(val)
                options_dict[key] = cleaned_opts
            elif type(val) == str and val.lower() in ('y', 'yes', 't', 'true', 'on'):
                options_dict[key] = True
            elif type(val) == str and val.lower() in ('n', 'no', 'f', 'false', 'off'):
                options_dict[key] = False
            elif type(val) == str and val.lower() in ('none'):
                options_dict[key] = None
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
                  (self.score(self.X, self.Y)*100))  # type: ignore
            if self.Y_tst is not None:
                print('Test accuracy: %.2f%%' %
                      (self.score(self.X_tst, self.Y_tst)*100))
            if self.X_tst is not None:
                data.append_data_column("Y_pred", self.predict(self.X_tst))
            return data
        elif self._PLUGIN_MODULE_OPTIONS['Type'] == 'regression':
            print('Training R2 score: %.3f' %
                  (self.score(self.X, self.Y)))  # type: ignore
            if self.Y_tst is not None:
                print('Training R2 score: %.3f' %
                      (self.score(self.X_tst, self.Y_tst)))
            if self.X_tst is not None:
                data.append_data_column("Y_pred", self.predict(self.X_tst))
            return data
        elif self._PLUGIN_MODULE_OPTIONS['Type'] == 'clustering':
            print('Clustering completed')
            if self.X_tst is not None:
                data.append_data_column("Y_pred", self.predict(self.X_tst))
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
        return _cleaned
            
    def fit(self):
        cleaned_options = self._clean_solver_options()
        try:
            self.proc.set_params(**cleaned_options)
        except Exception as exc:
            print('The plugin encountered an error on the parameters of '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+': '+str(exc)+'.')
            raise
        try:
            self.proc.fit(self.X)
        except Exception as exc:
            print('The plugin encountered an error when fitting '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+': '+str(exc)+'.')
            raise

    def transform(self, data: DataInterface) -> DataInterface:
        try:
            data.append_data_column("X", pd.DataFrame(self.proc.transform(self.X)))
        except Exception as exc:
            print('The plugin encountered an error when transforming the data with '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+': '+str(exc)+'.')
            raise
        if self.X_tst is not None:
            try:
                data.append_data_column("X_test", pd.DataFrame(self.proc.transform(self.X_tst)))
            except Exception as exc:
                print('The plugin encountered an error when transforming the data with '
                        +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+': '+str(exc)+'.')
                raise
        return data


class ModellingPluginT(PluginTemplate, ABC):
    def __init__(self, plugin_globals: dict) -> None:
        super().__init__(plugin_globals)

    def solve(self):
        """Sends params to solver, then runs solver"""
        try:
            self.clf.set_params(**self._config["options"])
        except Exception as exc:
            print('The plugin encountered an error on the parameters of '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+': '+str(exc)+'.')
            raise
        try:
            self.clf.fit(self.X, self.Y)
        except Exception as exc:
            print('The plugin encountered an error when fitting '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+': '+str(exc)+'.')
            raise

    def predict(self, data):
        """Uses fitted model to predict output of a given Y
        :param data: array-like or sparse matrix, shape (n_samples, n_features)
                    Samples
                    expected type: vai_lab.Data.Data_core.Data
        :returns: array, shape (n_samples,)
                    Returns predicted values.
        """
        try:
            return self.clf.predict(data)
        except Exception as exc:
            print('The plugin encountered an error when predicting with '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+': '+str(exc)+'.')
            raise

    def score(self, X, Y, sample_weight):
        """Return the coefficient of determination
        :param  X : array-like of shape (n_samples, n_features)
        :param  Y :  array-like of shape (n_samples,) or (n_samples, n_outputs)
        :param sample_weight : array-like of shape (n_samples,), default=None
                    Sample weights.

        :returns: score : float of ``self.predict(X)`` wrt. `y`.
        """
        try:
            return self.clf.score(X, Y, sample_weight)
        except Exception as exc:
            print('The plugin encountered an error when calculating the score with '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+'.')
            raise

class ModellingPluginTClass(ModellingPluginT, ABC):
    def __init__(self, plugin_globals: dict) -> None:
        super().__init__(plugin_globals)

    def predict_proba(self, data):
        """Uses fitted model to predict the probability of the output of a given Y
        :param data: array-like or sparse matrix, shape (n_samples, n_features)
                    Samples
                    expected type: vai_lab.Data.Data_core.Data
        :returns: array, shape (n_samples,)
                    Returns predicted values.
        """
        try:
            return self.clf.predict_proba(data)
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
        try:
            self.BO = self.model(**self._clean_options())
        except Exception as exc:
            print('The plugin encountered an error on the parameters of '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+'.')
            raise
        if type(self.X) is None and type(self.Y) is None:
            print('Invalid Data name. Indicate whether to use `X` or `Y`')


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