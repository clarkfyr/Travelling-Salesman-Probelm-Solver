import numpy as np
import pdb
import copy

class Vertex:
    def __init__(self, index, value):
        self.index = index
        self.value = value
        self.neighbors = []

    def add_neighbor(self, index):
        self.neighbors.append(index)

    def has_child(self, v):
        return v.index in self.neighbors

class dummyVertex(Vertex):
    def __init__(self, index):
        Vertex.__init__(self, index, 0)

    def add_neighbor(self, index):
        pass

    def has_child(self, v):
        return False

# Graph is changed but functionalities should remain
class Graph:
    def __init__(self, filename = None):
        if filename is not None:
            f = open(filename, "r")
            self.size = int(f.readline().rstrip())
            adj_list = []
            for line in f:
                adj_list.append(line.split())
            self.adj_list = np.array(adj_list)
            self.reversed = False
            self.set_vertices()

    def reverse(self):
        self.reversed = True
        self.adj_list = self.adj_list.T
        self.set_vertices()

    def cal_score(self, assignment):
        score = 0
        for path in assignment:
            values = [self.vertices[i].value for i in path]
            score += sum(values) * len(values)
        return score

    def set_vertices(self):
        i = 0 # Index of vertex
        self.vertices = []
        self.numE = 0
        for row in self.adj_list:
            # line = line.split()
            # pdb.set_trace()
            v = Vertex(i, int(row[i]))
            # Add neighbors
            for j in range(self.size):
                if j != i and (row[j] != 0 and row[j] != "0"):
                    v.add_neighbor(j)
                    self.numE += 1
            self.vertices.append(v)
            i += 1

    def add_vertices(self, vertices):
        self.vertices = vertices
        self.numE = 0
        for v in vertices:
            self.numE += len(v.neighbors)

def delete_given_path(graph, path):
    g = copy.deepcopy(graph)
    vertices = g.vertices
    for v in vertices:
        if v.index in path:
            vertices[v.index] = dummyVertex(v.index)
        else:
            for n in v.neighbors:
                if n in path:
                    v.neighbors.remove(n)
    return g

    # def get_score_by_list(self, list_index):
    #     score = 0
    #     temp = list_index.pop(0)
    #     temp_multiplier = 1
    #     while len(list_index) != 0


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
