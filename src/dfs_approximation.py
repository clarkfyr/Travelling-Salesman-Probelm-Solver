import dag
import object
import random
import pdb

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
    new_graph = object.delete_given_path(graph, singles)

    # If no source, it's a huge cycle
    total_path = random_dfs_explore(graph, sources)

    return total_path

def random_dfs_explore_jk(graph, sources):
    sources_list = sources
    dfs_path = []
    g = graph
    while True:
        finish_iter = True
        for v in g.vertices:
            if v.value != 0:
                finish_iter = False
                break
        if finish_iter == True:
            break
        start = None
        if sources_list:
            start = random.choice(sources)
        else:
            for v in g.vertices:
                if v.value != 0:
                    start = v.index
        stack = [start]
        visited = set()
        temp_path = []
        # visited_vertices = []
        while (len(stack) > 0):
            curr = stack.pop()
            visited.add(curr)
            temp_path.append(curr)
            if curr in sources_list:
                sources_list.remove(curr)
            # visited_vertices = visited_vertices.append(self.g.vertices[curr])
            neighbors = g.vertices[curr].neighbors
            random.shuffle(neighbors)
            for neighbor in neighbors:
                if (neighbor not in visited) and (g.vertices[neighbor].value != 0) and (neighbor not in dfs_path) and (neighbor not in temp_path):
                    stack.append(neighbor)
        g = object.delete_given_path(g, temp_path)
        print temp_path
        for index in temp_path:
            dfs_path.append(index)
    return dfs_path

def random_dfs_explore(graph, sources):
    magic = dag.DFS(graph)
    pre_nums = magic.dfs(sources, True)[0]
    indices = [index for value, index in sorted((e,i) for i,e in enumerate(pre_nums))]
    return indices


def test_run():
    g = dag.DAG("../inputs/dag_exact/10.in")
    print(random_dfs_explore(g, find_sources_and_singles(g)["sources"]))
