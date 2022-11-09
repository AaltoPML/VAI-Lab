from attr import attr
from vai_lab._plugin_templates import EnvironmentPluginT
from vai_lab._import_helper import rel_to_abs
from typing import Any, Dict
import pybullet as p
from time import sleep


_PLUGIN_READABLE_NAMES = {"PyBullet":"default"}                                                 # type:ignore
_PLUGIN_MODULE_OPTIONS = {}                                                                     # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"model_dir": "str", "headless": "bool",
                                "timestep":"float", "max_steps":"int"}                          # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"gravity":"list"}                                                  # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                                                      # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X","Y","X_tst", 'Y_tst'}                                              # type:ignore


class PyBulletEnv(EnvironmentPluginT):
    """
    Loads the pybullet library as wildcard and exposes all functions
    """

    def __init__(self) -> None:
        super().__init__(globals())
        self.connection_mode = p.GUI
        self.model_ids: Dict = {}

    def set_gui(self, use_gui: bool = True):
        if use_gui:
            self.connection_mode = p.GUI  # Use pybullet GUI
        else:
            self.connection_mode = p.DIRECT  # Use pybullet without GUI

    def connect(self):
        self.physicsClient = p.connect(self.connection_mode)

    def disconnect(self):
        return p.disconnect()

    def reset(self):
        return p.resetSimulation()

    def load_pb_data(self):
        import pybullet_data                                        # type:ignore
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

    def _load_model_by_type(self, model):
        model = rel_to_abs(model)
        ext = model.split(".")[-1]
        name = model.split("/")[-1].split(".")[0]
        if name == "plane":
            self.load_pb_data()
        if ext == "urdf":
            self.model_ids[name] = p.loadURDF(model)
        elif ext == "sdf":
            self.model_ids[name] = p.loadSDF(model, 1, 1.0)
        elif ext == "xml":
            self.model_ids[name] = p.loadMJCF(model)

    def load_model(self) -> None:
        model_paths = self._config["options"]["model_dir"]
        if type(model_paths) == str:
            self._load_model_by_type(model_paths)
        elif type(model_paths) == list:
            for model in model_paths:
                self._load_model_by_type(model)

    def _set_options(self):
        api_list = dir(p)
        for key, value in self._config["options"].items():
            if key in api_list:
                getattr(p,key)(*value)
        if "timestep" in self._config["options"]:
            p.setPhysicsEngineParameter(
                fixedTimeStep=self._config["options"]["timestep"])
        elif "max_steps" in self._config["options"]:
            p.setPhysicsEngineParameter(
                numSolverIterations=self._config["options"]["max_steps"])

    def run_simulation(self):
        self._set_options()
        for step in range(1, self._config["options"]["max_steps"]):
            p.stepSimulation()
            sleep(self._config["options"]["timestep"])
        self.disconnect()

    def __getattr__(self, attr: str) -> Any:
        """Allows calling pybullet functions directly as if they were functions of this class

        TODO: This is probably not the best way to do this, but pybullet is
        a compiled module and cannot be used as a parent. This is a workaround.
        """
        return getattr(p, attr)


if __name__ == "__main__":
    pb = PyBulletEnv()
    print(pb.ACTIVATION_STATE_DISABLE_SLEEPING)
    # pb.set_gui(True)
    # pb.connect()
