from vai_lab._import_helper import import_plugin_absolute
from vai_lab._types import PluginSpecsInterface, DataInterface, EnvironmentPluginInterface

class Environment(object):
    def __init__(self) -> None:
        self.output_data: DataInterface

    def set_avail_plugins(self, avail_plugins: PluginSpecsInterface) -> None:
        self._avail_plugins = avail_plugins

    def set_data_in(self, data_in: DataInterface) -> None:
        self._data_in = data_in

    def _load_plugin(self, data_in) -> None:
        self._plugin_name = self._module_config["plugin"]["plugin_name"]
        avail_plugins = self._avail_plugins.find_from_readable_name(
            self._plugin_name)
        self.set_data_in(data_in)
        self._plugin: EnvironmentPluginInterface = import_plugin_absolute(globals(),
                                              avail_plugins["_PLUGIN_PACKAGE"],
                                              avail_plugins["_PLUGIN_CLASS_NAME"])\
            .__call__(self._module_config["plugin"], data_in)

    def set_options(self, module_config: dict) -> None:
        """Send configuration arguments to plugin

        :param module_config: dict of settings to configure the plugin
        """
        self._module_config = module_config
        self._load_plugin(self._module_config["plugin"]["plugin_name"])

    def launch(self) -> None:
        self._plugin.connect()
        self._plugin.load_model()
        self._plugin.run_simulation()
        

    def get_result(self) -> DataInterface:
        # return self.output_data
        return self._data_in
