import time
from sys import exit
from os.path import join
from typing import Dict, List, Tuple, Union
import pickle

from vai_lab._import_helper import import_module, rel_to_abs
from vai_lab._plugin_helpers import PluginSpecs
from vai_lab._types import ModuleInterface, PluginSpecsInterface
from vai_lab.GUI.GUI_core import GUI
from vai_lab.Data.Data_core import Data
from vai_lab.Data.xml_handler import XML_handler


class Core:
    def __init__(self) -> None:
        self.data = {}
        self.data['Initialiser'] = Data()
        self._xml_handler = XML_handler()
        self._avail_plugins: PluginSpecsInterface = PluginSpecs()
        
        self.loop_level: int = 0
        self._initialised: bool = False
        self.status_logger:Dict = {}
        self._debug = False

    def _launch(self):
        gui_app = GUI()
        gui_app._debug = self._debug
        gui_app.set_avail_plugins(self._avail_plugins)
        gui_app.set_gui_as_startpage()
        gui_output = gui_app.launch()
        if not self._debug:
            try:
                self.load_config_file(gui_output["xml_filename"])
            except:
                raise Exception("No XML File Selected. Cannot Run Pipeline")

    def load_config_file(self, filename: Union[str,List,Tuple]):
        """Loads XML file into XML_handler object.
        Parses filename first, if needed.
        """
        if type(filename) == list or type(filename) == tuple:
            filedir:str = join(*filename)
        else:
            filedir = str(filename)
        self._xml_handler.load_XML(filedir)
        self._initialised = True

    def _load_data(self, specs, module = 'Initialiser') -> None:
        """Loads data from XML file into Data object"""
        init_data_fn = self._xml_handler.data_to_load(modules=specs, module=module)
        if module not in self.data.keys():
            self.data[module] = Data()
        if isinstance(init_data_fn, str):
            self.data[module].import_existing_data(init_data_fn, self.data)
        elif isinstance(init_data_fn, dict):
            self.data[module].import_data_from_config(init_data_fn)

    def _execute_module(self, specs):
        """Executes named module with given options
        Imports, instantiates, sets params, then launches module

        :param specs: dict of module to be executed
        """
        mod: ModuleInterface = import_module(globals(), specs["module_type"]).__call__()
        mod._debug = self._debug
        mod.set_avail_plugins(self._avail_plugins)
        self._load_data(specs, specs["name"])
        mod.set_options(specs)
        if specs["name"] == 'User Interaction':
            mod._load_plugin(specs["plugin"]["plugin_name"])
            mod.set_data_in(self.data[specs["name"]])
        else:
            mod._load_plugin(self.data[specs["name"]])
        print("\t"*self.loop_level
                + specs["module_type"]
                + " module: \"{}\" ".format(specs["name"])
                + "processing..."
              )
        mod.launch()
        self.data[specs["name"]] = mod.get_result()

    def _execute_loop(self, specs):
        if  hasattr(self,"_execute_{}_loop".format(specs["type"])):
            print("\t"*self.loop_level
                        + "Starting "
                        + specs["type"]
                        + " loop: \"{}\"".format(specs["name"])
                        + " ...")
            self.loop_level += 1
            getattr(self, "_execute_{}_loop".format(specs["type"]))(specs)
            self.loop_level -= 1
        else:
            print("\nError: Invalid Loop Type.")
            print("Loop \"{0}\" with type \"{1}\" not recognised".format(
                specs["name"], specs["type"]))

    def _execute_entry_point(self, specs):
        """Placeholder: Will parse the initialiser module when ready"""
        pass

    def _execute_exit_point(self, specs):
        """ Runs the Output module """
        if all(k in specs['plugin']['options'] for k in ('outdata', 'outpath')):
            data_out = {}
            if type(specs['plugin']['options']['outdata']) is list:
                for module in specs['plugin']['options']['outdata']:
                    data_out[module] = self.data[module]
            elif type(specs['plugin']['options']['outdata']) is str:
                data_out[specs['plugin']['options']['outdata']] = self.data[specs['plugin']['options']['outdata']]

            with open(rel_to_abs(specs['plugin']['options']['outpath']), 'wb') as handle:
                pickle.dump(data_out, handle, protocol=pickle.HIGHEST_PROTOCOL)
                
    def _parse_loop_condition(self, condition):
        try:
            condition = int(condition)
            
            if isinstance(condition, int):
                return range(0, condition)
        except:
            print("Condition \"{0}\" cannot be parsed".format(condition))
            print(
                "Other formats in development. Only ranged for loops are working currently")

    def _execute_for_loop(self, specs):
        condition = self._parse_loop_condition(specs["condition"])
        for c in condition:
            self._execute(specs)

    def _show_updated_tracker(self):
        self.gui_app = GUI()
        self.gui_app._debug = self._debug
        self.gui_app.set_avail_plugins(self._avail_plugins)
        self.gui_app.set_gui_as_progress_tracker(self.status_logger)
        self.gui_app._append_to_output("xml_filename", self._xml_handler.filename)
        return self.gui_app.launch()
    
    def _init_status(self, modules):
        for key in [key for key, val in modules.items() if type(val) == dict]:
            self.status_logger[modules[key]['name']] = {}
            if modules[key]['class'] == "loop":
                self._init_status(modules[key])

    def _add_status(self, module, key, value):
        self.status_logger[module['name']][key] = value

    def _progress_start(self, module):
        self._add_status(module, 'start', self._t)

    def _progress_finish(self, module):
        self._add_status(module, 'finish', self._t)

    @property
    def _t(self):
        return time.strftime('%H:%M:%S', time.localtime())

    def _execute(self, specs):
        """Run elements within a given dictionary.
        Only iterates over dict values that are dicts themselves.
        Non-dict elements cannot contain modules or loops

        :param specs: dict of elements to be executed
        """
        for key in [key for key, val in specs.items() if type(val) == dict]:
            
            self._progress_start(specs[key])
            getattr(self, "_execute_{}".format(specs[key]["class"]))(specs[key])
            self._progress_finish(specs[key])

            if specs[key]["class"] == 'module':
                _tracker = self._show_updated_tracker()

                if not _tracker['terminate']:
                    self.load_config_file(self._xml_handler.filename)
                else:
                    print('Pipeline terminated')
                    exit()

    def _initialise_with_gui(self):
        """Launches GUI when no XML file is specified"""
        print("Loading GUI")
        print("To load existing config, run core.load_config_file(<path_to_file>)")
        self._launch()

    def run(self):
        if not self._initialised:
            self._initialise_with_gui()
        print("Running pipeline...")
        if len(self._xml_handler.loaded_modules) > 0:
            self._load_data(self._xml_handler.loaded_modules)
        
        self._init_status(self._xml_handler.loaded_modules)
        self._execute(self._xml_handler.loaded_modules)
        print("Pipeline Complete")