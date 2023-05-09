from vai_lab._import_helper import import_plugin_absolute
from vai_lab._types import PluginSpecsInterface, DataInterface, DataProcessingPluginInterface

class DataProcessing(object):
    def __init__(self) -> None:
        self.output_data: DataInterface

    def set_avail_plugins(self, avail_plugins: PluginSpecsInterface) -> None:
        self._avail_plugins = avail_plugins

    def set_data_in(self, data_in: DataInterface) -> None:
        self._data_in = data_in

    def _load_plugin(self, plugin_name: str) -> None:
        avail_plugins = self._avail_plugins.find_from_readable_name(
            plugin_name)
        self._plugin_name = plugin_name
        self._plugin: DataProcessingPluginInterface = import_plugin_absolute(globals(),
                                              avail_plugins["_PLUGIN_PACKAGE"],
                                              avail_plugins["_PLUGIN_CLASS_NAME"])\
            .__call__()

    def set_options(self, module_config: dict) -> None:
        """Send configuration arguments to plugin

        :param module_config: dict of settings to configure the plugin
        """
        self._module_config = module_config
        self._load_plugin(self._module_config["plugin"]["plugin_name"])

    def launch(self) -> None:
        self._plugin.set_data_in(self._data_in)
        self._plugin.configure(self._module_config["plugin"])
        self._plugin.fit()
        self.output_data = self._data_in.copy()
        self.output_data = self._plugin.transform(self.output_data)

    def get_result(self) -> DataInterface:
        return self.output_data
