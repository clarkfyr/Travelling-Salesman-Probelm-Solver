import object
import pdb
import copy
import time
import random
from joblib import Parallel, delayed
import multiprocessing

class SCC(object.Graph, object.Vertex):
    """
    Instance attributes
    self.vertices: Inherited from Graph. vertices in this SCC
    self.neighbors: Inherited from Vertex. indices of neighbor vertices
    self.value: Inherited from Vertex. Set to 0 if this SCC contains multiple vertices
    self.index: Inherited from Vertex. Represent the index of SCC in parent graph
    self.internals: Indices of internal vertices
    self.in_vertices: Indices of vertices with in coming edges
    self.out_vertices: Indices of vertices with out going edges
    """
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

# class SubGraph(object.Graph):
#     """
#     Instance variables:
#     self.g: parent graph of this SubGraph
#     """
#     def __init__(self, g, vertices):
#         self.g = g
#         self.vertices = vertices

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
        # Start from specified start vertex
        # self._dfs(self.g, start, random)
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
        try:
            for neighbor in neighbors:
                if neighbor not in self.visited:
                    self._dfs(g, neighbor, rand)
        except:
            pdb.set_trace()
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

# Transform a graph into a dag of SCC
class DAG(object.Graph):
    """
    # Instance attributes
    # self.sccs: list of SCCs in this graph
    # self.scc_neighbors: list of SCC neighbors of SCCs. Similar format as self.neighbors
    """
    def cal_score(self, assignment):
        score = 0
        for path in assignment:
            values = [self.sccs[i].value for i in path]
            score += sum(values) * len(values)
        return score

    def __init__(self, filename):

        object.Graph.__init__(self, filename)
        self.sccs = []
        self.scc_neighbors = []
        self.sub_graphs = []
        self._set_scc()
        # self._set_subgraph()
        self.size_in_scc = len(self.sccs)

    def _set_scc(self):
        # Find all sccs
        # Run DFS on GR
        self.reverse()
        dfs_helper = DFS(self)
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
            new_scc = SCC(self, list(scc_vertices), scc_index)
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
                        neighbors.append(self.locate_scc(vertex_neighbor))
            self.scc_neighbors.append(neighbors)

    # def _set_subgraph(self):
    #     self.undirected()

    def locate_scc(self, vertex_index):
        """Given a index of a vertex, return the index of the SCC it belongs to"""
        for scc in self.sccs:
            if vertex_index in scc.internals:
                return scc.index
        return -1

    def print_dag(self):
        for i in range(len(self.sccs)):
            line = ""
            # print(self.sccs[i].scc_neighbors)
            for j in range(len(self.sccs)):
                if (j in self.scc_neighbors[i]):
                    line += str(1) + " "
                else:
                    if (i == j):
                        line += str(self.sccs[i].value) + " "
                    else:
                        line += str(0) + " "
            line += "Nodes: "
            line += ", ".join(list(map(str, self.sccs[i].internals)))
            print(line)

    def is_dag(self):
        """Return if the original graph is a dag or not"""
        return len(self.sccs) == len(self.vertices)

    def delete_path(self, path):
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

        scc = self.sccs[self.locate_scc(path[0])]
        for vertex in scc.in_vertices:
            if vertex in path:
                scc.in_vertices.remove(vertex)
        for vertex in scc.out_vertices:
            if vertex in path:
                scc.out_vertices.remove(vertex)
        # if (len(scc.vertices) == 1):
        #     scc.value = scc.vertices[0].value
        # elif (len(scc.vertices) == 0):
        #     scc.value = 0

        for scc in self.sccs:
            for neighbor in scc.neighbors:
                if neighbor in path:
                    scc.neighbors.remove(neighbor)

    def solve(self):
        """solve a dag"""
        sub = [[[0, []] for _ in range(self.size_in_scc)] for _ in range(self.size_in_scc)]
        for i in range(self.size_in_scc):
            sub[i][i][0] = self.sccs[i].value
            sub[i][i][1].append([self.sccs[i].index])
        for m in range(1, self.size_in_scc):
            # print(m)
            # pdb.set_trace()
            sub_range = list(range(m))
            sub_range.reverse()
            for i in sub_range:
                max_val = -1
                max_assignment = []
                for k in range(i+1, m+1):
                    assignment = copy.deepcopy(sub[k][m][1])
                    if (k in self.scc_neighbors[i]):
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
        max_assignment = sub[0][self.size_in_scc - 1][1]
        max_assignment_vertices = []
        for path in max_assignment:
            try:
                max_assignment_vertices.append([self.sccs[scc_index].vertices[0].index for scc_index in path])
            except:
                pdb.set_trace()
            
        return (sub[0][self.size_in_scc - 1][0], max_assignment_vertices)

# def run(i):
#     """main function for parallelized main"""
#     try:
#         start_time = time.time()
#         g = DAG("../inputs/unsolved/"+str(i)+".in")
#         print(str(i)+".in")
#         print("--- %s seconds to process DAG ---" % (time.time() - start_time))
#         for scc in g.sccs:
#             print("----------- # %s SCC -------------" % (scc.index))
#             for v in scc.vertices:
#                 print(v.index)
#             print("In vertices: ")
#             for v in scc.in_vertices:
#                 print(v.index)
#             print("Out vertices: ")
#             for v in scc.out_vertices:
#                 print(v.index)
#     except (IOError):
#         pass
#     except (IndexError):
#         pass
# 
# def test_run():
#     start = time.time()
#     g = DAG("../inputs/dag_exact/72.in")
#     sol = g.solve()
#     print(sol[1])
#     print(time.time() - start)



import time
    # start_time = time.time()

    # g = DAG("./result.txt")
    # g.print_graph()
    # sol = g.solve()
    # print(sol[0])
    # print(sol[1])
def run(p):
    # print("--- %s seconds ---" % (time.time() - start_time))
    result = open('new_dag.txt', "a")
    for i in range(p, p+1):
        # if i in hard or i in easy or i in moderate:
        #   continue
        try:
            g = object.Graph("../inputs/dag_exact/"+str(i)+".in")
            if (len(g.vertices) in range(0, 501)):
                start_time = time.time()
                print str(i)+".in"
                g = DAG("../inputs/dag_exact/"+str(i)+".in")
                print("--- %s seconds to process DAG ---" % (time.time() - start_time))
                # result.write(str(i)+" is not a DAG" + "\n")
                if g.is_dag():
                    print str(i)+" is a DAG"
                    start_time = time.time()
                    soln = g.solve()[1]
                    result.write(str(i) + ". " + str(soln))
                    result.write("\n")
                    print(i, soln)
                    print("--- %s seconds to solve DAG---" % (time.time() - start_time))
                    # result.write(str(i) + ". " + str(soln))
                    # result.write("\n")
                    result = open('new_dag.txt', "a")
        except (IOError):
            pass
        except (IndexError):
            pass

# import time
#     result = open('new_dag.txt', "a")
#     for i in range(p, p+1):
#         # if i in hard or i in easy or i in moderate:
#         #   continue
#         try:
#             start_time = time.time()
#             path_list = [];
#             temp_score = 0
#             temp_path = []
#             # numV = []
# 
#             print(str(i)+".in")
#             g = object.Graph("../inputs/dag_exact/"+str(i)+".in")
#             for j in range(0, 1):
#                 order = (random_dfs_explore(g, find_sources_and_singles(g)["sources"]))
#                 path = object.get_path_from_order(g, order)
#                 path_list.append(path)
#             for p in path_list:
#                 score = compute_score_full_assignment(g, p)
#                 if score >= temp_score:
#                     temp_path = p
#                     temp_score = score
#             # for p in path_list:
#             #     num = 0
#             #     for i in p:
#             #         if type(i) == int:
#             #             num += 1
#             #         else:
#             #             num += len(i)
#             #     numV.append(num)
#             # print(numV)
#             soln = temp_path
#             # resultOld = open('dfs_approx_0_80.txt', "r")
#             # result.write(str(resultOld.read()))
#             # result = open('dfs_approx_0_80.txt', "w")
#             result.write(str(i) + ". " + str(soln))
#             result.write("\n")
#             result = open('new_5000.txt', "a")
#             print(i, soln)
#             print("--- %s seconds to solve graph---" % (time.time() - start_time))
#             # break;
#         except (IOError):
#             pass

# num_cores = multiprocessing.cpu_count()
# Parallel(n_jobs=num_cores)(delayed(run)(i) for i in range(0, 601))
