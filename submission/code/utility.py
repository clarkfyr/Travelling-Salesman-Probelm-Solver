"""
This file contains all the helper functions we used to build and test
"""
import data_structure as ds
import copy

def get_path_from_order(graph, order):
    """
    Turn a random order path into a valid path
    :param graph: Graph object
    :param order: order (a list of integer)
    :return: paths (list of lists)
    """
    final_path = []
    temp_path = []
    while len(order) > 1:
        curr = order.pop(0)
        next = order[0]
        if not next in graph.vertices[curr].neighbors:
            temp_path.append(curr)
            final_path.append(temp_path)
            temp_path = []
        else:
            temp_path.append(curr)
    final = order.pop()
    temp_path.append(final)
    final_path.append(temp_path)
    return final_path


def check_path(graph, list_of_paths):
    """
    Check if every path within given paths are all valid
    :param graph: Graph object
    :param list_of_paths: list of paths
    :return: True/False
    """
    for path in list_of_paths:
        for i in range(0, len(path) - 1):
            if path[i + 1] not in graph.vertices[path[i]].neighbors:
                return False
    return True


def check_fully_used(graph, list_of_paths):
    """
    Check if all vertices in a given graph are assigned
    and are assigned only once in a given list of paths
    :param graph: Graph object
    :param list_of_paths: list of paths
    :return: True/False
    """
    check = [0 for x in range(0, len(graph.vertices))]
    try:
        for path in list_of_paths:
            for i in range(0, len(path)):
                ind = path[i]
                if check[ind] == 0:
                    check[ind] = 1
                elif check[ind] == 1:
                    return False
        for i in range(0, len(check)):
            if check[i] == 0:
                return False
        return True
    except(IndexError):
        return False


def delete_given_path(graph, path):
    """
    Replace all vertices in a given path from the given graph with DummyVertex
    :param graph: Graph object
    :param path: one path
    :return: Modified graph
    """
    g = copy.deepcopy(graph)
    vertices = g.vertices
    for v in vertices:
        if v.index in path:
            vertices[v.index] = ds.DummyVertex(v.index)
        else:
            for n in v.neighbors:
                if n in path:
                    v.neighbors.remove(n)
    return g


def compute_score_full_assignment(graph, paths):
    """
    Compute the score for a given path
    :param graph: Graph object created by an input file
    :param paths: List of lists
    :return: score value of this paths
    """
    def compute_score(graph, list_of_path):
        """take in a graph and a pathes and compute the score
            under the assuption that the proposed soln is valid"""
        vertices = graph.vertices
        score = 0
        base = 0
        for v in list_of_path:
            base += vertices[v].value
        score += base * len(list_of_path)
        return score

    total = 0
    for path in paths:
        total += compute_score(graph, path)
        return total