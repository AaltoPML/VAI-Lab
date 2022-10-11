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

_PLUGIN_READABLE_NAMES = {"RectangleDetection":"default",
                          "RectDet": "alias", "rectangledetection": "alias"}        # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "Custom"}                                         # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"Data": "str"}                                         # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"r": "int", "c": "int", "h":"float", "w": "float"}     # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                                          # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X","Y","X_tst",'Y_tst'}                                   # type:ignore

class RectangleDetection(DataProcessingT):
    
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
        """
        TODO: Temporary solution until input data module is cofigured."""
        
        dst_img = os.path.join(
            get_lib_parent_dir(),
            'examples',
            'crystalDesign')
        #iterating over dst_image to get the images as arrays
        # for image in sorted(os.listdir(dst_img)):
        arr = np.array(Image.open(os.path.join(dst_img, '00007.png')))
        self.proc.fit(arr)
        """"""
        # self.proc.fit(self.X)

    def transform(self, data: DataInterface) -> DataInterface:
        """
        TODO: Temporary solution until input data module is cofigured."""
        dst_img = os.path.join(
            get_lib_parent_dir(),
            'examples',
            'crystalDesign')
        arr = np.array(Image.open(os.path.join(dst_img, '00007.png')))
        self.proc.transform(arr)
        """"""
        # data.append_data_column("X", pd.DataFrame(self.proc.transform(data)))
        return data

class model(BaseEstimator):
    def __init__(self, optional=False):
        self.optional = optional
    
    def fit(self, X, r=7, c=4, h=35, w=79, hs=34, vs=23, buffer=5):
        """Defines the number of samples in the design, their placement
        and their size.
        
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The image data with the samples with RGB information.
            Samples are expected to be marked with a red rectangle.
        r : int
            Number of rows with samples.
        c : int
            Number of columns with samples.
        h : float
            Sample height.
        w : int
            Sample width.
        hs : float
            Horizontal spacing.
        vs : int
            Vertical spacing.
        buffer : int
            Pixel buffer. Inidcates the margin for the inner rectangle.
        Returns
        -------
        self : object
            Fitted model.
        """
        self.r = r
        self.c = c
        self.h = h
        self.w = w
        self.hs = hs
        self.vs = vs
        self.buffer = buffer
        mask = (X[:,:,0] > 120) * (X[:,:,1] < 80) * (X[:,:,2] < 80)
        self.ii_ini, self.jj_ini = np.unravel_index(mask.argmax(), mask.shape)
        # return self

    def transform(self, X):
        # [h, w] = np.shape(X)[0:2]#calculating height and width for each image
        X_dict = {}
        fig, axs = plt.subplots(self.r, self.c)
        for i in np.arange(self.r):
            for j in np.arange(self.c):
                X_dict[i,j] = X[self.ii_ini+self.h*i+self.vs*i+self.buffer*(1+i):self.ii_ini+self.h*(i+1)+self.vs*i-self.buffer*(1-i), 
                                self.jj_ini+self.w*j+self.hs*j+self.buffer*(1+j):self.jj_ini+self.w*(j+1)+self.hs*j-self.buffer*(1-j),:]
                axs[i, j].imshow(X_dict[i,j])
        return X_dict