from sklearn.preprocessing import LabelEncoder as model
from aidesign.DataProcessing.data_processing_plugin_template import DataProcessingPluginTemplate
import pandas as pd

_PLUGIN_READABLE_NAMES = {"LabelEncoder":"default","LE":"alias"}
_PLUGIN_MODULE_OPTIONS = {"Type": "encoder"}
_PLUGIN_REQUIRED_SETTINGS = {"Data": "str"}
_PLUGIN_OPTIONAL_SETTINGS = {}
_PLUGIN_REQUIRED_DATA = {}
_PLUGIN_OPTIONAL_DATA = {"X","Y","X_tst", 'Y_tst'}

class LabelEncoder(DataProcessingPluginTemplate):
    """
    Encode target labels with value between 0 and n_classes-1
    """

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

    def transform(self,data):
        data.append_data_column("X", pd.DataFrame(self.proc.transform(self.X)))
        if self.X_tst is not None:
            data.append_data_column("X_test", pd.DataFrame(self.proc.transform(self.X_tst)))
        return data