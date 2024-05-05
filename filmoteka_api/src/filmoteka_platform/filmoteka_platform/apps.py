from django.apps import AppConfig
import pkg_resources


class FilmotekaPlatformConfig(AppConfig):
    name = 'filmoteka_platform'
    visualizer_plugins = []
    data_source_plugins = []

    def ready(self):
        self.visualizer_plugins = load_plugins("visualizer")
        self.data_source_plugins = load_plugins("parser")


def load_plugins(plugin_type):
    plugins = []
    for entry_point in pkg_resources.iter_entry_points(group=plugin_type):
        p = entry_point.load()
        plugin = p()
        plugins.append(plugin)
    return plugins
