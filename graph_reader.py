"""Module that implements functions to read graphs.

The input graph will be passed as an argument to the program. It has to be represented in JSON
format:

{nodes: list_of_vertices, edges: list_of_edges}

being list_of_edges a list of pairs (i,j), such that i and j are adjacent vertices in the graph.
"""
from json import load

from networkx import Graph

def read_graph(filename):
    """Reads a graph from filename in JSON format"""
    graph_json = None
    with open(filename) as json:
        graph_json = load(json)

    graph = Graph()
    graph.add_nodes_from(graph_json['nodes'])
    graph.add_edges_from(graph_json['edges'])
    return graph
