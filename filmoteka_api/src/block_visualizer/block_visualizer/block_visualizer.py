# block_visualizer.py

from django.template.loader import render_to_string
from api.block_visualizer_api import VisualizerAPI
from api.model import Graph
from django.template import engines
import json


class BlockVisualizer(VisualizerAPI):
    def name(self):
        return "Block Visualizer"

    def identifier(self):
        return "Block_Visualizer"

    def visualize(self, graph: Graph):
        vertices = [{"ID": vertex.id, "attributes": vertex.attributes} for vertex in graph.vertices]
        edges = [{"source": edge.start_vertex.id, "target": edge.end_vertex.id} for edge in graph.edges]

        context = {
            'vertices': json.dumps(vertices),
            'edges': json.dumps(edges)
        }

        django_engine = engines['django']
        template_html = django_engine.get_template('block_visualizer.html')
        html_output = template_html.render(context)
        return html_output