from PIL import Image
import numpy as np
import os
from aidesign._plugin_templates import DataProcessingT
from aidesign._types import DataInterface
import pandas as pd
from sklearn.base import BaseEstimator
from aidesign._import_helper import get_lib_parent_dir
from sklearn.metrics import mean_squared_error as mse
import cv2
import matplotlib.pyplot as plt

_PLUGIN_READABLE_NAMES = {"imgtofeatvect":"default",
                          "ImgToFeatVect": "alias", "ImageToFeatureVector": "alias"}        # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "other"}                                                  # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"Data": "str"}                                                 # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                                                              # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                                                  # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X","Y","X_tst",'Y_tst'}                                           # type:ignore

class ImgToFeatVect(DataProcessingT):
    
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
        data.append_data_column("X", pd.DataFrame(self.proc.transform(self.X)))
        if self.X_tst is not None:
            data.append_data_column("X_test", pd.DataFrame(
                self.proc.transform(self.X_tst)))
        return data

class model(BaseEstimator):
    def __init__(self, optional=False):
        self.optional = optional
    
    def fit(self, X):
        """Defines the number of samples in the design, their placement
        and their size.
        
        Parameters
        ----------
        X : {dict}
            A dictionary containing images in each entry.
        Returns
        -------
        self : object
            Fitted model.
        """
        self.n = len(X.keys())
        h,w,self.rgb = next(iter(X.values())).shape
        self.d = h*w
        return self
    
    def transform(self, X):
        X_mat = np.dstack([X[el].reshape(self.d,self.rgb) for el in X.keys()])
        X_mat = X_mat.reshape(self.n,self.d,self.rgb)
        return pd.DataFrame(X_mat)