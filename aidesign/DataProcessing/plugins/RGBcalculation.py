from PIL import Image
import numpy as np
import os
from aidesign._plugin_templates import DataProcessingT
from aidesign._types import DataInterface
import pandas as pd
from sklearn.base import BaseEstimator
from aidesign._import_helper import get_lib_parent_dir
from sklearn.metrics import mean_squared_error as mse

_PLUGIN_READABLE_NAMES = {"RGBcalculation":"default"}  # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "Custom"}            # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"Data": "str"}            # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                         # type:ignore
_PLUGIN_REQUIRED_DATA = {}                             # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X","Y","X_tst", 'Y_tst'}     # type:ignore

class RGBcalculation(DataProcessingT):
    
    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.proc = model()

    def configure(self, config: dict):
        """Sets and parses plugin configurations options
        :param config: dict of internal tags set in the XML config file 
        """
        super().configure(config)

    def set_data_in(self, data_in):
        """Sets and parses incoming data
        :param data_in: saves data as class variable
                        expected type: aidesign.Data.Data_core.Data
        """
        super().set_data_in(data_in)

    def fit(self):
        cleaned_options = self._clean_solver_options()
        self.proc.set_params(**cleaned_options)
        self.proc.fit(self.X)


    def transform(self, data: DataInterface) -> DataInterface:
        data.append_data_column("X", pd.DataFrame(self.proc.transform(data)))
        # if self.X_tst is not None:
        #     data.append_data_column("X_test", pd.DataFrame(self.proc.transform(self.X_tst)))
        print(data)
        return data

class model(BaseEstimator):
    def __init__(self, optional=False):
        self.optional = optional
    
    def fit(self, X):
        X = X

    def transform(self, X):
        # [h, w] = np.shape(X)[0:2]#calculating height and width for each image
        arr_mean = np.mean(X, axis=(0,1))
        print(f'[R={arr_mean[0]:.1f},  G={arr_mean[1]:.1f}, B={arr_mean[2]:.1f}]')
        return np.mean(arr_mean)