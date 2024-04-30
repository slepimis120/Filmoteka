from typing import List, Type
from api.tmdb_source_api import DataSourceAPI
from api.block_visualizer_api import VisualizerAPI

class PluginManager:
    def __init__(self):
        self.data_source_plugins: List[Type[DataSourceAPI]] = []
        self.visualizer_plugins: List[Type[VisualizerAPI]] = []

    def register_data_source_plugin(self, plugin: Type[DataSourceAPI]):
        self.data_source_plugins.append(plugin)

    def register_visualizer_plugin(self, plugin: Type[VisualizerAPI]):
        self.visualizer_plugins.append(plugin)

    def get_data_source_plugins(self) -> List[Type[DataSourceAPI]]:
        return self.data_source_plugins

    def get_visualizer_plugins(self) -> List[Type[VisualizerAPI]]:
        return self.visualizer_plugins