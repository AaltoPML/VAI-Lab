from aidesign._plugin_templates import EnvironmentPluginT
from typing import Dict
import pybullet as p

_PLUGIN_READABLE_NAMES = {"PyBullet":"default"}                                                 # type:ignore
_PLUGIN_MODULE_OPTIONS = {}                                                                     # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"model_dir": "str", "headless": "bool"}                            # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"neg_label": "int", "pos_label": "int","timestep":"float"}         # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                                                      # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X","Y","X_tst", 'Y_tst'}                                              # type:ignore

class PyBullet(EnvironmentPluginT):
    """
    Load and control the PyBullet Environment
    """
    def __init__(self) -> None:
        super().__init__(globals())
        self.model_ids:Dict = {}
        
    def connect(self):
        physicsClient = p.connect(p.GUI)# p.DIRECT for non-graphical version

    def disconnect(self):
        return p.disconnect()

    def reset(self):
        return p.resetSimulation()

    def load_model(self,model_path) -> None:
        self.model_ids[model_path] = p.loadURDF(model_path)

    def step(self, action):
        return p.step(action)

        