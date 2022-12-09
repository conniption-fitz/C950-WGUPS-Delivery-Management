"""
The graphClass.py file contains both the Vertex class and the Graph class.

Vertex objects contain a label and address attribute, and have a get_address method.

Graph objects have an adjacency_list dictionary which holds all vertices, and a dictionary of edge_weights, which holds
the distance between each Vertex. The get_edge_weight method returns the distance between two vertices, which are passed
as arguments, when called.
"""


class Vertex:
    def __init__(self, label, address):
        self.label = label
        self.address = address

    def get_address(self):
        return self.address


class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    def add_directed_edge(self, from_vertex, to_vertex, weight=1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    def get_edge_weight(self, from_vertex, to_vertex):
        return self.edge_weights[(from_vertex, to_vertex)]
