#!/usr/bin/python
"""Module that, given a graph, using Z3, states whether there exist a Hamiltonian graph in it."""
from argparse import ArgumentParser

import matplotlib.pyplot as plt
from networkx import draw_networkx
from networkx import erdos_renyi_graph
from z3.z3types import Z3Exception

from graph_reader import read_graph
from graph_solver import GraphSolver

def _parse_arguments():
    """
    Function to parse the single command line argument `filename` and the single optional flag
    `--verbose`|`-v`. `filename` points to the file containing the JSON representation of the graph
    and the optional flag states wheter the output should be verbose or not.
    """
    parser = ArgumentParser(prog='hamilton-z3', description='Find Hamiltonian paths.')
    with_filename = parser.add_argument_group(title='graph file provided',
                                              description='Necessary arguments when the path to a '
                                              'file is provided')
    random_graph = parser.add_argument_group(title='random graph',
                                             description='Necessary arguments to generate a random '
                                             'graph')

    with_filename.add_argument('filename', type=str, nargs='?',
                               help='filename containing the input graph in JSON format')

    random_graph.add_argument('--nodes', '-n', type=int, metavar='N',
                              help='number of nodes when generating random graph')
    random_graph.add_argument('--probability', '-p', type=float, metavar='P',
                              help='probability of edge creation when generating random graph')

    parser.add_argument('--verbose', '-v', action='store_true', help='show Z3 script and model')
    parser.add_argument('--draw', '-d', action='store_true', help='draw graph before solving')
    parser.add_argument('--drawresult', '-dr', action='store_true', dest='draw_result',
                        help='draw result graph')
    args = parser.parse_args()
    return args.filename, args.nodes, args.probability, args.verbose, args.draw, args.draw_result

def _random_graph(nodes, probability):
    """Function that returns a random graph given the user input parameters."""
    if nodes is None:
        raise TypeError('Argument --nodes must be provided in order to generate a random graph'
                        '\nSee --help for more information')
    if probability is None:
        raise TypeError('Argument --probability must be provided in order to generate a random '
                        'graph.\nSee --help for more information')
    if probability < 0 or probability > 1:
        raise ValueError('Invalid probability: {}. This value must be a number between 0 and 1.'
                         .format(probability()))

    return erdos_renyi_graph(nodes, probability)

def main():
    """Main function"""
    filename, nodes, probability, verbose, to_draw, draw_result = _parse_arguments()

    graph = _random_graph(nodes, probability) if filename is None else read_graph(filename)

    if to_draw:
        draw_networkx(graph)
        plt.title(filename if filename else 'Random graph')
        plt.show()

    solver = GraphSolver(graph)
    if verbose:
        print(solver.to_smt2())
    print(solver.check())
    try:
        solver.draw_model(verbose, draw_result)
    except Z3Exception:
        pass

if __name__ == '__main__':
    main()
