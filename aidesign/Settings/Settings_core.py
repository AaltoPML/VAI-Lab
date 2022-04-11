import xml.etree.ElementTree as ET
from os import path
from ast import literal_eval


class Settings(object):
    def __init__(self):
        self.tree = None
        self.pipeline_tree = None
        self.data_tree = None

        self.initialisation_options = {}
        self.output_options = {}

        self.loaded_modules = {}
        self.loaded_data_options = {}

        self.valid_tags = {
            "pipeline": "declaration",
            "datastructure": "declaration",
            "Initialise": "entry_point",
            "Output": "exit_point",
            "GUI": "module",
            "DataProcessing": "module",
            "loop": "loop"
        }

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
        self.root = self.tree.getroot()

        self.pipeline_tree = self.root.find("pipeline")
        self.parse_tags(self.pipeline_tree, self.loaded_modules)

        self.parse_data_structure()

    def parse_tags(self, element, parent):
        for child in element:
            try:
                tag_type = self.valid_tags[child.tag]
                getattr(self, "add_{}".format(tag_type))(child, parent)
            except KeyError:
                print("\nError: Invalid XML Tag.")
                print("XML tag \"{0}\" not found".format(child.tag))
                print("Valid tags are: ")
                print("\t- {}".format(",\n\t- ".join([*self.valid_tags])))
                print("\n")

    def add_module(self, element, parent):
        module_name = element.attrib["name"]
        module_type = element.tag
        plugin = element.find("plugin")
        plugin_name = plugin.attrib["type"]
        parent[module_name] = {
            "module_type": module_type,
            "plugin_name": plugin_name,
            "options":{}
        }
        self.parse_plugin_options(plugin, parent[module_name]["options"])
        self.add_relationships(element, parent[module_name])

    def parse_plugin_options(self, element, parent):
        for child in element:
            if child.text != None: 
                val = self.parse_text_to_list(child)
            elif child.attrib["value"] != None:
                val = child.attrib["value"]
            parent[child.tag] = val
            

    def add_entry_point(self, element, parent):
        initialiser_name = element.attrib["name"]
        parent[initialiser_name] = {}
        init_data_file = element.find("initial_data").attrib["file"]
        goal_data_file = element.find("goal").attrib["file"]
        parent[initialiser_name]["init_data_file"] = init_data_file
        parent[initialiser_name]["goal_data_file"] = goal_data_file
        self.add_relationships(element, parent[initialiser_name])

    def add_exit_point(self, element, parent):
        parent["output"] = {}
        parent["output"]["save_fields"] = self.parse_text_to_list(element.find("out_data"))
        parent["output"]["save_dir"] = element.find("save_to").attrib["file"]
        self.add_relationships(element, parent["output"])
        

    def add_loop(self, element, parent):
        loop_name = element.attrib["name"]
        parent[loop_name] = {
            "type": element.attrib["type"],
            "condition": element.attrib["condition"]
        }
        self.parse_tags(element, parent[loop_name])

    def add_relationships(self, element, parent):
        parent["parents"] = []
        parent["children"] = []
        for rel in element.find("relationships"):
            if rel.tag == "parent":
                parent["parents"].append(rel.attrib["name"])
            elif rel.tag == "child":
                parent["children"].append(rel.attrib["name"])

    def parse_data_structure(self):
        self.data_tree = self.root.find("datastructure")
        for child in self.data_tree:
            self.loaded_data_options[child.tag]\
                = self.parse_text_to_list(child)

    def parse_text_to_list(self, element: ET.Element) -> list:
        new = element.text.replace(" ", "")
        out = new.split("\n")
        out = [item for item in out if item != ""]
        for idx in range(0, len(out)):
            if "[" in out[idx] and "]" in out[idx]:
                out[idx] = literal_eval(out[idx])
        return out

    def print_pretty(self, element: ET.Element):
        from pprint import PrettyPrinter
        pp = PrettyPrinter(sort_dicts=False, width=100)
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

    def append_pipeline_module_to_file(self,
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

    def append_data_structure_field_to_file(self,
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
# s.append_pipeline_module_to_file("GUI",
#                       "added_mod",
#                       "startpage",
#                       "no+class_list")
# s.append_data_structure_field_to_file("replay_buffer", "1")
# s.print_loaded_data_structure()
