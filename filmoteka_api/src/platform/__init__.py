from .plugin_manager import PluginManager
from .graph import Graph
from .workspace import Workspace
from .visualizer import Visualizer

# Inicijalizacija PluginManager-a
plugin_manager = PluginManager()

# Učitavanje svih pluginova
# Ovde bi trebalo da dodate kod za učitavanje svih pluginova
# Na primer, možete koristiti pkg_resources da biste dobili listu svih dostupnih pluginova
# Zatim, za svaki plugin, možete koristiti importlib da biste učitali plugin i registrujete ga u plugin_manager-u

# Inicijalizacija Graph, Workspace i Visualizer klasa
graph = Graph()
workspace = Workspace()
visualizer = Visualizer()