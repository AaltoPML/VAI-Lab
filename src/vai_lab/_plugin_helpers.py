from typing import List, Iterator, Union
from vai_lab._types import DictT

import ast
import os


class PluginSpecs(ast.NodeVisitor):
    def __init__(self) -> None:
        self.module_dirs: DictT = {}
        self.available_plugins: DictT = {}
        self._get_plugin_files()
        self._get_plugin_specs()

    def _get_plugin_files(self, root_dir: str = None) -> None:
        if root_dir is None:
            root_dir = os.path.dirname(os.path.realpath(__file__))

        for mod_folder in self._get_clean_module_dirs(root_dir):
            mod_path = os.path.join(root_dir, mod_folder, "plugins")
            plugins = self._get_clean_module_dirs(mod_path)

            self.module_dirs[mod_folder] = {}
            self.module_dirs[mod_folder]["root"] = mod_path
            self.module_dirs[mod_folder]["files"] = [
                f for f in plugins if f.endswith(".py")]

    def _get_clean_module_dirs(self, root_dir: str) -> List[str]:
        excludes = ["__init__.py", "__pycache__", "resources"]
        if os.path.exists(root_dir):
            mod_dirs = os.listdir(root_dir)
            for ex in excludes:
                if ex in mod_dirs:
                    mod_dirs.remove(ex)
            return mod_dirs
        else:
            return []

    def _plugins_generator(self) -> Iterator:
        plugin_names = self.module_dirs[self.curr_module]["files"]
        for plugin in plugin_names:
            self.curr_plugin = plugin
            yield os.path.join(self.module_dirs[self.curr_module]["root"], plugin)

    def _modules_generator(self):
        for self.curr_module in self.module_dirs.keys():
            self.available_plugins[self.curr_module] = {}
            plugins = self._plugins_generator()
            for plugin_dir in plugins:
                yield plugin_dir

    def _get_module_package(self):
        if __package__:
            parent_package = __package__.split(".")[0]
        else:
            parent_package = "aidesign"
        scipt_filename = self.curr_plugin.replace(".py", "")
        return "{0}.{1}.plugins.{2}".format(parent_package, self.curr_module, scipt_filename)

    def _get_plugin_specs(self):
        self.modules = self._modules_generator()
        for plugin_dir in self.modules:
            self.available_plugins[self.curr_module][self.curr_plugin] \
                = {"_PLUGIN_DIR": plugin_dir,
                   "_PLUGIN_PACKAGE": self._get_module_package()
                   }
            with open(plugin_dir, "r") as source:
                tree = ast.parse(source.read())
            self.visit(tree)

    def visit_ClassDef(self, node):
        """Append the name of the main class of the plugin to specs
        Called as a callback from "self.visit(tree)"
        Adds only the first class name - works for now, but may be suboptimal

        :param node: ast node of class name
        """
        c_tag = "_PLUGIN_CLASS_NAME"
        d_tag = "_PLUGIN_CLASS_DESCRIPTION"
        if c_tag not in self.available_plugins[self.curr_module][self.curr_plugin].keys():
            self.available_plugins[self.curr_module][self.curr_plugin][c_tag] = node.name
            ds = ast.get_docstring(node)
            self.available_plugins[self.curr_module][self.curr_plugin][d_tag] = ds

    def visit_Assign(self, node):
        """Append the name of all plugin specs to available_plugins dict
        Plugin specs should be declared with consants beginning with "_PLUGIN_<option_name>"
        Called as a callback from "self.visit(tree)"

        :param node: ast node of class name
        """
        if type(node.targets[0]) == ast.Name:
            if "_PLUGIN" in node.targets[0].id:
                key = node.targets[0].id
                val = eval(compile(ast.Expression(node.value),
                           "<ast expression>", "eval"))
                self.available_plugins[self.curr_module][self.curr_plugin][key] = val

    def _get_option_specs(self, option: str) -> dict:
        """Gets either required OR optional settings for each plugin.

        :param option: str containing either:
                        "_PLUGIN_OPTIONAL_SETTINGS"
                        OR
                        "_PLUGIN_REQUIRED_SETTINGS"

        :returns output: nested dict of options by [Module][Plugin Class Name]
        """
        output : DictT= {}
        for module in self.available_plugins.keys():
            output[module] = {}
            for plugin in self.available_plugins[module].keys():
                if option in self.available_plugins[module][plugin]:
                    cn = self.available_plugins[module][plugin]["_PLUGIN_CLASS_NAME"]
                    output[module][cn] = self.available_plugins[module][plugin][option]
        return output

    def _find_plugin_by_tag_and_value(self, tag: str, name: str) -> Union[DictT,None]:
        for module in self.available_plugins.keys():
            for plugin in self.available_plugins[module].keys():
                if tag in self.available_plugins[module][plugin]:
                    if name in self.available_plugins[module][plugin][tag]:
                        return self.available_plugins[module][plugin]
        return None

    @property
    def names(self):
        return self._get_option_specs("_PLUGIN_READABLE_NAMES")

    @property
    def class_names(self):
        return self._get_option_specs("_PLUGIN_CLASS_NAME")

    @property
    def module_options(self):
        return self._get_option_specs("_PLUGIN_MODULE_OPTIONS")

    @property
    def required_settings(self):
        return self._get_option_specs("_PLUGIN_REQUIRED_SETTINGS")

    @property
    def class_descriptions(self):
        return self._get_option_specs("_PLUGIN_CLASS_DESCRIPTION")

    @property
    def optional_settings(self):
        return self._get_option_specs("_PLUGIN_OPTIONAL_SETTINGS")

    @property
    def available_plugin_names(self):
        names = self.names
        output = []
        for n in names.keys():
            for plugin in names[n]:
                for variant in names[n][plugin].keys():
                    if names[n][plugin][variant] == "default":
                        output.append(variant)
        return output

    def find_from_class_name(self, value):
        return self._find_plugin_by_tag_and_value("_PLUGIN_CLASS_NAME", value)

    def find_from_readable_name(self, value):
        return self._find_plugin_by_tag_and_value("_PLUGIN_READABLE_NAMES", value)

    def print(self, value):
        from pprint import PrettyPrinter
        pp = PrettyPrinter(sort_dicts=False, width=100)
        pp.pprint(value)


if __name__ == "__main__":
    ps = PluginSpecs()
    ps.print(ps.available_plugin_names)
    # ps.print(ps.names)
    # ps.print(ps.class_descriptions)
    # print(list(ps.class_descriptions()['GUI'].values()))
