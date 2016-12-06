"""
Exact DAG Algorithm:
    1. Run on Graphs that are exactly DAGs
    2. File contains a DAG class and a run() script
"""

import data_structure as ds
import copy
import time
import dfs

# Transform a graph into a dag of SCC
class DAG(ds.Graph):

    def __init__(self, filename):
        ds.Graph.__init__(self, filename)
        self.sccs = []
        self.scc_neighbors = []
        self.sub_graphs = []
        self.find_sccs()
        self.scc_size = len(self.sccs)

    def find_sccs(self):
        """
        Find all SCCs
        """
        self.reverse()
        dfs_helper = dfs.DFS(self)
        post_nums = dfs_helper.dfs()[1]
        self.connected = len(dfs_helper.explore(post_nums.index(min(post_nums)))) == self.size
        self.reverse()

        # Explore in decreasing post number order
        to_explore = post_nums
        # indices of removed vertices
        removed = set()
        # removed vertices
        removed_vertices = set()
        scc_index = 0
        while (len(to_explore) > 0):
            scc_indices = dfs_helper.explore(post_nums.index(max(to_explore)))
            removed = removed.union(scc_indices)
            to_explore = [post_nums[i] for i in range(len(post_nums)) if i not in removed]
            scc_vertices = [vertex for vertex in self.vertices if vertex.index in scc_indices]
            scc_vertices = set(scc_vertices).difference(removed_vertices)
            new_scc = ds.SCC(self, list(scc_vertices), scc_index)
            scc_index += 1
            removed_vertices = removed_vertices.union(scc_vertices)
            self.sccs.append(new_scc)

        # Index sccs
        self.sccs.reverse()
        for i in range(len(self.sccs)):
            self.sccs[i].index = i

        # Find the neighbor sccs of all sccs
        for i in range(len(self.sccs)):
            neighbors = []
            for vertex in self.sccs[i].vertices:
                for vertex_neighbor in vertex.neighbors:
                    if vertex_neighbor not in self.sccs[i].internals:
                        neighbors.append(self.which_scc(vertex_neighbor))
            self.scc_neighbors.append(neighbors)

    def which_scc(self, vertex_index):
        """Given a index of a vertex, return the index of the SCC it belongs to"""
        for scc in self.sccs:
            if vertex_index in scc.internals:
                return scc.index
        return -1

    def is_dag(self):
        """Return if the original graph is a dag or not"""
        return len(self.sccs) == len(self.vertices)

    def delete_path(self, path):
        """
        Use in longest_path.py
        """
        if path == []:
            return
        for v in self.vertices:
            if v.index in path:
                self.vertices[v.index].value = 0
                self.vertices[v.index].neighbors = []
            else:
                for neighbor in v.neighbors:
                    if neighbor in path:
                        v.neighbors.remove(neighbor)

        scc = self.sccs[self.which_scc(path[0])]
        for vertex in scc.in_vertices:
            if vertex in path:
                scc.in_vertices.remove(vertex)
        for vertex in scc.out_vertices:
            if vertex in path:
                scc.out_vertices.remove(vertex)
        for scc in self.sccs:
            for neighbor in scc.neighbors:
                if neighbor in path:
                    scc.neighbors.remove(neighbor)

    def get_score(self, assignment):
        score = 0
        for path in assignment:
            values = [self.sccs[i].value for i in path]
            score += sum(values) * len(values)
        return score

    def solve(self):

        sub = [[[0, []] for _ in range(self.scc_size)] for _ in range(self.scc_size)]
        for i in range(self.scc_size):
            sub[i][i][0] = self.sccs[i].value
            sub[i][i][1].append([self.sccs[i].index])

        for m in range(1, self.scc_size):
            sub_range = list(range(m))
            sub_range.reverse()

            for i in sub_range:
                max_val = -1
                max_assignment = []

                for k in range(i+1, m+1):
                    assignment = copy.deepcopy(sub[k][m][1])
                    if k in self.scc_neighbors[i]:
                        assignment[0].insert(0,i)
                    else:
                        assignment.insert(0,[i])
                    if k > i + 1:
                        value = self.get_score(assignment) + sub[i + 1][k - 1][0]
                        assignment = assignment + sub[i+1][k-1][1]
                    else:
                        value = self.get_score(assignment)
                    if (value > max_val):
                        max_val = value
                        max_assignment = copy.deepcopy(assignment)
                sub[i][m] = [max_val, max_assignment]
        max_assignment = sub[0][self.scc_size - 1][1]
        max_assignment_vertices = []

        for path in max_assignment:
            max_assignment_vertices.append([self.sccs[scc_index].vertices[0].index for scc_index in path])

        return sub[0][self.scc_size - 1][0], max_assignment_vertices


# Test
# def run(p):
#
#     result = open('new_dag.txt', "a")
#     for i in range(p, p+1):
#
#         try:
#             g = ds.Graph("../inputs/dag_exact/" + str(i) + ".in")
#             if (len(g.vertices) in range(0, 501)):
#                 start_time = time.time()
#                 print str(i)+".in"
#                 g = DAG("../inputs/dag_exact/"+str(i)+".in")
#                 print("--- %s seconds to process DAG ---" % (time.time() - start_time))
#
#                 if g.is_dag():
#                     print str(i)+" is a DAG"
#                     start_time = time.time()
#                     soln = g.solve()[1]
#                     result.write(str(i) + ". " + str(soln))
#                     result.write("\n")
#                     print(i, soln)
#                     print("--- %s seconds to solve DAG---" % (time.time() - start_time))
#                     result = open('new_dag.txt', "a")
#         except (IOError):
#             pass
#         except (IndexError):
#             pass