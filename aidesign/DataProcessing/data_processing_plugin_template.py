from aidesign._plugin_template import PluginTemplate
from aidesign._types import DataInterface

from abc import ABC, abstractmethod


class DataProcessingPluginTemplate(PluginTemplate, ABC):
    def __init__(self, plugin_globals: dict) -> None:
        """Instantiates data containers and parses plugin-specific options

        param: plugin_globals:dict dictionary representing the global symbol table of the plugin script
        """
        super().__init__(plugin_globals)
        self._options_to_ignore = ["Data"]

    def configure(self, config: dict):
        """Implemented by parent: aidesign.utils.common_plugin_template.PluginTemplate"""
        super().configure(config)
        if type(self.X) is None and type(self.Y) is None:
            print('Invalid Data name. Indicate whether to use `X` or `Y`')

    def set_data_in(self, data_in: DataInterface):
        """Implemented by parent: aidesign.utils.common_plugin_template.PluginTemplate"""
        super().set_data_in(data_in)

    def _clean_solver_options(self):
        """XML tags that specify data to be processed should not be sent to solver
        TODO: in future, reverse the direction of this function - instead pull all options
                that are directly required by the solver
        """
        return {i[0]: i[1]
                for i in self._config["options"].items()
                if i[0] not in self._options_to_ignore}

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def transform(self, data: DataInterface) -> DataInterface:
        pass

    def _test(self, data):
        if self._PLUGIN_MODULE_OPTIONS['Type'] == 'classification':
            print('Training accuracy: %.2f%%' %
                  (self.score(self.X, self.Y)*100))
            if self.Y_tst is not None:
                print('Test accuracy: %.2f%%' %
                      (self.score(self.X_tst, self.Y_tst)*100))
            if self.X_tst is not None:
                data.append_data_column("Y_pred", self.predict(self.X_tst))
            return data
        elif self._PLUGIN_MODULE_OPTIONS['Type'] == 'regression':
            print('Training R2 score: %.3f' % (self.score(self.X, self.Y)))
            if self.Y_tst is not None:
                print('Training R2 score: %.3f' %
                      (self.score(self.X_tst, self.Y_tst)))
            if self.X_tst is not None:
                data.append_data_column("Y_pred", self.predict(self.X_tst))
            return data
        elif self._PLUGIN_MODULE_OPTIONS['Type'] == 'clustering':
            print('Clustering completed')
            if self.X_tst is not None:
                data.append_data_column("Y_pred", self.predict(self.X_tst))
            return data
