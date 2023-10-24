from vai_lab._import_helper import import_plugin_absolute
from vai_lab._types import PluginSpecsInterface, DataInterface, DataProcessingPluginInterface

class DataProcessing(object):
    def __init__(self) -> None:
        self.output_data: DataInterface

    def set_avail_plugins(self, avail_plugins: PluginSpecsInterface) -> None:
        self._avail_plugins = avail_plugins

    def set_data_in(self, data_in: DataInterface) -> None:
        self._data_in = data_in

    def _load_plugin(self, data_in: DataInterface) -> None:
        avail_plugins = self._avail_plugins.find_from_readable_name(
            self._module_config["plugin"]["plugin_name"])
        self.set_data_in(data_in)
        self._plugin: DataProcessingPluginInterface = import_plugin_absolute(globals(),
                                              avail_plugins["_PLUGIN_PACKAGE"],
                                              avail_plugins["_PLUGIN_CLASS_NAME"])\
            .__call__(self._module_config["plugin"], data_in)

    def set_options(self, module_config: dict) -> None:
        """Send configuration arguments to plugin

        :param module_config: dict of settings to configure the plugin
        """
        self._module_config = module_config

    def launch(self) -> None:

        for method in self._module_config["plugin"]["methods"]["_order"]:
            if "options" in self._module_config["plugin"]["methods"][method].keys():
                getattr(self._plugin, "{}".format(method))(self._plugin._parse_options_dict(self._module_config["plugin"]["methods"][method]["options"]))
            else:
                getattr(self._plugin, "{}".format(method))()

        self.output_data = self._data_in.copy()

    def get_result(self) -> DataInterface:
        return self.output_data