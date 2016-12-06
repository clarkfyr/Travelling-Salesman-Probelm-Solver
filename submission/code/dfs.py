import dag
import data_structure as ds
import random
import utility
import time


# Helper class for doing DFS on a graph
class DFS:
    def __init__(self, g):
        self.g = g
        self.i = 0
        self.visited = set()
        self.pre_nums = [0 for _ in range(len(g.vertices))]
        self.post_nums = [0 for _ in range(len(g.vertices))]

    # Return the pre numbers and post numbers after DFS
    def dfs(self, sources = [], rand = False):
        # While not all vertices are visited
        while (len(self.visited) < len(self.g.vertices)):
            # Find the first unvisited source
            unvisited = [i for i in range(self.g.size) if self.g.vertices[i].index not in self.visited]
            unvisited_sources = list(set().union(unvisited, sources))
            # If there is an unvisited source, start from unvisted source
            # Otherwise, start at any unvisted vertex
            if (len(unvisited_sources) > 0):
                start = random.choice(unvisited_sources)
            else:
                start = random.choice(unvisited)
            # Run DFS starting from this vertex
            self._dfs(self.g, start, rand)
        return self.pre_nums, self.post_nums

    def _dfs(self, g, curr, rand):
        self.visited.add(curr)
        self.pre_nums[curr] = self.i
        self.i += 1
        if (rand):
            # random.sample(x, len(x))
            neighbors = random.sample(self.g.vertices[curr].neighbors, len(self.g.vertices[curr].neighbors))
        else:
            neighbors = self.g.vertices[curr].neighbors

        for neighbor in neighbors:
            if neighbor not in self.visited:
                self._dfs(g, neighbor, rand)
        self.post_nums[curr] = self.i
        self.i += 1

    # Return all nodes can be reached from start node
    def explore(self, start):
        # print(self.g.adj_list)
        # print(start)
        stack = [start]
        visited = set()
        # visited_vertices = []
        while (len(stack) > 0):
            curr = stack.pop()
            visited.add(curr)
            # visited_vertices = visited_vertices.append(self.g.vertices[curr])
            for neighbor in self.g.vertices[curr].neighbors:
                if (neighbor not in visited):
                    stack.append(neighbor)
        return visited


def find_sources_and_singles(graph):
    sources = [_.index for _ in graph.vertices][:] # Index
    singles = [] # Index
    for v in graph.vertices:
        for vv in v.neighbors:
            if vv in sources:
                sources.remove(vv)
    for s in sources:
        if not graph.vertices[s].neighbors:
            singles.append(s)
    sources = list(set(sources) - set(singles))
    return {'sources': sources, 'singles': singles}


def dfs_approximate(graph):
    total_path = []
    temp = find_sources_and_singles(graph)
    singles = temp['singles']
    sources = temp['sources']

    # Add disconnected single vertices
    for single in singles:
        total_path.append([single])
    new_graph = ds.delete_given_path(graph, singles)

    # If no source, it's a huge cycle
    total_path = random_dfs_explore(graph, sources)

    return total_path


def random_dfs_explore(graph, sources):
    magic = dag.DFS(graph)
    pre_nums = magic.dfs(sources, True)[0]
    indices = [index for value, index in sorted((e,i) for i,e in enumerate(pre_nums))]
    return indices


def run(p):
    result = open('new_5000.txt', "a")
    for i in range(p, p+1):

        try:
            start_time = time.time()
            path_list = [];
            temp_score = 0
            temp_path = []
            print(str(i)+".in")
            g = ds.Graph("../inputs/all/" + str(i) + ".in")
            for j in range(0, 10000):
                order = (random_dfs_explore(g, find_sources_and_singles(g)["sources"]))
                path = ds.get_path_from_order(g, order)
                path_list.append(path)
            for p in path_list:
                score = utility.compute_score_full_assignment(g, p)
                if score >= temp_score:
                    temp_path = p
                    temp_score = score
            soln = temp_path
            result.write(str(i) + ". " + str(soln))
            result.write("\n")
            result = open('new_5000.txt', "a")
            print(i, soln)
            print("--- %s seconds to solve graph---" % (time.time() - start_time))
        except (IOError):
            pass
