import json

from django.apps import apps
from api.json_parser_api import JSONParserAPI
from api.model import *


class JSONParser(JSONParserAPI):
    def name(self):
        return "JSON parser"

    def identifier(self):
        return "json_parser"

    def parse(self, path):
        with open(path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        graph = Graph()
        root_vertex = self._create_vertex_from_json(graph, data)
        apps.get_app_config('filmoteka_platform').rootId = root_vertex.id
        graph.vertices.add(root_vertex)

        self._create_edges_and_children(graph, root_vertex, data.get('child', []))

        self._update_graph_attributes(graph)

        return graph

    def _create_vertex_from_json(self, graph, data):
        existing_vertex = next((v for v in graph.vertices if v.id == data['ID']), None)
        if existing_vertex:
            return existing_vertex

        vertex = Vertex()
        vertex.id = data['ID']
        vertex.attributes = {
            'Original Title': data['Original Title'],
            'Popularity': data['Popularity'],
            'Release Date': data['Release Date']
        }
        return vertex

    def _create_edges_and_children(self, graph: Graph, parent_vertex: Vertex, children_data: List[dict]):
        for child in children_data:
            child_vertex = self._create_vertex_from_json(graph, child)
            graph.vertices.add(child_vertex)

            edge = Edge()
            edge.start_vertex = parent_vertex
            edge.end_vertex = child_vertex
            graph.edges.add(edge)

            parent_vertex.children.append(child_vertex)

            if 'child' in child:
                self._create_edges_and_children(graph, child_vertex, child['child'])

    def _update_graph_attributes(self, graph):
        attributes = {}
        for vertex in graph.vertices:
            for attr, value in vertex.attributes.items():
                if attr not in attributes:
                    attributes[attr] = type(value).__name__
        apps.get_app_config('filmoteka_platform').graph_attributes = attributes
