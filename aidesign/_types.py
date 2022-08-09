from typing import Protocol, KeysView


class PluginOptions(Protocol):
    _PLUGIN_READABLE_NAMES: dict
    _PLUGIN_MODULE_OPTIONS: dict
    _PLUGIN_REQUIRED_SETTINGS: dict
    _PLUGIN_OPTIONAL_SETTINGS: dict
    _PLUGIN_REQUIRED_DATA: dict
    _PLUGIN_OPTIONAL_DATA: dict


class Data(Protocol):
    def __init__(self) -> None:
        ...

    def import_data(self, config: dict) -> None:
        ...

    def import_data_from_config(self, config: dict) -> None:
        ...

    def append_data_column(self, col_name:str, data=None) -> None:
        ...

    def keys(self) -> KeysView:
        ...