from django.apps import AppConfig
from api.model import Graph
import pkg_resources


class FilmotekaPlatformConfig(AppConfig):
    name = 'filmoteka_platform'
    original_graph = Graph()
    graph = Graph()
    visualizer_plugins = []
    data_source_plugins = []
    graph_attributes = {}
    active_filters = []

    def ready(self):
        self.visualizer_plugins = load_plugins("visualiser")
        self.data_source_plugins = load_plugins("parser")
        print("Visualizer plugins: ", self.visualizer_plugins)
        print("Data source plugins: ", self.data_source_plugins)


def load_plugins(plugin_type):
    plugins = []
    for entry_point in pkg_resources.iter_entry_points(group=plugin_type):
        p = entry_point.load()
        plugin = p()
        plugins.append(plugin)
    return plugins
