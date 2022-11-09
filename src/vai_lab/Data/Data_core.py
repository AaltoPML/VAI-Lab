"""Adds aidesign root folder to pythonpath assuming this script is 2 levels down.
Hacky patch For testing only, normally you'd have aidesign in your
OS's PYTHONPATH"""
from os import path

if not __package__:
    import sys
    root_mod = path.dirname(path.dirname(path.dirname(__file__)))
    sys.path.append(root_mod)

from typing import Dict, KeysView, TypeVar

from vai_lab._import_helper import get_lib_parent_dir
from vai_lab.Data.xml_handler import XML_handler
from vai_lab._import_helper import rel_to_abs

import pandas as pd # type: ignore
import numpy as np

DataT = TypeVar("DataT",bound="Data")
class Data:
    
    def __init__(self: DataT) -> None:
        self._lib_base_path = get_lib_parent_dir()
        self._xml_parser = XML_handler()
        self.data: Dict[str, pd.core.frame.DataFrame] = {}

    def _import_csv(self: DataT,
                    filename: str,
                    data_name: str,
                    strip_whitespace: bool = True) -> None:
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
            self.data[data_name].columns = [c.strip()
                                            for c in self.data[data_name].columns]

    def _import_png(self: DataT,
                    filename: str,
                    data_name: str) -> None:
        """Loads png into PIL.Image class. Adds instance to self.data
        The image is stored as a function (not a matrix - can be added if needed)
        :param filename: str, filename of csv file to be loaded
        :param data_name: str, name of dict key in which data will be stored
        """
        import cv2 # type: ignore
        key = filename.split(path.sep)[-1].split(".")[0]
        self.data[data_name][key] = cv2.imread(filename)

    def _import_dir(self: DataT,
                    folder_dir: str,
                    data_name: str) -> None:
        """Explores folder, and imports all data items recursively
        
        :param folder_dir: str, directory to be explored
        :param data_name: str, name of dict key in which data will be stored
                data_name is "data" overwritten by folder name due to recursion
                This will probably change for user-defined names
        """
        from glob import glob
        if folder_dir[-1] != path.sep:
            folder_dir += path.sep
        # data_name = folder_dir.split(path.sep)[-2]
        files = np.sort(glob(folder_dir + "*"))
        self.data[data_name] = {}
        for f in files:
            self.import_data(f, data_name)

    def _get_ext(self: DataT, path_dir: str) -> str:
        """Extracts extension from path_dir, or check if is dir
        :param path_dir: str, path_dir to be checked
        :returns ext: str, path_dir extension or "dir" if path_dir is directory
        """
        if path.isdir(path_dir):
            return "dir"
        else:
            return path_dir.split(".")[-1]

    def import_data(self: DataT,
                    filename: str,
                    data_name: str = "data") -> None:
        """Import file directly into DataFrame
        Translates relative files to absolute before parsing - not ideal
        Filename to parsing method based on extension name.
        :param filename: str, filename of file to be loaded
        :param data_name: str, name of class variable data will be loaded to
        """
        filename = rel_to_abs(filename).replace(
            "\\", "/").replace("/", path.sep)
        ext = self._get_ext(filename)
        getattr(self, "_import_{0}".format(ext))(filename, data_name)

    def import_data_from_config(self: DataT, config: dict) -> None:
        for c in config.keys():
            self.import_data(config[c], c)

    def append_data_column(self: DataT, col_name: str, data=None) -> None:
        self.data[col_name] = data

    def _parse_data_options(self: DataT) -> None:
        for s in self.loaded_options["data_fields"]:
            self.append_data_column(s)

    def load_data_settings(self: DataT, filename: str) -> None:
        self._xml_parser.load_XML(filename)
        self.loaded_options = self._xml_parser._get_init_data_structure()
        self._parse_data_options()

    def keys(self: DataT) -> KeysView:
        return self.data.keys()

    def __getitem__(self: DataT, key: str) -> pd.core.frame.DataFrame:
        return self.data[key]

    def copy(self: DataT) -> DataT:
        from copy import deepcopy
        return deepcopy(self)

if __name__ == "__main__":
    d = Data()
    # d.load_data_settings("./examples/data_passing_test.xml")
    d.import_data("./examples/crystalDesign")
    print(d["crystalDesign"])
    # print(d["data"]["input"].loc[0:3])
    # dc = d.copy()
    # d["data"]["input"].loc[0:3] = 9
    # print(d["data"]["input"].loc[0:3])
    # print(dc["data"]["input"].loc[0:3])
    # dc.keys()
    # print(dc["input"])
    # d.data_names