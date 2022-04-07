from typing import Any
import xml.etree.ElementTree as ET
from os import path
from ast import literal_eval

class Settings(object):
    def __init__(self):
        self.tree = None
        self.pipeline_tree = None
        self.data_tree = None
        self.loaded_modules = {}
        self.loaded_data_options = {}

    def load_XML(self, filename: str):
        """Loads XML file into class. Converts relative paths into absolute first.
        """
        if filename[0] == ".":
            self.filename = path.join(path.dirname(__file__), filename)
        elif filename[0] == "/":
            self.filename = filename
        self.tree = ET.parse(self.filename)
        self.parse_XML()

    def parse_XML(self):
        self.root = s.tree.getroot()
        self.parse_pipeline()
        self.parse_data_structure()

    def parse_text_to_list(self, element: ET.Element) -> list:
        new = element.text.replace(" ", "")
        out = new.split("\n")
        out = [item for item in out if item != ""]
        for idx in range(0,len(out)):
            if "[" in out[idx] and "]" in out[idx]:
                out[idx] = literal_eval(out[idx])
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
                "module_type": module_type,
                "plugin_name": plugin_name,
                "class_list": class_list
            }

    def parse_data_structure(self):
        self.data_tree = self.root.find("datastructure")
        for child in self.data_tree:
            self.loaded_data_options[child.tag]\
                = self.parse_text_to_list(child)

    def print_pretty(self, element: ET.Element):
        from pprint import PrettyPrinter
        pp = PrettyPrinter(sort_dicts=False)
        pp.pprint(element)

    def print_loaded_modules(self):
        self.print_pretty(self.loaded_modules)

    def print_loaded_data_structure(self):
        self.print_pretty(self.loaded_data_options)

    def append_to_XML(self):
        """Formats XML Tree correctly, then writes to filename
        """
        self.indent(self.root)
        self.tree.write(self.filename)

    def indent(self,
               elem: ET.Element,
               level: int = 0):
        """Formats XML tree to be human-readable before writing to file

        :param elem: xml.etree.ElementTree.Element to be indented
        :param level: int, level of initial indentation
        """
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def add_pipeline_module(self,
                            module_type: str,
                            module_name: str,
                            plugin_type: str,
                            class_list: list
                            ):
        """Append new pipeline module to existing XML file
        :param module_type: string declare type of module (GUI,data_processing etc)
        :param module_name: string give module a user-defined name
        :param plugin_type: string type of plugin to be loaded into module
        :param class_list: list(string) of class labels for plugin
        TODO: This is very specific to the GUI module - need to make more generic
        """
        new_mod = ET.Element(module_type)
        new_mod.set('name', module_name)

        new_plugin = ET.SubElement(new_mod, "plugin")
        new_plugin.set('type', plugin_type)

        new_class_list = ET.SubElement(new_plugin, "class_list")
        new_class_list.text = class_list

        self.pipeline_tree.append(new_mod)
        self.append_to_XML()

    def add_data_structure_field(self,
                                 field_type: str,
                                 value: list,
                                 field_name: str = None):
        new_field = ET.Element(field_type)
        if field_name is not None:
            new_field.set('name', field_name)
        new_field.text = value
        self.data_tree.append(new_field)
        self.append_to_XML()


s = Settings()
s.load_XML("./resources/example_config.xml")
s.print_loaded_modules()
# s.add_pipeline_module("GUI",
#                       "added_mod",
#                       "startpage",
#                       "no+class_list")
# s.add_data_structure_field("replay_buffer", "1")
s.print_loaded_data_structure()
