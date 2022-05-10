"""Adds aidesign root folder to pythonpath assuming this script is 2 levels down.
Hacky patch For testing only, normally you'd have aidesign in your
OS's PYTHONPATH"""
if not __package__:
    import sys 
    from os import path
    root_mod = path.dirname(path.dirname(path.dirname(__file__)))
    sys.path.append(root_mod)

from aidesign.utils.import_helper import import_module
from aidesign.Data.xml_handler import XML_handler
import pandas as pd
import numpy as np

class Data(object):
    def __init__(self) -> None:
        self.xml_parser = XML_handler()
        self.data = pd.DataFrame()

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
    d.load_data_settings("./resources/basic_operation.xml")
    print(d.data)