import xml.etree.ElementTree as ET
from os import path
from ast import literal_eval


class Settings(object):
    def __init__(self, filename: str = None):
        """Loads XML file and parses into nested dictionaries
        This module is used as the backbone for all future modules.
        If filename is not given, can be passed straight to self.load_XML()

        :param filename [optional]: filename from which to load XML
        """
        self.tree = None
        self.pipeline_tree = None
        self.loaded_modules = {}

        self.data_tree = None
        self.loaded_data_options = {}

        self.initialisation_options = {}
        self.output_options = {}

        """valid_tags lists the available XML tags and their function
        TODO: populate the modules in this list automatically
        """
        self.valid_tags = {
            "pipeline": "declaration",
            "datastructure": "declaration",
            "Initialiser": "entry_point",
            "Output": "exit_point",
            "GUI": "module",
            "DataProcessing": "module",
            "loop": "loop"
        }

        if filename is not None:
            self.load_XML(filename)

    def set_filename(self, filename: str):
        """Converts relative paths into before setting."""
        if filename[0] == ".":
            self.filename = path.join(path.dirname(__file__), filename)
        elif filename[0] == "/":
            self.filename = filename

    def new_config_file(self, filename: str = None):
        if filename is not None: 
            self.set_filename(filename)
        self.tree = ET.ElementTree(ET.Element("Settings"))
        self.root = self.tree.getroot()
        self.pipeline_tree = ET.SubElement(self.root,"pipeline")
        self.data_tree = ET.SubElement(self.root,"datastructure")

    def load_XML(self, filename: str):
        """Loads XML file into class. 
        """
        if filename != None:
            self.set_filename(filename)
        self.tree = ET.parse(self.filename)
        self.parse_XML()

    def parse_XML(self):
        self.root = self.tree.getroot()

        self.pipeline_tree = self.root.find("pipeline")
        self.parse_tags(self.pipeline_tree, self.loaded_modules)

        self.parse_data_structure()

    def parse_tags(self, element, parent):
        """Detect tags and send them to correct method for parsing
        Uses getattr to call the correct method

        :param elem: xml.etree.ElementTree.Element to be parsed
        :param parent: dict or dict fragment parsed tags will be appened to
        """
        for child in element:
            try:
                tag_type = self.valid_tags[child.tag]
                getattr(self, "load_{}".format(tag_type))(child, parent)
            except KeyError:
                print("\nError: Invalid XML Tag.")
                print("XML tag \"{0}\" not found".format(child.tag))
                print("Valid tags are: ")
                print("\t- {}".format(",\n\t- ".join([*self.valid_tags])))
                print("\n")

    def load_module(self, element, parent):
        """Parses tags associated with modules and appends to parent dict

        :param elem: xml.etree.ElementTree.Element to be parsed
        :param parent: dict or dict fragment parsed tags will be appened to
        """
        module_name = element.attrib["name"]
        module_type = element.tag
        plugin = element.find("plugin")
        plugin_name = plugin.attrib["type"]
        parent[module_name] = {
            "module_type": module_type,
            "plugin_name": plugin_name,
            "options": {}
        }
        self.load_plugin_options(plugin, parent[module_name]["options"])
        self.load_relationships(element, parent[module_name])

    def load_plugin_options(self, element, parent):
        """Parses tags associated with plugins and appends to parent dict

        :param elem: xml.etree.ElementTree.Element to be parsed
        :param parent: dict or dict fragment parsed tags will be appened to
        """
        for child in element:
            if child.text != None:
                val = self.parse_text_to_list(child)
            elif child.attrib["value"] != None:
                val = child.attrib["value"]
            parent[child.tag] = val

    def load_entry_point(self, element, parent):
        """Parses tags associated with initialiser and appends to parent dict

        :param elem: xml.etree.ElementTree.Element to be parsed
        :param parent: dict or dict fragment parsed tags will be appened to
        """
        initialiser_name = element.attrib["name"]
        parent[initialiser_name] = {}
        init_data_file = element.find("initial_data").attrib["file"]
        goal_data_file = element.find("goal").attrib["file"]
        parent[initialiser_name]["init_data_file"] = init_data_file
        parent[initialiser_name]["goal_data_file"] = goal_data_file
        self.load_relationships(element, parent[initialiser_name])

    def load_exit_point(self, element, parent):
        """Parses tags associated with output and appends to parent dict

        :param elem: xml.etree.ElementTree.Element to be parsed
        :param parent: dict or dict fragment parsed tags will be appened to
        """
        parent["output"] = {}
        parent["output"]["save_fields"] = self.parse_text_to_list(
            element.find("out_data"))
        parent["output"]["save_dir"] = element.find("save_to").attrib["file"]
        self.load_relationships(element, parent["output"])

    def load_loop(self, element, parent):
        """Parses tags associated with loops and appends to parent dict

        :param elem: xml.etree.ElementTree.Element to be parsed
        :param parent: dict or dict fragment parsed tags will be appened to
        """
        loop_name = element.attrib["name"]
        parent[loop_name] = {
            "type": element.attrib["type"],
            "condition": element.attrib["condition"]
        }
        self.parse_tags(element, parent[loop_name])

    def load_relationships(self, element, parent):
        """Parses tags associated with relationships and adds to parent dict

        :param elem: xml.etree.ElementTree.Element to be parsed
        :param parent: dict or dict fragment parsed tags will be appened to
        """
        parent["parents"] = []
        parent["children"] = []
        for rel in element.find("relationships"):
            if rel.tag == "parent":
                parent["parents"].append(rel.attrib["name"])
            elif rel.tag == "child":
                parent["children"].append(rel.attrib["name"])

    def parse_data_structure(self):
        """Parses tags associated with data structure"""
        self.data_tree = self.root.find("datastructure")
        for child in self.data_tree:
            self.loaded_data_options[child.tag]\
                = self.parse_text_to_list(child)

    def parse_text_to_list(self, element: ET.Element) -> list:
        """Formats raw text data

        :param elem: xml.etree.ElementTree.Element to be parsed
        :returns out: list containing parsed text data
        """
        new = element.text.strip().replace(" ", "")
        out = new.split("\n")
        raw_elem_text = str()
        for idx in range(0, len(out)):
            raw_elem_text = (raw_elem_text+"\n{}").format(out[idx])
            if "[" in out[idx] and "]" in out[idx]:
                out[idx] = literal_eval(out[idx])
        element.text = raw_elem_text
        return out

    def print_pretty(self, element: ET.Element):
        """Print indented dictionary to screen"""
        from pprint import PrettyPrinter
        pp = PrettyPrinter(sort_dicts=False, width=100)
        pp.pprint(element)

    def print_loaded_modules(self):
        """Print indented pipeline specifications to screen"""
        self.print_pretty(self.loaded_modules)

    def print_loaded_data_structure(self):
        """Print indented data structure specifications to screen"""
        self.print_pretty(self.loaded_data_options)

    def write_to_XML(self):
        """Formats XML Tree correctly, then writes to filename
        TODO: add overwrite check and alternate filename option
        """
        self.indent(self.root)
        self.tree.write(self.filename)

    def indent(self, elem: ET.Element, level: int = 0):
        """Formats XML tree to be human-readable before writing to file

        :param elem: xml.etree.ElementTree.Element to be indented
        :param level: int, level of initial indentation
        """
        sep = "    "
        i = "\n" + level*sep
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + sep
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
            if elem.text:
                elem.text = elem.text.replace("\n", ("\n" + (level+1)*sep))
                elem.text = ("{0}{1}").format(elem.text, i)

    def get_element_from_name(self, name: str):
        """Find a module name and return its parent tags"""
        if name == None:
            return self.pipeline_tree
        elems = self.root.findall(".//*[@name='{0}']".format(name))
        unique_elem = [e for e in elems if e.tag != "parent" and e.tag != "child"]
        assert len(unique_elem)<2, "Error: More than one tag with same identifier"
        assert len(unique_elem)>0, "Error: No element exists with name \"{0}\"".format(name)
        return unique_elem[0]

    def get_all_elements_with_tag(self, tag: str):
        """Return all elements with a given tag
        
        :param tag: string with tag name
        """
        elems = self.root.findall(".//*{0}".format(tag))
        return elems

    def loop_rels_autofill(self,
                            elem:ET.Element,
                            xml_child:str):
        """Add the name of a new nested module to the relationships of a loop
        
        :param elem: ET.Element
        """
        if elem.tag != "loop":
            return elem
        rels_elem = elem.find("relationships")
        if rels_elem == None:
            rels_elem = ET.SubElement(elem, "relationships")
        new_child = ET.SubElement(rels_elem, "child")
        new_child.set("name",xml_child)
        return elem

    def add_relationships(self, 
                            elem:ET.Element, 
                            parents:list, 
                            children:list):
                                    
        new_relationships = ET.SubElement(elem, "relationships")
        for p in parents:
            new_parent = ET.SubElement(new_relationships, "parent")
            new_parent.set('name', p)
        for c in children:
            new_child = ET.SubElement(new_relationships, "child")
            new_child.set('name', c)
        return elem

    def add_coords(self, 
                    elem:ET.Element, 
                    coords:list=None):
        if coords == None:
            return elem
        coords_elem = elem.find("coordinates")
        if coords_elem == None:
            coords_elem = ET.SubElement(elem, "coordinates")
        coords_elem.text = str("\n{0}".format(coords))
        return elem

    def append_pipeline_module(self,
                                module_type: str,
                                module_name: str,
                                plugin_type: str,
                                plugin_options: dict,
                                parents: list,
                                children: list,
                                xml_parent_element: str,
                                coords: list = None
                                ):
        """Append new pipeline module to existing XML elementTree to be written later
        
        :param module_type: string declare type of module (GUI,data_processing etc)
        :param module_name: string give module a user-defined name
        :param plugin_type: string type of plugin to be loaded into module
        :param plugin_options: dict where keys & values are options & values
        :param parents: list of parent names for this module (can be empty)
        :param children: list of child names for this module (can be empty)
        :param xml_parent_element: str containing name of parent Element for new module
        :param coords [optional]: list of coordinates for GUI canvas
        """
        xml_parent_element = self.get_element_from_name(xml_parent_element)

        new_mod = ET.Element(module_type)
        new_mod.set('name', module_name)

        new_plugin = ET.SubElement(new_mod, "plugin")
        new_plugin.set('type', plugin_type)

        for key in plugin_options.keys():
            new_option = ET.SubElement(new_plugin, key)
            if isinstance(plugin_options[key], list):
                option_text = ("\n{}".format(
                    "\n".join([*plugin_options[key]])))
                new_option.text = option_text

            elif isinstance(plugin_options[key], str):
                new_option.set('value', plugin_options[key])

        if xml_parent_element.tag =="loop":
            parents.append(xml_parent_element.attrib["name"])
        new_mod = self.add_relationships(new_mod,parents,children)
        new_mod = self.add_coords(new_mod,coords)

        self.loop_rels_autofill(xml_parent_element, module_name)
        xml_parent_element.append(new_mod)

    def append_pipeline_loop(self,
                                loop_type: str,
                                condition: str,
                                loop_name: str,
                                parents: list,
                                children: list,
                                xml_parent_element: str = None, 
                                coords: list = None
                                ):
        """Append new pipeline module to existing XML file
        
        :param loop_type: string declare type of loop (for/while/manual etc)
        :param loop_name: string give loop a user-defined name
        :param plugin_type: string type of plugin to be loaded into module
        :param parents: list of parent names for this module (can be empty)
        :param children: list of child names for this module (can be empty)
        :param xml_parent_element: str containing name of parent Element for new module
        :param coords [optional]: list of coordinates for GUI canvas
        """
        xml_parent_element = self.get_element_from_name(xml_parent_element)

        new_loop = ET.Element("loop")
        new_loop.set('type', loop_type)
        new_loop.set('condition', condition)
        new_loop.set('name', loop_name)

        if xml_parent_element.tag =="loop":
            parents.append(xml_parent_element.attrib["name"])
        new_loop = self.add_relationships(new_loop,parents,children)
        new_loop = self.add_coords(new_loop,coords)

        self.loop_rels_autofill(xml_parent_element, loop_name)
            
        xml_parent_element.append(new_loop)


    def append_data_structure_field(self,
                                            field_type: str,
                                            value: list,
                                            field_name: str = None):
        """Add new tags for data structure to XML file

        :param field_type: str of desired XML tag to add
        :param value: list of values for field_type
        :param field_name [optional]: str with user defined name for tag
        """
        new_field = ET.Element(field_type)
        if field_name is not None:
            new_field.set('name', field_name)
        new_field.text = value
        self.data_tree.append(new_field)



# Use case examples:
# s = Settings("./resources/example_config.xml")
# s = Settings()
# s.new_config_file("./resources/example_config.xml")
# s.get_all_elements_with_tag("loop")
# s.load_XML("./resources/example_config.xml")
# s.print_loaded_modules()
# s.write_to_XML()
# s.append_pipeline_loop("for",
#                       "10",
#                       "my_loop_3",
#                       ["Init"],
#                       [])
# s.append_pipeline_module("GUI",
#                       "added_mod",
#                       "startpage",
#                       {"class_list":["test_1","test_2"],"class_list_2":["test_1","test_2"]},
#                       ["For Loop 1"],
#                       ["Output"],
#                       None,
#                       [2,3,4,5])
# s.write_to_XML()
# s.append_data_structure_field_to_file("replay_buffer", "1")
# s.print_loaded_data_structure()
