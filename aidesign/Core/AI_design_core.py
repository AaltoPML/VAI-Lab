from aidesign.utils.import_helper import import_module
from aidesign.Settings.Settings_core import Settings
from aidesign.GUI.GUI_core import GUI


class Core(Settings):
    def __init__(self) -> None:
        super().__init__()
        self.loop_level = 0

    def launch(self):
        gui_app = GUI()
        gui_app.set_plugin_name('main')
        gui_output = gui_app.launch()
        if not gui_app.closed:
            try:
                self.load_config_file(gui_output["xml_filename"])
            except:
                raise Exception("No XML File Selected. Cannot Run Pipeline")
            self.run()

    def load_config_file(self, filename: str):
        self.load_XML(filename)

    def _execute_module(self, specs):
        """Executes named module with given options
        Imports, instantiates, sets params, then launches module

        :param specs: dict of module to be executed
        """
        mod = import_module(globals(), specs["module_type"])()
        mod.set_options(specs)
        print("\t"*self.loop_level
                + specs["module_type"]
                + " module: \"{}\"".format(specs["name"])
                + "processing..."
              )
        mod.launch()

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
        print("Running pipeline...")
        self._execute(self.loaded_modules)
        print("Pipeline Complete")
