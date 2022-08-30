from aidesign._types import DataInterface

import numpy as np


class PluginTemplate:
    def __init__(self, plugin_globals: dict) -> None:
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
                        expected type: aidesign.Data.Data_core.Data
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
        raise Exception("Minimal Data Requirements not met"
                        + "\n\t{0} ".format(self.default_name)
                        + "requires data: {0}".format(self._PLUGIN_REQUIRED_DATA)
                        + "\n\tThe following data is missing:"
                        + "\n\t\u2022 {}".format(",\n\t\u2022 ".join([*req])))

    def _parse_config(self):
        """Parse incoming data and args, sets them as class variables"""
        self.X = self._data_in["X"]
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

    def _clean_options(self):
        """Parses incoming plugin options in self._config["options"] 
                and modifies DataInterface in-place
                str options which only contain numeric data are converted to float OR int
        """
        for key, val in self._config["options"].items():
            """ 
            TODO: Maybe, if list -> cv
            """
            if type(val) == str and val.replace('.', '').replace(',', '').isnumeric():
                val = float(val)
                if val.is_integer():
                    val = int(val)
            self._config["options"][key] = val
