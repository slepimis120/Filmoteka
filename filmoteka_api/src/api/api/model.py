from typing import *


class Vertex:
    def __init__(self):
        self._id = "-1"
        self._attributes = {}
        self._has_been_found = True
        self._children = []

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        self._children = children

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, identification):
        self._id = identification

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        self._attributes = attributes

    @property
    def has_been_found(self):
        return self._has_been_found

    @has_been_found.setter
    def has_been_found(self, has_been_found):
        self._has_been_found = has_been_found

    def __str__(self):
        text = str(self._id)
        if self._attributes:
            for key, value in self._attributes.items():
                text += "\n" + str(key) + ": " + str(value)
        return text


class Edge:
    def __init__(self):
        self.__start_vertex: Vertex = Vertex()
        self.__end_vertex: Vertex = Vertex()

    @property
    def start_vertex(self):
        return self.__start_vertex

    @start_vertex.setter
    def start_vertex(self, vertex: Vertex):
        self.__start_vertex = vertex

    @property
    def end_vertex(self):
        return self.__end_vertex

    @end_vertex.setter
    def end_vertex(self, vertex: Vertex):
        self.__end_vertex = vertex


class Graph:
    def __init__(self):
        self.__vertices: Set[Vertex] = set()
        self.__edges: Set[Edge] = set()

    @property
    def vertices(self):
        return self.__vertices

    @vertices.setter
    def vertices(self, vertices: Set[Vertex]):
        self.__vertices = vertices

    @property
    def edges(self):
        return self.__edges

    @edges.setter
    def edges(self, edges: Set[Edge]):
        self.__edges = edges
