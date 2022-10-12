from aidesign._plugin_templates import EnvironmentPluginT
from typing import Dict
from pybullet import *

_PLUGIN_READABLE_NAMES = {"PyBullet":"default"}                                                 # type:ignore
_PLUGIN_MODULE_OPTIONS = {}                                                                     # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"model_dir": "str", "headless": "bool"}                            # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                                                                  # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                                                      # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X","Y","X_tst", 'Y_tst'}                                              # type:ignore

class PyBulletEnv(EnvironmentPluginT):
    """
    Loads the pybullet library as wildcard and exposes all functions
    """
    def __init__(self) -> None:
        super().__init__(globals())
        self.connection_mode = GUI
        self.model_ids:Dict = {}
        
    def set_gui(self,use_gui:bool=True):
        if use_gui:
            self.connection_mode = GUI # Use pybullet GUI
        else:
            self.connection_mode = DIRECT # Use pybullet without GUI

    def connect(self):
        self.physicsClient = connect(self.connection_mode)

    def disconnect(self):
        return disconnect()

    def reset(self):
        return resetSimulation()

    def load_model(self) -> None:
        model_path = self._config["options"]["model_dir"]
        self.model_ids[model_path] = loadURDF(model_path)

if __name__ == "__main__":
    pb = PyBulletEnv()
    pb.set_gui(True)
    pb.connect()
