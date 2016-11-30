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

class Graph:
    def __init__(self, filename):
        f = open(filename, "r")
        n = int(f.readline().rstrip())
        i = 0 # Index of vertex
        self.vertices = []
        self.numE = 0
        for line in f:
            line = line.split()
            v = Vertex(i, int(line[i]))
            # Add neighbors
            for j in range(n):
                if j != i and line[j] == '1':
                    v.add_neighbor(j)
                    self.numE += 1
            self.vertices.append(v)
            i += 1
    def delete_given_path(self, path):
        g = copy.deepcopy(self)
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

