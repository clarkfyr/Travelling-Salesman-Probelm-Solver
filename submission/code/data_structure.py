"""
Data Structure class file:
    Vertex
    DummyVertex
    Graph
    Subproblem (TSP)
    SCC
"""
import numpy as np

class Vertex:
    def __init__(self, index, value):
        self.index = index
        self.value = value
        self.neighbors = []

    def add_neighbor(self, index):
        self.neighbors.append(index)

    def has_child(self, v):
        return v.index in self.neighbors


class DummyVertex(Vertex):
    def __init__(self, index):
        Vertex.__init__(self, index, 0)

    def add_neighbor(self, index):
        pass

    def has_child(self, v):
        return False


class Graph:
    """
    Instance Variables:
    self.adj_list: adjoint list of this graph, can be edited to suppport tweaks to the graph
    self.adj_list_backup: original adjoint list of this graph. Used to restore the graph after tweaks
    """
    def __init__(self, filename = None):
        if filename is not None:
            f = open(filename, "r")
            self.size = int(f.readline().rstrip())
            adj_list = []
            for line in f:
                adj_list.append([int(s) for s in line.split()])
            self.adj_list = np.array(adj_list)
            self.adj_list_backup = np.array(adj_list)
            self._set_vertices(self.adj_list)

    # Reverse the graph
    def reverse(self):
        self.adj_list = self.adj_list.T
        self._set_vertices(self.adj_list)

    # Change graph to undirected
    def undirected(self):
        self.adj_list = self.adj_list + self.adj_list.T
        self._set_vertices(self.adj_list)

    # Restore the original graph
    def restore(self):
        self._set_vertices(self.adj_list_backup)

    # set the vertices after the adjoint list is changed/created.
    def _set_vertices(self, adj_list):
        i = 0 # Index of vertex
        self.vertices = []
        self.numE = 0
        for row in adj_list:
            v = Vertex(i, int(row[i]))
            # Add neighbors
            for j in range(self.size):
                if (j != i and row[j] != 0):
                    v.add_neighbor(j)
                    self.numE += 1
            self.vertices.append(v)
            i += 1

    def add_vertices(self, vertices):
        self.vertices = vertices
        self.numE = 0
        for v in vertices:
            self.numE += len(v.neighbors)

    def print_graph(self):
        for i in range(self.size):
            line = ""
            # print(self.sccs[i].scc_neighbors)
            for j in range(self.size):
                if (j in self.vertices[i].neighbors):
                    line += str(1) + " "
                else:
                    if (i == j):
                        line += str(self.vertices[i].value) + " "
                    else:
                        line += str(0) + " "
            print(line)


class Subproblem:
    def __init__(self, start, end, visited, path, score):
        self.start = start
        self.end = end
        self.visited = visited
        self.size = len(visited)
        self.path = path
        self.score = score

    def update_path_score(self, v):
        if not self.path: # Base case
            self.path = [[v]]
            self.score = v.value
        else:
            end = self.path[len(self.path) - 1][(-1):][0]
            if not end.has_child(v):
                self.path.append([v])
                self.score += v.value
            else:
                last_path = self.path[len(self.path) - 1]
                self.score -= sum([x.value for x in last_path]) * len(last_path)
                last_path.append(v)
                self.score += sum([x.value for x in last_path]) * len(last_path)


class SCC(Graph, Vertex):

    def __init__(self, g, vertices, index):
        self.vertices = vertices # Object
        self.neighbors = []
        self.internals = []
        self.parent_graph = None
        self.in_vertices = [] # Index
        self.out_vertices = [] # Index
        self.numEdge = 0
        self.g = g
        self.index = index
        if (len(vertices) == 1):
            self.value = vertices[0].value
        else:
            self.value = 0

        # Find the neighbor vertices and internal vertices of SCC
        for vertex in self.vertices:
            self.internals.append(vertex.index)
            for neighbor in vertex.neighbors:
                if (neighbor not in self.vertices and neighbor not in self.neighbors):
                    self.neighbors.append(neighbor)

        # Find the number of edges inside a SCC
        for vertex in self.vertices:
            for neighbor in list(set().union(vertex.neighbors, self.internals)):
                self.numEdge += 1

        # Set in/out vertices a SCC
        out_vertices = set()
        for vertex in self.vertices:
            for neighbor in vertex.neighbors:
                if (neighbor not in self.internals):
                    out_vertices.add(neighbor)
        self.out_vertices = list(out_vertices)
        in_vertices = set()
        for vertex in self.g.vertices:
            for neighbor in vertex.neighbors:
                if (neighbor in self.internals):
                    in_vertices.add(neighbor)
        self.in_vertices = list(in_vertices)

    def trim_neighbors(self):
        """ Set the neighbors of vertices to have only internal vertices s"""
        for vertex in self.vertices:
            for neighbor in vertex.neighbors:
                if (neighbor not in self.internals):
                    vertex.neighbors.remove(neighbor)
