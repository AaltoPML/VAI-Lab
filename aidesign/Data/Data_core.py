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
        self.data = pd.DataFrame()

    def import_csv(self, 
                    filename:str,
                    strip_whitespace:bool=True):
        """import data directly into DataFrame

        :param filename: str, filename of csv file to be loaded
        :param strip_whitespace: bool, remove spaces from before & after header names
        TODO: pandas has a lot of inbuilt read functions, including excel - implement
        """
        self.data = pd.read_csv(filename,
                            delimiter=',',
                            quotechar='|')
        if strip_whitespace:
            self.data.columns = [c.strip() for c in self.data.columns]

    def import_data(self, filename:str):
        """Import file directly into DataFrame

        Translates relative files to absolute before parsing - not ideal

        Filename to parsing method based on extension name.
        
        :param filename: str, filename of file to be loaded
        """
        if filename[0] == ".":
            filename = path.join(self.lib_base_path,filename)
        elif filename[0] == "/" or (filename[0].isalpha() and filename[0].isupper()):
            filename = filename
        ext = filename.split(".")[-1]
        getattr(self,"import_{0}".format(ext))(filename)

    def append_data_column(self, col_name:str, data=None):
        self.data[col_name] = data

    def _parse_data_options(self):
        for s in self.loaded_options["data_fields"]:
            self.append_data_column(s)

    def load_data_settings(self, filename:str):
        self.xml_parser.load_XML(filename)
        self.loaded_options = self.xml_parser.loaded_data_options
        self._parse_data_options()
        
if __name__ == "__main__":
    d = Data()
    # d.load_data_settings("./resources/basic_operation.xml")
    d.import_data("./Data/resources/import_test.csv")
    print(d.data)