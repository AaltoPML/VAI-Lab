class DataStorage(object):
    def __init__(self):
        self.node_name = None
        self.plugin_name = None
        self.output_data = None

    def set_input_data(self, data):
        self.input_data = data

    def set_target_data(self, data):
        self.target_data = data

    def _load_plugin(self):
        pass

    def set_plugin_name(self, plugin_name):
        self.plugin_name = plugin_name
        self._load_plugin()

    def set_options(self, options):
        self.options = options

    def solve(self):
        # send the input data to the modelling plugin and assign it to an output property
        pass

    def get_result(self):
        return self.output_data
