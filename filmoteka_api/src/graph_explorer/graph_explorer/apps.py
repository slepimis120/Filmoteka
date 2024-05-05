import pkg_resources
from django.apps import AppConfig
from filmoteka_platform.plugin_manager import PluginManager


class GraphExplorerConfig(AppConfig):
    name = 'graph_explorer'
    default_auto_field = 'django.db.models.BigAutoField'
    plugin_manager = PluginManager()

    def ready(self):
        load_plugins("parser", self.plugin_manager.register_data_source_plugin)
        load_plugins("visualiser", self.plugin_manager.register_visualizer_plugin)

        # Ispisivanje svih učitanih data source pluginova
        print("Data source plugins:")
        for plugin in self.plugin_manager.get_data_source_plugins():
            print(f"- {plugin.name()}")

        # Ispisivanje svih učitanih visualizer pluginova
        print("Visualizer plugins:")
        for plugin in self.plugin_manager.get_visualizer_plugins():
            print(f"- {plugin.name()}")


def load_plugins(plugin_name, register_method):
    for ep in pkg_resources.iter_entry_points(group=plugin_name):
        p = ep.load()
        plugin = p()
        register_method(plugin)
