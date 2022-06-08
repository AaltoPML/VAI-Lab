"""Adds aidesign root folder to pythonpath assuming this script is 2 levels down.
Hacky patch For testing only, normally you'd have aidesign in your
OS's PYTHONPATH"""
from os import path

if not __package__:
    import sys 
    root_mod = path.dirname(path.dirname(path.dirname(__file__)))
    sys.path.append(root_mod)

from aidesign.utils.import_helper import import_module
from aidesign.Data.xml_handler import XML_handler
import pandas as pd
import numpy as np


class Data(object):
    def __init__(self) -> None:
        self.lib_base_path = __file__.split("aidesign")[0] + "aidesign"
        self.xml_parser = XML_handler()
        self.data = {}

    def _import_csv(self, 
                    filename:str,
                    data_name:str,
                    strip_whitespace:bool=True):
        """import data directly into DataFrame

        :param filename: str, filename of csv file to be loaded
        :param data_name: str, name of dict key in which data will be stored
        :param strip_whitespace: bool, remove spaces from before & after header names
        TODO: pandas has a lot of inbuilt read functions, including excel - implement
        """
        self.data[data_name] = pd.read_csv(filename,
                            delimiter=',',
                            quotechar='|')
        if strip_whitespace:
            self.data[data_name].columns = [c.strip() for c in self.data[data_name].columns]

    def _import_png(self, 
                    filename:str,
                    data_name:str):
        """Loads png into PIL.Image class. Adds instance to self.data
        The image is stored as a function (not a matrix - can be added if needed)

        :param filename: str, filename of csv file to be loaded
        :param data_name: str, name of dict key in which data will be stored
        """
        from PIL import Image
        self.data[data_name][filename] = Image.open(filename)


    def _import_dir(self,
                        folder_dir:str,
                        data_name:str = "data"):
        from glob import glob
        files =np.sort(glob(folder_dir + "*"))
        self.data[data_name] = {}
        for f in files:
            self.import_data(f,data_name)

    def _rel_to_abs(self, filename: str):
        """Checks if path is relative or absolute
        If absolute, returns original path 
        If relative, converts path to absolute by appending to base directory
        """
        if filename[0] == ".":
            filename = path.join(self.lib_base_path,filename)
        elif filename[0] == "/" or (filename[0].isalpha() and filename[0].isupper()):
            filename = filename
        return filename

    def _get_ext(self, path_dir:str):
        """Extracts extension from path_dir, or check if is dir

        :param path_dir: str, path_dir to be checked

        :returns ext: str, path_dir extension or "dir" if path_dir is directory
        """
        if path.isdir(path_dir):
            return "dir"
        else:
            return path_dir.split(".")[-1]

    def import_data(self,
                        filename:str,
                        data_name:str = "data"):
        """Import file directly into DataFrame

        Translates relative files to absolute before parsing - not ideal

        Filename to parsing method based on extension name.
        
        :param filename: str, filename of file to be loaded
        :param data_name: str, name of class variable data will be loaded to
        """
        filename = self._rel_to_abs(filename)
        ext = self._get_ext(filename)
        getattr(self,"_import_{0}".format(ext))(filename,data_name)

    def import_data_from_config(self,config:dict):
        for c in config.keys():
            self.import_data(config[c],c)

    def append_data_column(self, col_name:str, data=None):
        self.data[col_name] = data

    def _parse_data_options(self):
        for s in self.loaded_options["data_fields"]:
            self.append_data_column(s)

    def load_data_settings(self, filename:str):
        self.xml_parser.load_XML(filename)
        self.loaded_options = self.xml_parser.init_data_structure
        self._parse_data_options()
        
    def keys(self):
        return self.data.keys()
    
    def __getitem__(self, key:str):
        return self.data[key]

if __name__ == "__main__":
    d = Data()
    # d.load_data_settings("./Data/resources/data_passing_test.xml")
    d.import_data("./Data/resources/import_test.csv")
    print(d.data_names)
    d.data_names