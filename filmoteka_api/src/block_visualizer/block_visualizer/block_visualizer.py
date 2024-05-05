import os

from api.block_visualizer_api import VisualizerAPI
from api.model import Graph
from django.template import Template, Context


class BlockVisualizer(VisualizerAPI):
    def name(self):
        return "Block Visualizer"

    def identifier(self):
        return "Block_Visualizer"

    def visualize(self, graph: Graph):
        with open(os.path.join(os.path.dirname(__file__), 'templates', 'block_visualizer.html'), 'r') as f:
            rawTemplate = f.read()
        template = Template(rawTemplate)
        context = Context({"graph": graph})
        return template.render(context)
