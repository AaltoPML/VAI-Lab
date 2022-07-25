from aidesign.utils.import_helper import import_module
from aidesign.Data.xml_handler import XML_handler
from aidesign.GUI.GUI_core import GUI
from aidesign.Data.Data_core import Data
from aidesign.utils.plugin_helpers import PluginSpecs


class Core(object):
    def __init__(self) -> None:
        self._xml_handler = XML_handler()
        self._avail_plugins = PluginSpecs()
        self.data = Data()
        self.loop_level = 0
        self.setup_complete = False

    def launch(self):
        gui_app = GUI()
        gui_app.set_avail_plugins(self._avail_plugins)
        gui_app.set_gui_as_startpage()
        gui_output = gui_app.launch()
        if not gui_app.closed:
            try:
                self.load_config_file(gui_output["xml_filename"])
            except:
                raise Exception("No XML File Selected. Cannot Run Pipeline")
            self.run()
            self._load_data()

    def load_config_file(self, filename: str):
        self._xml_handler.load_XML(filename)
        self.setup_complete = True

    def _load_data(self):
        init_data_fn = self._xml_handler.data_to_load
        self.data.import_data_from_config(init_data_fn)

    def _execute_module(self, specs):
        """Executes named module with given options
        Imports, instantiates, sets params, then launches module

        :param specs: dict of module to be executed
        """
        mod = import_module(globals(), specs["module_type"]).__call__()
        mod.set_avail_plugins(self._avail_plugins)
        mod.set_data_in(self.data)
        mod.set_options(specs)
        print("\t"*self.loop_level
                + specs["module_type"]
                + " module: \"{}\"".format(specs["name"])
                + "processing..."
              )
        mod.launch()
        self.data = mod.get_result()

    def _execute_loop(self, specs):
        try:
            print("\t"*self.loop_level
                        + specs["type"]
                        + " loop: "
                        + "\"{}\"".format(specs["name"])
                        + " starting...")
            self.loop_level += 1
            getattr(self, "_execute_{}_loop".format(specs["type"]))(specs)
            self.loop_level -= 1
        except KeyError:
            print("\nError: Invalid Loop Type.")
            print("Loop \"{0}\" with type \"{1}\" not recognised".format(
                specs.key, specs["type"]))

    def _execute_entry_point(self, specs):
        """Placeholder: Will parse the initialiser module when ready"""
        pass

    def _execute_exit_point(self, specs):
        """Placeholder: Will parse the Output module when ready"""
        pass

    def _parse_condition(self, condition):
        try:
            condition = int(condition)
            
            if isinstance(condition, int):
                return range(0, condition)
        except:
            print("Condition \"{0}\" cannot be parsed".format(condition))
            print(
                "Other formats in in development. Only ranged for loops are working currently")

    def _execute_for_loop(self, specs):
        condition = self._parse_condition(specs["condition"])
        for c in condition:
            self._execute(specs)

    def _execute(self, specs):
        """Run elements within a given dictionary.
        Only interates over dict values that are dicts themselves.
        Non-dict elements cannot contain modules or loops

        :param specs: dict of elements to be executed
        """
        for key in [key for key, val in specs.items() if type(val) == dict]:
            getattr(self, "_execute_{}".format(
                specs[key]["class"]))(specs[key])

    def run(self):
        if not self.setup_complete:
            print("No pipeline specified. Running GUI.")
            print("To load existing config, run core.load_config_file(<path_to_file>)")
            self.launch()
        print("Running pipeline...")
        self._load_data()
        self._execute(self._xml_handler.loaded_modules)
        print("Pipeline Complete")
