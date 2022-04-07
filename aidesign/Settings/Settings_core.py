import xml.etree.ElementTree as ET
from os import path

class Settings(object):
    def __init__(self):
        self.tree = None
        self.pipeline_tree = None
        self.data_tree = None
        self.loaded_modules = {}
        self.loaded_data_options = {}

    def load_XML(self,filename):
        if filename[0] == ".":
            self.filename = path.join(path.dirname(__file__),filename)
        elif filename[0] == "/":
            self.filename = filename
        self.tree = ET.parse(self.filename)
        self.parse_XML()

    def parse_XML(self):
        self.root = s.tree.getroot()
        self.parse_pipeline()
        self.parse_data_structure()

    def parse_text_to_list(self,element):
        out = []
        new = element.text.replace(" ", "")
        out = new.split("\n")
        out = [item for item in out if item != "" ]
        return out
        

    def parse_pipeline(self):
        self.pipeline_tree = self.root.find("pipeline")
        for child in self.pipeline_tree:
            module_name = child.attrib["name"]
            module_type = child.tag
            plugin = child.find("plugin")
            plugin_name = plugin.attrib["type"]
            class_list = self.parse_text_to_list(plugin.find("class_list"))
            self.loaded_modules[module_name] = {
                "module_type" : module_type,
                "plugin_name" : plugin_name,
                "class_list" : class_list
            }

    def parse_data_structure(self):
        self.data_tree = self.root.find("datastructure")
        for child in self.data_tree:
            self.loaded_data_options[child.tag]\
                            = self.parse_text_to_list(child)
            
        
    def print_pretty(self,element):
        from pprint import PrettyPrinter
        pp = PrettyPrinter(sort_dicts=False)
        pp.pprint(element)

    def print_loaded_modules(self):
        self.print_pretty(s.loaded_modules)

    def print_loaded_data_structure(self):
        self.print_pretty(s.loaded_data_options)

s = Settings()
s.load_XML("./resources/example_config.xml")
s.print_loaded_data_structure()
