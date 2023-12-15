from vai_lab.Data.Data_core import Data
from vai_lab._import_helper import import_plugin_absolute

class InputData(Data):
    def __init__(self):
        super().__init__()
        self.node_name = None
        self.plugin_name = None
        self.output_data = None

    def set_data_in(self, data_in) -> None:
        """Pass existing data from another module to be stored in this class"""
        self._data_in = data_in

    def load_data_from_file(self, filename: str, data_id: str) -> None:
        """Load data from file. Calls parent class method to store data in self.data"""
        super().import_data(filename, data_id)

    def set_options(self, module_config: dict) -> None:
        """Send configuration arguments to plugin

        :param module_config: dict of settings to configure the plugin
        """
        self._module_config = module_config

    def set_avail_plugins(self, avail_plugins) -> None:
        self._avail_plugins = avail_plugins

    def _load_plugin(self, data_in) -> None:
        avail_plugins = self._avail_plugins.find_from_readable_name(
            self._module_config["plugin"]["plugin_name"])
        self.set_data_in(data_in)
        self._plugin = import_plugin_absolute(globals(),
                                                    avail_plugins["_PLUGIN_PACKAGE"],
                                                    avail_plugins["_PLUGIN_CLASS_NAME"])\
                                                    .__call__(self._module_config["plugin"], data_in)

    def get_result(self):
        return self._data_in
