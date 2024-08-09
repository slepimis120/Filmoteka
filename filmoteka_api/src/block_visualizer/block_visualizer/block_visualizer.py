# block_visualizer.py

from api.block_visualizer_api import VisualizerAPI
from api.model import *
from django.template import engines
import json
from django.apps import apps


class BlockVisualizer(VisualizerAPI):
    def name(self):
        return "Block Visualizer"

    def identifier(self):
        return "Block_Visualizer"

    def visualize(self, graph: Graph):
        config = apps.get_app_config('filmoteka_platform')
        active_filters = config.active_filters

        if active_filters:
            filtered_graph = Graph()

            for vertex in graph.vertices:
                matches_all_filters = all(
                    self.apply_filter(vertex, f['parameter_name'], f['comparator'], f['value'])
                    for f in active_filters
                )
                if matches_all_filters:
                    filtered_graph.vertices.add(vertex)

            filtered_edges = set()
            for edge in graph.edges:
                if edge.start_vertex in filtered_graph.vertices and edge.end_vertex in filtered_graph.vertices:
                    filtered_edges.add(edge)

            filtered_graph.edges = filtered_edges

            config.graph = filtered_graph
        else:
            config.graph = graph

        vertices_data = [{"ID": vertex.id, "attributes": vertex.attributes} for vertex in config.graph.vertices]
        edges_data = [{"source": edge.start_vertex.id, "target": edge.end_vertex.id} for edge in config.graph.edges]

        context = {
            'vertices': json.dumps(vertices_data),
            'edges': json.dumps(edges_data)
        }

        django_engine = engines['django']
        template_html = django_engine.get_template('block_visualizer.html')
        html_output = template_html.render(context)

        return html_output

    def apply_filter(self, item, parameter, comparator, value):
        if isinstance(item, Vertex):
            attributes = item.attributes
        elif isinstance(item, Edge):
            attributes = {
                'start_vertex_id': item.start_vertex.id,
                'end_vertex_id': item.end_vertex.id
            }
        else:
            return False

        item_value = attributes.get(parameter, None)

        try:
            item_value = float(item_value)
            value = float(value)
        except (ValueError, TypeError):
            pass

        if comparator == '==':
            return item_value == value
        elif comparator == '!=':
            return item_value != value
        elif comparator == '>':
            return item_value > value
        elif comparator == '<':
            return item_value < value
        elif comparator == '>=':
            return item_value >= value
        elif comparator == '<=':
            return item_value <= value
        elif comparator == 'contains':
            if isinstance(item_value, str) and isinstance(value, str):
                return value in item_value
            return False
        else:
            return False

