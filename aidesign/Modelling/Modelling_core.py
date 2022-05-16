# -*- coding: utf-8 -*-
from aidesign.utils.import_helper import import_plugin_absolute
class Modelling(object):
    def __init__(self):
        self.node_name = None
        self.plugin_name = None
        self.output_data = None

    @property
    def data_in(self):
        return self._data_in

    @data_in.setter
    def data_in(self,data_in):
        self._data_in = data_in

    def set_input_data(self, data):
        self.input_data = data

    def set_target_data(self, data):
        self.target_data = data

    def _load_plugin(self, plugin_name:str):
        self.plugin_name = plugin_name
        self.plugin = import_plugin_absolute(globals(),
                                ui_specs["_PLUGIN_PACKAGE"],
                                ui_specs["_PLUGIN_CLASS_NAME"])

    def set_options(self, module_config: dict):
        """Send configuration arguments to plugin

        :param module_config: dict of settings to congfigure the plugin
        """
        self._module_config = module_config
        self._load_plugin(self._module_config["plugin"]["plugin_name"])

    def launch(self):
        # send the input data to the modelling plugin and assign it to an output property
        pass

    def get_result(self):
        return self.output_data
