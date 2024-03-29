from os import path
from ast import literal_eval
from typing import Any, Dict, List, Optional, Union
import xml.etree.ElementTree as ET

# Allows standalone testing 
if not __package__:
    import sys
    root_mod = path.dirname(path.dirname(path.dirname(__file__)))
    sys.path.append(root_mod)

from vai_lab._import_helper import get_lib_parent_dir, rel_to_abs


class XML_handler:
    def __init__(self, filename: str = None):
        """Loads XML file and parses into nested dictionaries
        This module is used as the backbone for all future modules.
        If filename is not given, can be passed straight to self.load_XML()
        :param filename [optional]: filename from which to load XML
        """
        self.lib_base_path = get_lib_parent_dir()
        self.loaded_modules: Dict[str, Dict] = {}

        """valid_tags lists the available XML tags and their function
        TODO: populate the modules in this list automatically
        TODO: Can extend the plugin_helpers.py script to automatically populate these things
        """
        self._valid_tags: Dict[str, str] = {
            "pipeline": "declaration",
            "relationships": "relationships",
            "plugin": "plugin",
            "method": "method",
            "options": "options",
            "coordinates": "list",
            "Initialiser": "entry_point",
            "inputdata": "data",
            "Output": "exit_point",
            "UserInteraction": "module",
            "DataProcessing": "module",
            "Modelling": "module",
            "InputData": "module",
            "DecisionMaking": "module",
            "Environment": "module",
            "DataStorage": "module",
            "loop": "loop"
        }

        if filename is not None:
            self.load_XML(filename)

    def _check_filename_abs_rel(self, filename: str):
        """Checks if path is relative or absolute
        If absolute, returns original path 
        If relative, converts path to absolute by appending to base directory
        """
        return path.normpath(path.join(self.lib_base_path, filename))

    def _check_file_exists(self, filename: str):
        """Checks if a given path exists
        Convert any rel path to abs first
        :returns: 
            - True if file exists
            - False if file does not exist
        """
        abs_path = self._check_filename_abs_rel(filename)
        return path.exists(abs_path)

    def set_filename(self, filename: str):
        """Sets filename. Converts relative paths to absolute first."""
        self.filename: str = self._check_filename_abs_rel(filename)

    def append_initialiser(self):
        self.append_pipeline_module("Initialiser",
                                    "Initialiser",
                                    None,
                                    None,
                                    [],
                                    [],
                                    None,
                                    [0, 0, 0])

    def new_config_file(self, filename: str = None) -> None:
        """Constructs new XML file with minimal format"""
        if filename is not None:
            self.set_filename(filename)
        self.tree = ET.ElementTree(ET.Element("pipeline"))
        self.root = self.tree.getroot()
        self.append_initialiser()

    def load_XML(self, filename: str) -> None:
        """Loads XML file into class. 
        """
        if filename != None:
            self.set_filename(filename)
        if hasattr(self, 'tree'):
            prev_tree = self.tree
            self.tree = self._combine_XML(prev_tree.getroot(), ET.parse(self.filename).getroot())
        else:
            self.tree = ET.parse(self.filename)
        self._parse_XML()

    def _combine_XML(self, tree1, tree2):
        """
        This function recursively updates either the text or the children
        of an element if another element is found in `tree1`, or adds it
        from `tree2` if not found.
        """
        # Create a mapping from tag name to element, as that's what we are fltering with
        mapping = {el.tag: el for el in tree1}
        for el in tree2:
            if len(el) == 0:
                # Not nested
                try:
                    # Update the text
                    mapping[el.tag].text = el.text
                except KeyError:
                    # An element with this name is not in the mapping
                    mapping[el.tag] = el
                    # Add it
                    tree1.append(el)
            else :
                try:
                    # Recursively process the element, and update it in the same way
                    self._combine_XML(mapping[el.tag], el)
                except KeyError:
                    # Not in the mapping
                    mapping[el.tag] = el
                    tree1.append(el)
        return ET.ElementTree(tree1)
        
    def _parse_XML(self) -> None:
        self.root = self.tree.getroot()
        self._parse_tags(self.root, self.loaded_modules)

    def _bullet_list(self, val_list: Union[List[Any], Dict[str, str]]) -> str:
        sep = "\n\t\u2022"
        return sep + " {}".format(("," + sep + " ").join([*val_list]))

    def _parse_tags(self, element: ET.Element, parent: dict) -> None:
        """Detect tags and send them to correct method for parsing
        Uses getattr to call the correct method
        :param elem: xml.etree.ElementTree.Element to be parsed
        :param parent: dict or dict fragment parsed tags will be appened to
        """
        for child in element:
            try:
                tag_type = self._valid_tags[child.tag]
                getattr(self, "_load_{}".format(tag_type))(child, parent)
            except KeyError:
                from sys import exit
                print("\nError: Invalid XML Tag." +
                      "\nXML tag \"{0}\"".format(child.tag) +
                      "in \"{0}\" not found".format(element.tag) +
                      "\nValid tags are:" +
                      self._bullet_list(self._valid_tags))
                exit(1)
            except AssertionError as Error:
                from sys import exit
                print(Error)
                exit(1)

    def _load_module(self, element: ET.Element, parent: dict) -> None:
        """Parses tags associated with modules and appends to parent dict
        :param elem: xml.etree.ElementTree.Element to be parsed
        :param parent: dict or dict fragment parsed tags will be appened to
        """
        module_name = element.attrib["name"]
        module_type = element.tag
        parent[module_name] = {"name": module_name,
                               "class": self._valid_tags[module_type],
                               "module_type": module_type}
        self._parse_tags(element, parent[module_name])

    def _load_plugin(self, element: ET.Element, parent: dict) -> None:
        """Parses tags associated with plugins and appends to parent dict
        :param elem: xml.etree.ElementTree.Element to be parsed
        :param parent: dict or dict fragment parsed tags will be appened to
        """
        parent["plugin"] = {}
        parent["plugin"]["plugin_name"] = element.attrib["type"]
        parent["plugin"]["methods"] = {"_order" : []}
        parent["plugin"]["options"] = {}
        self._parse_tags(element, parent["plugin"])

    def _load_method(self, element: ET.Element, parent: dict) -> None:
        """Parses tags associated with methods and appends to parent dict
        :param elem: xml.etree.ElementTree.Element to be parsed
        :param parent: dict or dict fragment parsed tags will be appened to
        """
        for key in element.attrib:
            parent["methods"]["_order"].append(element.attrib[key])
            parent["methods"][element.attrib[key]] = {'options': {}}
            self._parse_tags(element, parent["methods"][element.attrib[key]])

    def _load_options(self, element: ET.Element, parent: dict) -> None:
        """Parses tags associated with options and appends to parent dict
        :param elem: xml.etree.ElementTree.Element to be parsed
        :param parent: dict or dict fragment parsed tags will be appened to
        """
        for child in element:
            if child.text is not None:
                try:
                    parent["options"][child.tag] = literal_eval(child.text.strip())
                except Exception as exc:
                    val = self._parse_text_to_list(child)
                    parent["options"][child.tag] = (val[0] if len(val) == 1 else val)

            for key in child.attrib:
                if key == "val":
                    parent["options"][child.tag] = child.attrib[key]
                else:
                    parent["options"][child.tag] = {key: child.attrib[key]}

    def _load_entry_point(self, element: ET.Element, parent: dict) -> None:
        """Parses tags associated with initialiser and appends to parent dict
        :param elem: xml.etree.ElementTree.Element to be parsed
        :param parent: dict or dict fragment parsed tags will be appened to
        """
        initialiser_name = element.attrib["name"]
        parent[initialiser_name] = {"name": initialiser_name,
                                    "class": self._valid_tags[element.tag]}
        self._parse_tags(element, parent[initialiser_name])

    def _load_data(self, element: ET.Element, parent: dict) -> None:
        """Parses tags associated with initial data files and appends to parent dict
        :param elem: xml.etree.ElementTree.Element to be parsed
        :param parent: dict or dict fragment parsed tags will be appened to
        """
        data_name = (element.attrib["name"]
                     if "name" in element.attrib else "input_data")
        parent[data_name] = {"name": data_name,
                             "class": "data",
                             "to_load": {}}
        for child in element:
            assert "file" in child.attrib or "folder" in child.attrib or "module" in child.attrib,\
                str("XML Parse Error \
                        \n\tA path to data file must be specified. \
                        \n\t{0} does not contain the \"file\" tag. \
                        \n\tCorrect usage: {0} file = <path-to-file>".format(child.tag))

            if "file" in child.attrib:
                assert self._check_file_exists(child.attrib["file"]),\
                    str("Error: Data file not found. \
                        \n\tFile: {0} does not exist"
                        .format(self._check_filename_abs_rel(child.attrib["file"])))
                parent[data_name]["to_load"][child.tag] = child.attrib["file"]

            if "folder" in child.attrib:
                assert self._check_file_exists(child.attrib["folder"]),\
                    str("Error: Data folder not found. \
                        \n\tFolder: {0} does not exist"
                        .format(self._check_filename_abs_rel(child.attrib["folder"])))
                parent[data_name]["to_load"][child.tag] = child.attrib["folder"]

            if "module" in child.attrib:
                parent[data_name]["to_load"] = child.attrib["module"]          

    def _load_exit_point(self, element: ET.Element, parent: dict) -> None:
        """Parses tags associated with output and appends to parent dict
        :param elem: xml.etree.ElementTree.Element to be parsed
        :param parent: dict or dict fragment parsed tags will be appened to
        """
        parent["Output"] = {"name": "Output",
                            "class": self._valid_tags[element.tag]}
        self._parse_tags(element, parent["Output"])

    def _load_loop(self, element: ET.Element, parent: dict) -> None:
        """Parses tags associated with loops and appends to parent dict
        :param elem: xml.etree.ElementTree.Element to be parsed
        :param parent: dict or dict fragment parsed tags will be appened to
        """
        loop_name = element.attrib["name"]
        parent[loop_name] = {
            "name": loop_name,
            "class": self._valid_tags[element.tag],
            "type": element.attrib["type"].lower(),
            "condition": element.attrib["condition"],
        }
        self._parse_tags(element, parent[loop_name])

    def _load_relationships(self, element: ET.Element, parent: dict) -> None:
        """Parses tags associated with relationships and adds to parent dict
        :param elem: xml.etree.ElementTree.Element to be parsed
        :param parent: dict or dict fragment parsed tags will be appened to
        """
        parent["parents"] = []
        parent["children"] = []
        for rel in element:
            if rel.tag == "parent":
                parent["parents"].append(rel.attrib["name"])
            elif rel.tag == "child":
                parent["children"].append(rel.attrib["name"])

    def _load_list(self, element: ET.Element, parent: dict) -> None:
        """Parses elements consisting of lists, e.g. coordinates
        :param elem: xml.etree.ElementTree.Element to be parsed
        :param parent: dict or dict fragment parsed tags will be appened to
        """
        if element.text is not None:
            parent[element.tag] = self._parse_text_to_list(element)
            if len(parent[element.tag]) == 1:
                parent[element.tag] = parent[element.tag][0]

    def _str_to_num(self, string:str) -> Union[str, int, float]:
        """Converts a string containing only numeric data to float or int
            Otherwise returns string

        :param string: The string to be converted if possible
        :returns out: either a string, float or int
        """
        try:
            return int(string)
        except ValueError:
            pass

        try:
            return float(string)
        except ValueError:
            return string

    def _parse_text_to_list(self, element: ET.Element) -> List:
        """Formats raw text data
        :param elem: xml.etree.ElementTree.Element to be parsed
        :returns out: list containing parsed text data
        """
        if element.text is not None:
            new = element.text.strip()

        out: List[Any] = new.split("\n")
        raw_elem_text = str()
        for idx in range(0, len(out)):
            out[idx] = " ".join(out[idx].split())
            raw_elem_text = (raw_elem_text+"\n{}").format(out[idx])
            if "[" in out[idx] and "]" in out[idx]:
                out[idx] = literal_eval(out[idx])
            if "(" in out[idx] and ")" in out[idx]:
                out[idx] = list(literal_eval(out[idx]))
            if type(out[idx]) == str:
                out[idx] = self._str_to_num(out[idx])
        element.text = raw_elem_text
        return out

    def _print_pretty(self, element: ET.Element):
        """Print indented dictionary to screen"""
        from pprint import PrettyPrinter
        pp = PrettyPrinter(sort_dicts=False, width=100)
        pp.pprint(element)

    def _print_xml_config(self):
        """Print indented pipeline specifications to screen"""
        if len(self.loaded_modules) == 0:
            self._parse_XML()
        self._print_pretty(self.loaded_modules)

    def write_to_XML(self):
        """Formats XML Tree correctly, then writes to filename
        TODO: add overwrite check and alternate filename option
        """
        self._indent(self.root)
        self.tree.write(self.filename)

    def _indent(self, elem: ET.Element, level: int = 0):
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
                self._indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
            if elem.text:
                elem.text = elem.text.replace("\n", ("\n" + (level+1)*sep))
                elem.text = ("{0}{1}").format(elem.text, i)

    def _find_dict_with_key_val_pair(self,
                                     parent: dict,
                                     key: str,
                                     val: Any,
                                     out=None) -> List[Dict[str, str]]:
        """Search nested dict for a given key-value pair
        :param parent: dict to be searched
        :param key: str of key to find
        :param val: val to find in target key
        :param out [optional]: list to append found dicts to
        :returns out: list of dicts containing val pairs if any
        """
        if out is None:
            out = []
        for k in parent.keys():
            if isinstance(parent[k], dict):
                if key in parent[k]:
                    if parent[k][key] == val:
                        out.append(parent[k])
            if isinstance(parent[k], dict):
                self._find_dict_with_key_val_pair(parent[k], key, val, out)
        return out

    def _get_element_from_name(self, name: Union[str, Optional[str]]) -> ET.Element:
        """Find a module name and return its parent tags"""
        if name == None:
            return self.root

        elems = self.root.findall(".//*[@name='{0}']".format(name))

        unique_elem = [e for e in elems if e.tag !=
                       "parent" and e.tag != "child"]

        assert len(unique_elem) < 2,\
            "Error: More than one tag with same identifier"

        assert len(unique_elem) > 0, \
            "Error: No element exists with name \"{0}\"".format(name)

        return unique_elem[0]

    def _get_all_elements_with_tag(self, tag: str):
        """Return all elements with a given tag
        :param tag: string with tag name
        """
        elems = self.root.findall(".//*{0}".format(tag))
        return elems

    def _loop_rels_autofill(self,
                            elem: ET.Element,
                            xml_child: str):
        """Add the name of a new nested module to the relationships of a loop
        :param elem: ET.Element
        :param xml_child:str name of child to be nested in XML
        """
        if elem.tag != "loop":
            return elem
        else:
            return self._add_relationships(elem, [], [xml_child])

    def _add_relationships(self,
                           elem: ET.Element,
                           parents: list,
                           children: list):
        """Add parents and/or children as a subelement
        Checks for duplicates before appending
        :param elem: ET.Element to which the relationship are appeneded
        :param parents: list of strings of parents to be appended
        :param children: list of strings of children to be appended
        """
        rels_elem = elem.find("./relationships")
        if rels_elem is None:
            rels_elem = ET.SubElement(elem, "relationships")
        for p in parents:
            if not elem.findall(".//parent/[@name='{0}']".format(p)):
                new_parent = ET.SubElement(rels_elem, "parent")
                new_parent.set('name', p)
        for c in children:
            if not elem.findall(".//child/[@name='{0}']".format(c)):
                new_child = ET.SubElement(rels_elem, "child")
                new_child.set('name', c)
        return elem

    def append_module_relationships(self,
                                    module_name: str,
                                    parents: list,
                                    children: list):
        elem = self._get_element_from_name(module_name)
        self._add_relationships(elem, parents, children)

    def update_module_coords(self,
                             module_name: str,
                             coords: list = None,
                             save_changes: bool = False):
        elem = self._get_element_from_name(module_name)
        self._add_coords(elem, coords)
        self._parse_XML()
        if save_changes:
            self.write_to_XML()

    def _add_coords(self,
                    elem: ET.Element,
                    coords: list = None):
        if coords == None:
            return elem
        coords_elem = elem.find("./coordinates")
        if coords_elem is None:
            coords_elem = ET.SubElement(elem, "coordinates")
        coords_elem.text = str("\n{0}".format(coords))
        return elem

    def update_plugin_options(self,
                              xml_parent_name: Union[ET.Element,str],
                              options: dict,
                              save_changes: bool = False):
        """Update the options of a plugin
        :param plugin_name: str of plugin name
        :param options: dict of options to be updated
        """
        xml_parent: ET.Element
        if isinstance(xml_parent_name, str):
            xml_parent = self._get_element_from_name(xml_parent_name)
        else:
            xml_parent = xml_parent_name
        plugin_elem: ET.Element = xml_parent.find("./plugin")
        self._add_options(plugin_elem, options)
        self._parse_XML()
        if save_changes:
            self.write_to_XML()

    def _add_options(self,
                            plugin_elem: ET.Element,
                            options
                            ):
        opt_elem = plugin_elem.find("./options")
        if opt_elem is None:
            opt_elem = ET.SubElement(plugin_elem, "options")
        for key in options.keys():
            if isinstance(options[key], list):
                new_option = ET.SubElement(opt_elem, key)
                option_text = ("\n{}".format(
                    "\n".join([*options[key]])))
                new_option.text = option_text
            elif isinstance(options[key], (int, float, str)):
                new_option = opt_elem.find(str("./" + key))
                if new_option is None:
                    new_option = ET.SubElement(opt_elem, key)
                text_lead = "\n" if "\n" not in str(options[key]) else ""
                new_option.text = "{0} {1}".format(
                    text_lead, str(options[key]))
            elif isinstance(options[key], (dict)):
                self._add_options(opt_elem, options[key])

    def append_input_data(self,
                          data_name: str,
                          data_dir: str,
                          xml_parent: Union[ET.Element, str] = "Initialiser",
                          save_dir_as_relative: bool = True):
        """Appened path to input datafile. Replaces windows backslash

        :param plugin_type: plugin to be loaded into module
        :type plugin_type: str
        :param plugin_options: plugin options as key-value pairs
        :type plugin_options: dict
        :param xml_parent: Name of parent or pass element directly
        :type xml_parent: str, ET.Element
        :param save_dir_as_relative: Replace root path in filename with "./"
        :type save_dir_as_relative: bool, optional
        :return: None
        """
        if isinstance(xml_parent, str):
            xml_parent = self._get_element_from_name(xml_parent)

        input_data_elem = xml_parent.find("./inputdata")

        if input_data_elem is None:
            input_data_elem = ET.SubElement(xml_parent, "inputdata")

        data_name_elem = input_data_elem.find("./"+data_name)
        if data_name_elem is not None:
            input_data_elem.remove(data_name_elem)

        plugin_elem = ET.SubElement(input_data_elem, data_name)
        if save_dir_as_relative:
            data_dir = data_dir.replace(self.lib_base_path, "./")
        data_dir = data_dir.replace("\\", "/")
        if path.exists(path.dirname(rel_to_abs(data_dir))):
            plugin_elem.set('file', data_dir)
        else:
            plugin_elem.set('module', data_dir)

    def append_method_to_plugin(self,
                                method_type: str,
                                method_options: dict,
                                xml_parent: Union[ET.Element, str],
                                overwrite_existing: Union[bool, int] = False
                                ):
        """Appened method as subelement to existing plugin element
        
        :param method_type: string type of method to be loaded into plugin
        :param method_options: dict where keys & values are options & values
        :param xml_parent: dict OR str. 
                            If string given, parent elem is found via search,
                            Otherwise, method appeneded directly
        """
        if isinstance(xml_parent, str):
            xml_parent = self._get_element_from_name(xml_parent)

        method_elem = xml_parent.find("./method")

        if method_elem is not None and overwrite_existing:
            if method_elem.attrib['type'] == method_type:
                xml_parent.remove(method_elem)
            method_elem = None

        if method_elem is None:
            method_elem = ET.SubElement(xml_parent, "method")
            method_elem.set('type', method_type)
        self._add_options(method_elem, method_options)

    def append_plugin_to_module(self,
                                plugin_type: str,
                                plugin_options: dict,
                                method_list: list,
                                plugin_data: str,
                                xml_parent: Union[ET.Element, str],
                                overwrite_existing: Union[bool, int] = False
                                ):
        """Appened plugin as subelement to existing module element
        
        :param plugin_type: string type of plugin to be loaded into module
        :param plugin_options: dict where keys & values are options & values
        :param plugin_data: string type of data to be used as input
        :param xml_parent: dict OR str. 
                            If string given, parent elem is found via search,
                            Otherwise, plugin appeneded directly
        """
        if isinstance(xml_parent, str):
            xml_parent = self._get_element_from_name(xml_parent)

        plugin_elem = xml_parent.find("./plugin")

        if plugin_elem is not None and overwrite_existing:
            xml_parent.remove(plugin_elem)
            plugin_elem = None

        if plugin_elem is None:
            plugin_elem = ET.SubElement(xml_parent, "plugin")
            plugin_elem.set('type', plugin_type)
        if plugin_data is not None and len(plugin_data) > 0:
            self.append_input_data('X', plugin_data, xml_parent, False)
        if '__init__' in plugin_options.keys():
            self._add_options(plugin_elem, plugin_options['__init__'])
        for f in method_list:
            self.append_method_to_plugin(f,
                                        plugin_options[f], 
                                        plugin_elem, 
                                        overwrite_existing)

    def append_pipeline_module(self,
                               module_type: str,
                               module_name: str,
                               plugin_type: str,
                               plugin_options: Dict[str, Any],
                               parents: list,
                               children: list,
                               xml_parent_element_name: str,
                               coords: list = None
                               ) -> None:
        """Append new pipeline module to existing XML elementTree to be written later
        :param module_type: string declare type of module (UserFeedback,data_processing etc)
        :param module_name: string give module a user-defined name
        :param plugin_type: string type of plugin to be loaded into module
        :param plugin_options: dict where keys & values are options & values
        :param parents: list of parent names for this module (can be empty)
        :param children: list of child names for this module (can be empty)
        :param xml_parent_element_name: str containing name of parent Element for new module
        :param coords [optional]: list of coordinates for UserFeedback canvas
        """
        xml_parent_element: ET.Element = self._get_element_from_name(
            xml_parent_element_name)

        new_mod = ET.Element(module_type.replace(" ", ""))
        new_mod.set('name', module_name)

        if plugin_type != None:
            self.append_plugin_to_module(plugin_type,
                                         plugin_options,
                                         [],
                                         parents[0],
                                         new_mod,
                                         0
                                         )

        if xml_parent_element.tag == "loop":
            parents.append(xml_parent_element.attrib["name"])
        new_mod = self._add_relationships(new_mod, parents, children)
        new_mod = self._add_coords(new_mod, coords)

        self._loop_rels_autofill(xml_parent_element, module_name)
        xml_parent_element.append(new_mod)

    def append_pipeline_loop(self,
                             loop_type: str,
                             condition: str,
                             loop_name: str,
                             parents: list,
                             children: list,
                             xml_parent_element_name: str = None,
                             coords: list = None
                             ) -> None:
        """Append new pipeline module to existing XML file
        :param loop_type: string declare type of loop (for/while/manual etc)
        :param loop_name: string give loop a user-defined name
        :param plugin_type: string type of plugin to be loaded into module
        :param parents: list of parent names for this module (can be empty)
        :param children: list of child names for this module (can be empty)
        :param xml_parent_element_name: str containing name of parent Element for new module
        :param coords [optional]: list of coordinates for UserFeedback canvas
        """
        xml_parent_element: ET.Element = self._get_element_from_name(
            xml_parent_element_name)

        new_loop = ET.Element("loop")
        new_loop.set('type', loop_type)
        new_loop.set('condition', condition)
        new_loop.set('name', loop_name)

        if xml_parent_element.tag == "loop":
            parents.append(xml_parent_element.attrib["name"])
        new_loop = self._add_relationships(new_loop, parents, children)
        new_loop = self._add_coords(new_loop, coords)

        self._loop_rels_autofill(xml_parent_element, loop_name)

        xml_parent_element.append(new_loop)

    def _get_data_structure(self, modules, module) -> Dict[str, Any]:
        try:
            data_struct = self._find_dict_with_key_val_pair(
                modules[module],
                "class", "data")
        except Exception as exc:
            data_struct = self._find_dict_with_key_val_pair(
                modules,
                "class", "data")

        assert len(data_struct) < 2, \
            "Multiple data with same ID, please check XML"

        out: Dict[str, Any]
        if len(data_struct) == 1:
            out = data_struct[0]
        else:
            out = {"to_load": {}}
        return out

    #@property
    def data_to_load(self, modules=False, module='Initialiser') -> Dict[str, str]:
        if not modules:
            modules = self.loaded_modules
        return self._get_data_structure(modules, module)["to_load"]


# Use case examples:
if __name__ == "__main__":
    s = XML_handler()
    s.load_XML("./examples/xml_files/regerssion_test.xml")
    s.update_plugin_options("Modelling-1",{"alpha":4})
    s._print_xml_config()
    a = s.data_to_load
    print(1)

    # s.write_to_XML()
    # s.append_pipeline_loop("for",
    #                       "10",
    #                       "my_loop_3",
    #                       ["Init"],
    #                       [])
    # s.append_pipeline_module("UserFeedback thing",
    #                       "added_mod",
    #                       "startpage",
    #                       {"class_list":["test_1","test_2"],"class_list_2":["test_1","test_2"]},
    #                       ["loop0"],
    #                       ["Output","loop0"],
    #                       "loop0",
    #                       [2,3,4,5])
    # s.write_to_XML()