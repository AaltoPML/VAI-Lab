import ast
import os     
class PluginSpecs(ast.NodeVisitor):
    def __init__(self) -> None:
        self.module_dirs = {}
        self.available_plugins = {}
        self.get_plugin_files()
        self.get_plugin_specs()

    def get_plugin_files(self, root_dir=None):
        if root_dir is None:
            root_dir = os.path.dirname(os.path.realpath(__file__+"/.."))

        for mod_folder in self.get_clean_module_dirs(root_dir):
            mod_path = os.path.join(root_dir,mod_folder,"plugins")
            plugins = self.get_clean_module_dirs(mod_path)

            self.module_dirs[mod_folder] = {}
            self.module_dirs[mod_folder]["root"] = mod_path
            self.module_dirs[mod_folder]["files"] = [f for f in plugins if f.endswith(".py")]

    def get_clean_module_dirs(self, root_dir:str=None) -> list:
        excludes = ["__init__.py","__pycache__","resources"]
        if os.path.exists(root_dir):
            mod_dirs = os.listdir(root_dir)
            for ex in excludes:
                if ex in mod_dirs:
                    mod_dirs.remove(ex)
            return mod_dirs
        else:
            return []

    def plugins_generator(self):
        plugin_names = self.module_dirs[self.curr_module]["files"]
        for plugin in plugin_names:
            self.curr_plugin = plugin
            yield os.path.join(self.module_dirs[self.curr_module]["root"],plugin)

    def modules_generator(self):
        for self.curr_module in self.module_dirs.keys():
            self.available_plugins[self.curr_module] = {}
            plugins = self.plugins_generator()
            for plugin_dir in plugins:
                yield plugin_dir

    def get_module_package(self):
        if __package__:
            parent_package = __package__.split(".")[0]
        else:
            parent_package = "aidesign"
        scipt_filename = self.curr_plugin.replace(".py","")
        return "{0}.{1}.plugins.{2}".format(parent_package,self.curr_module,scipt_filename)

    def get_plugin_specs(self):
        self.modules = self.modules_generator()
        for plugin_dir in self.modules:
            self.available_plugins[self.curr_module]\
                                    [self.curr_plugin] \
                                    = {"_PLUGIN_DIR":plugin_dir,
                                       "_PLUGIN_PACKAGE":self.get_module_package()
                                    }
            with open(plugin_dir, "r") as source:
                tree = ast.parse(source.read())
            self.visit(tree)

    def visit_Assign(self, node):
        if type(node.targets[0]) == ast.Name:
            if "_PLUGIN" in node.targets[0].id:
                key = node.targets[0].id
                val = eval(compile(ast.Expression(node.value),"<ast expression>","eval"))
                self.available_plugins[self.curr_module][self.curr_plugin][key] = val

    def get_option_specs(self, option:str) -> dict:
        output = {}
        for module in self.available_plugins.keys():
            output[module] = {}
            for plugin in self.available_plugins[module].keys():
                if option in self.available_plugins[module][plugin]:
                    output[module][plugin] = self.available_plugins\
                                                        [module]\
                                                        [plugin]\
                                                        [option]
        return output

    def find_plugin_by_tag_and_value(self, tag:str, name:str) -> dict:
        for module in self.available_plugins.keys():
            for plugin in self.available_plugins[module].keys():
                if tag in self.available_plugins[module][plugin]:
                    if name in self.available_plugins[module][plugin][tag]:
                        return self.available_plugins\
                                                [module]\
                                                [plugin]
        return None

    def names(self):
        return self.get_option_specs("_PLUGIN_READABLE_NAMES")

    def get_all_available_plugin_names(self):
        names = self.names()
        output = []
        for n in names.keys():
            for plugin in names[n]:
                output.append(plugin)
        return output

    def find_from_class_name(self, value):
        return self.find_plugin_by_tag_and_value("_PLUGIN_CLASS_NAME",value)

    def find_from_readable_name(self, value):
        return self.find_plugin_by_tag_and_value("_PLUGIN_READABLE_NAMES",value)

    def class_names(self):
        return self.get_option_specs("_PLUGIN_CLASS_NAME")
    
    def class_descriptions(self):
        return self.get_option_specs("_PLUGIN_CLASS_DESCRIPTION")
    
    def required_settings(self):
        return self.get_option_specs("_PLUGIN_REQUIRED_SETTINGS")

    def print(self, value):
        from pprint import PrettyPrinter
        pp = PrettyPrinter(sort_dicts=False, width=100)
        pp.pprint(value)


# if __name__ == "__main__":
#     ps = PluginSpecs()
#     ps.print(ps.get_all_available_plugin_names())
        # ps.print(ps.names())
#     ps.print(ps.class_descriptions())
    # print(list(ps.class_descriptions()['GUI'].values()))