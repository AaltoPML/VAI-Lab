import sys

def import_plugin(script_config, plugin_name):
    plugin_list = __import__(script_config["__package__"]+'.plugins.' + plugin_name,
                             script_config,
                             {},
                             [plugin_name])
    plugin_class = getattr(plugin_list, plugin_name)
    return plugin_class


def import_module(script_config, module_name):
    module_list = __import__('aidesign.' + module_name + "." + module_name + "_core",
                             script_config,
                             {},
                             [module_name])
    module_class = getattr(module_list, module_name)
    return module_class

def get_plugin_names():
    #get current list of sys.modules
    # cycle list of plugins
    # remove all new plugins from sys.modules
