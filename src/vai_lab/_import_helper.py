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
    module_list = __import__('vai_lab.' + module_name + "." + module_name + "_core",
                             script_config,
                             {},
                             [module_name])
    module_class = getattr(module_list, module_name)
    return module_class

def get_lib_parent_dir():
    """Returns the absolute path of the current library
    
    :returns: str of absolute path of the library root dir
    """
    return [__file__[:i] \
                for i,_ in enumerate(__file__)\
                if __file__[:i].\
                endswith("{0}vai_lab{0}".format(path.sep))][-1]

def rel_to_abs(filename: str) -> str:
        """Checks if path is relative or absolute
        If absolute, returns original path 
        If relative, converts path to absolute by appending to base directory
        """
        if filename[0] == ".":
            filename = path.normpath(path.join(get_lib_parent_dir(), filename))
        elif filename[0] == "/" or (filename[0].isalpha() and filename[0].isupper()):
            filename = filename
        return filename

def abs_to_rel(filename: str) -> str:
        """Checks if path is relative or absolute
        If absolute, converts path to relative if possible
        If relative, returns itself
        """
        if filename[0] == ".":
            #Relative path
            return filename
        elif filename[0].isalpha() and filename[0] != get_lib_parent_dir()[0]:
            #Different drive -> Absolute path
            return filename
        else:
            #Same drive not relative
            _folder = path.relpath(filename, get_lib_parent_dir())
            if _folder[:2] == '..':
                # Absolute path
                return filename
            else:
                # Relative path
                return path.join('.',_folder)
