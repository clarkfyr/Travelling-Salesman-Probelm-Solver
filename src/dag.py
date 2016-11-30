import object
import pdb
import copy

class SCC(object.Graph, object.Vertex):
    def __init__(self, vertices):
        self.vertices = vertices
        self.neighbors = []
        self.internals = []
        self.scc_neighbors = []
        for vertex in self.vertices:
            self.internals.append(vertex.index)
            for neighbor in vertex.neighbors:
                if (neighbor not in self.vertices and neighbor not in self.neighbors):
                    self.neighbors.append(neighbor)

# Helper class for doing DFS on a graph
class DFS:
    def __init__(self, g):
        self.g = g
        self.i = 0
        self.visited = set()
        self.pre_nums = [0 for _ in range(len(g.vertices))]
        self.post_nums = [0 for _ in range(len(g.vertices))]

    # Return the pre numbers and post numbers after DFS
    def dfs(self):
        # While not all vertices are visited
        while (len(self.visited) < len(self.g.vertices)):
            # Find the first unvisited vertex
            unvisited = [i for i in range(self.g.size) if self.g.vertices[i].index not in self.visited][0]
            # Run DFS starting from this vertex
            self._dfs(self.g, self.g.vertices[unvisited])
        return self.pre_nums, self.post_nums

    def _dfs(self, g, curr):
        self.visited.add(curr.index)
        self.pre_nums[curr.index] = self.i
        self.i += 1
        for neighbor in curr.neighbors:
            if neighbor not in self.visited:
                self._dfs(g, g.vertices[neighbor])
        self.post_nums[curr.index] = self.i
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

# Transform a graph into a dag of SCC
class DAG(object.Graph):

    def __init__(self, filename):

        # Initialize a graph
        # self.connected: whether this graph is connected
        # self.sccs: list of SCC in this graph
        # self.scc_neighbors: list of SCC neighbors of SCCs.
        object.Graph.__init__(self, filename)

        # Find all sccs
        # Run DFS on GR
        self.reverse()
        dfs_helper = DFS(self)
        post_nums = dfs_helper.dfs()[1]
        self.connected = len(dfs_helper.explore(post_nums.index(min(post_nums)))) == self.size
        self.reverse()

        # Explore in decreasing post number order
        self.sccs = []
        to_explore = post_nums
        # indices of removed vertices
        removed = set()
        # removed vertices
        removed_vertices = set()
        while (len(to_explore) > 0):
            scc_indices = dfs_helper.explore(post_nums.index(max(to_explore)))
            removed = removed.union(scc_indices)
            to_explore = [post_nums[i] for i in range(len(post_nums)) if i not in removed]
            scc_vertices = [vertex for vertex in self.vertices if vertex.index in scc_indices]
            scc_vertices = set(scc_vertices).difference(removed_vertices)
            new_scc = SCC(list(scc_vertices))
            removed_vertices = removed_vertices.union(scc_vertices)
            self.sccs.append(new_scc)



        # Index sccs
        self.sccs.reverse()
        for i in range(len(self.sccs)):
            self.sccs[i].index = i

        # Find the neighbor sccs of all sccs
        self.scc_neighbors = []
        for i in range(len(self.sccs)):
            neighbors = []
            for vertex in self.sccs[i].vertices:
                for vertex_neighbor in vertex.neighbors:
                    if vertex_neighbor not in self.sccs[i].internals:
                        neighbors.append(self.locate_scc(vertex_neighbor))
            self.scc_neighbors.append(neighbors)

    def locate_scc(self, vertex_index):
        for scc in self.sccs:
            if vertex_index in scc.internals:
                return scc.index
        return -1

    def print_graph(self):
        for i in range(len(self.sccs)):
            line = ""
            # print(self.sccs[i].scc_neighbors)
            for j in range(len(self.sccs)):
                if (j in self.scc_neighbors[i]):
                    line += str(1) + " "
                else:
                    line += str(0) + " "
            line += "Nodes: "
            line += ", ".join(list(map(str, self.sccs[i].internals)))
            print(line)

    # Return if the original graph is a dag or not
    def is_dag(self):
        return len(self.sccs) == len(self.vertices)


    # Miss Dong's algorithm on how to compute max in a dag
    # User should make sure that this function is only called on
    # a dag.
    # User is_dag to check if a graph is a dag
    def partition(self):
        sub = [[[0, []] for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            sub[i][i][0] = self.vertices[i].value
            sub[i][i][1].append([self.vertices[i].index])
        for m in range(1, self.size):
            # pdb.set_trace()
            sub_range = list(range(m))
            sub_range.reverse()
            for i in sub_range:
                max_val = 0
                max_assignment = []
                for k in range(i+1, m+1):
                    assignment = copy.deepcopy(sub[k][m][1])
                    if (k in self.vertices[i].neighbors):
                        assignment[0].insert(0,i)
                    else:
                        assignment.insert(0,[i])
                    if k > i + 1:
                        value = self.cal_score(assignment) + sub[i+1][k-1][0]
                        assignment = assignment + sub[i+1][k-1][1]
                    else:
                        value = self.cal_score(assignment)
                    if (value > max_val):
                        max_val = value
                        max_assignment = copy.deepcopy(assignment)
                sub[i][m] = [max_val, max_assignment]
        return sub[0][self.size - 1]

# Test
if __name__ == '__main__':
    import time
    start_time = time.time()

    g = DAG("../final_inputs/25.in")
    g.print_graph()
    sol = g.partition()
    print(sol[0])
    print(sol[1])

    print("--- %s seconds ---" % (time.time() - start_time))
