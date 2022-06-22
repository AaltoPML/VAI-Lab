from os import path

def import_plugin(script_config, plugin_name):
    plugin_list = __import__(script_config["__package__"]+'.plugins.' + plugin_name,
                             script_config,
                             {},
                             [plugin_name])
    plugin_class = getattr(plugin_list, plugin_name)
    return plugin_class

def import_plugin_absolute(script_config,plugin_package,plugin_name):
    plugin_list = __import__(plugin_package,
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

def get_lib_parent_dir():
    """Returns the absolute path of the library
    :param file: str of the builtin __file__ property of the calling script
    
    :returns: str of absolute path of the library root dir
    """
    return [__file__[:i] \
                for i,_ in enumerate(__file__)\
                if __file__[:i].\
                endswith("{0}aidesign{0}".format(path.sep))][-1]