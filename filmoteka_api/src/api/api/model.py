class Node:
    def __init__(self, id, data):
        self.id = id
        self.data = data


class Edge:
    def __init__(self, source, target):
        self.source = source
        self.target = target


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)
