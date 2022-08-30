from aidesign._plugin_template import PluginTemplate
from aidesign._types import DataInterface
from abc import ABC, abstractmethod


class ModellingPluginTemplate(PluginTemplate,ABC):
    def __init__(self, plugin_globals: dict) -> None:
        """Instantiates data containers and parses plugin-specific options

        param: plugin_globals:dict dictionary representing the global symbol table of the plugin script
        """
        super().__init__(plugin_globals)

    def configure(self, config: dict):
        """Implemented by parent: aidesign.utils.common_plugin_template.PluginTemplate"""
        super().configure(config)

    def set_data_in(self, data_in: DataInterface):
        """Implemented by parent: aidesign.utils.common_plugin_template.PluginTemplate"""
        super().set_data_in(data_in)

    @abstractmethod
    def solve(self):
        pass

    @abstractmethod
    def predict(self):
        pass

    @abstractmethod
    def score(self):
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
