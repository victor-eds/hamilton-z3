"""Module implementing class GraphSolver"""
from collections import deque

import matplotlib.pyplot as plt
from networkx import draw_networkx_edges
from networkx import draw_networkx_labels
from networkx import draw_networkx_nodes
from networkx import non_neighbors
from networkx import spring_layout
from z3 import Bool
from z3 import Implies
from z3 import Not
from z3 import Or
from z3 import Solver

class GraphSolver(Solver):
    """
    Z3 Solver which, given a graph, adds the needed constants and assertions to itself in order to
    find Hamiltonian paths in the graph.
    """
    def __init__(self, graph):
        """
        GraphSolver constructor which adds the necessary constants and assertions to find
        Hamiltionian paths in the input graph.
        """
        super().__init__()
        self._graph = graph
        self._init_constants()
        self._every_node_appears_once()
        self._every_position_has_a_single_node()
        self._only_adjacent_nodes_together()

    def draw_model(self, verbose, draw_result):
        """Draws generated model, if present"""
        model = self.model()
        if verbose:
            print(model)

        edges = self._edges_from_model(model)
        print(edges)

        if draw_result:
            graph = self._graph
            pos = spring_layout(graph)
            draw_networkx_nodes(graph, pos, nodelist=graph.nodes())
            draw_networkx_edges(graph, pos, edgelist=graph.edges(), style='dotted')
            draw_networkx_edges(graph, pos, edgelist=edges)
            draw_networkx_labels(graph, pos)
            plt.title('Hamiltonian path')
            plt.show()

    def _edges_from_model(self, model):
        """Returns the list of edges in the Hamiltonian path"""
        def find_true(positions, model, nodes):
            i = 0
            node = None
            while node is None:
                position = positions[i]
                if model[position]:
                    node = nodes[i]
                i += 1
            return node

        edges = []
        nodes = list(self._graph.nodes)
        left_node = None
        values = zip(*self._constants.values())
        left_node = find_true(next(values), model, nodes)
        for positions in values:
            right_node = find_true(positions, model, nodes)
            edges.append((left_node, right_node))
            left_node = right_node
        return edges

    def _init_constants(self):
        """
        Initializes Boolean constants: p_i_j for each node i in the graph for each position j in the
        sequence.
        """
        self._constants = {node: [Bool('p_{}_{}'.format(node, i))
                                  for i in range(self._graph.number_of_nodes())]
                           for node in self._graph.nodes()}

    def _unicity_condition(self, positions):
        """
        Adds a set of conditions to solver s.t. they guarantee the uniqueness of each element in
        positions, i.e., (assert (or p_i_0 ... p_i_n))
                         (assert (=> p_i_j (not (or p_i_0 ... p_i_(j-1) p_i_(j+1) ... p_i_n))))
                          for all j
        """
        self.add(Or(positions))
        self.add([Implies(i, Not(Or([j for j in positions if j is not i]))) for i in positions])

    def _every_node_appears_once(self):
        """Adds a set of conditions to guarantee that every node appears exactly one in the path."""
        for positions in self._constants.values():
            self._unicity_condition(positions)

    def _every_position_has_a_single_node(self):
        """Adds a set of conditions to guarantee that every position contains exactly one node."""
        for positions in zip(*self._constants.values()):
            self._unicity_condition(positions)

    def _only_adjacent_nodes_together(self):
        """
        Adds a set of conditions to guarantee that only neighbour vertices can appear in successive
        positions in a sequence.
        """
        for node, positions in self._constants.items():
            positions_deque = deque(positions)
            positions_deque.rotate()
            self.add([Implies(condition[0], Not(Or(condition[1:])))
                      for non_neighbor in non_neighbors(self._graph, node)
                      for condition in list(zip(positions_deque,
                                                self._constants[non_neighbor]))[1:]])
