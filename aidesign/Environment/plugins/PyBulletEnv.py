from aidesign._plugin_templates import EnvironmentPluginT
from aidesign._import_helper import rel_to_abs
from typing import Dict
from pybullet import *
from time import sleep


_PLUGIN_READABLE_NAMES = {"PyBullet":"default"}                                                 # type:ignore
_PLUGIN_MODULE_OPTIONS = {}                                                                     # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"model_dir": "str", "headless": "bool",
                                "timestep":"float", "max_steps":"int"}                          # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                                                                  # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                                                      # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X","Y","X_tst", 'Y_tst'}                                              # type:ignore

class PyBulletEnv(EnvironmentPluginT):
    """
    Loads the pybullet library as wildcard and exposes all functions
    """
    def __init__(self) -> None:
        super().__init__(globals())
        self.TIMESTEP: float
        self.MAX_STEPS: int
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

    def load_pb_data(self):
        import pybullet_data
        setAdditionalSearchPath(pybullet_data.getDataPath())

    def _load_model_by_type(self,model):
        model = rel_to_abs(model)
        ext = model.split(".")[-1]
        name = model.split("/")[-1].split(".")[0]
        if name == "plane":
                self.load_pb_data()
        if ext == "urdf":
            self.model_ids[name] = loadURDF(model)
        elif ext == "sdf":
            self.model_ids[name] = loadSDF(model,1,1.0)
        elif ext == "xml":
            self.model_ids[name] = loadMJCF(model)

    def load_model(self) -> None:
        model_paths = self._config["options"]["model_dir"]
        if type(model_paths) == str:
            self._load_model_by_type(model_paths)
        elif type(model_paths) == list:
            for model in model_paths:
                self._load_model_by_type(model)
            

    def run_simulation(self):
        for step in range(1,self.MAX_STEPS):
            stepSimulation()
            sleep(self.TIMESTEP)

if __name__ == "__main__":
    pb = PyBulletEnv()
    pb.set_gui(True)
    pb.connect()
