from typing import Any, Protocol, KeysView, Dict, TypeVar
from pandas.core.frame import DataFrame
from tkinter.font import Font

DataInterfaceT = TypeVar("DataInterfaceT", bound="DataInterface")
DictT = Dict[str, Dict]


class PluginOptions(Protocol):
    _PLUGIN_READABLE_NAMES: dict
    _PLUGIN_MODULE_OPTIONS: dict
    _PLUGIN_REQUIRED_SETTINGS: dict
    _PLUGIN_OPTIONAL_SETTINGS: dict
    _PLUGIN_REQUIRED_DATA: dict
    _PLUGIN_OPTIONAL_DATA: dict


class DataInterface(Protocol):
    def __init__(self) -> None:
        ...

    def import_data(self, config: dict) -> None:
        ...

    def import_data_from_config(self, config: dict) -> None:
        ...

    def append_data_column(self, col_name: str, data=None) -> None:
        ...

    def keys(self) -> KeysView:
        ...

    def copy(self: DataInterfaceT) -> DataInterfaceT:
        ...

    def __getitem__(self, key: str) -> DataFrame:
        ...


class PluginInterface(Protocol):
    def configure(self, config: dict) -> None:
        ...

    def set_data_in(self, data_in: DataInterface) -> None:
        ...


class DataProcessingPluginInterface(PluginInterface, Protocol):
    def fit(self):
        ...

    def transform(self, data: DataInterfaceT) -> DataInterface:
        ...

class EnvironmentPluginInterface(PluginInterface, Protocol):
    def load_model(self) -> None:
        ...

    def connect(self):
        ...

    def reset(self):
        ...

    def disconnect(self):
        ...

    def run_simulation(self):
        ...


class PluginSpecsInterface(Protocol):
    @property
    def names(self):
        ...

    @property
    def class_names(self):
        ...

    @property
    def module_options(self):
        ...

    @property
    def required_settings(self):
        ...

    @property
    def class_descriptions(self):
        ...

    @property
    def optional_settings(self):
        ...

    @property
    def available_plugin_names(self):
        ...

    def find_from_class_name(self, value):
        ...

    def find_from_readable_name(self, value):
        ...

    def print(self, value):
        ...


class ModuleInterface(Protocol):
    def set_avail_plugins(self, avail_plugins: PluginSpecsInterface):
        ...

    def set_data_in(self, data_in: DataInterface):
        ...

    def set_options(self, module_config: DictT):
        ...

    def launch(self):
        ...

    def get_result(self) -> DataInterface:
        ...

class GUICoreInterface(ModuleInterface,Protocol):
    title: Any #mypy bug prevents proper typing
    pages_font: Font

    def destroy(self) -> None:
        ...

    def set_gui(self) -> None:
        ...

class InputDataCoreInterface(ModuleInterface,Protocol):
    def load_data_from_file(self, filename:str, data_id:str) -> None:
        ...