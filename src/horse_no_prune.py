import object
import copy

def horse(graph):
    vertices = graph.vertices
    all_path = []
    # Zero Edge Situation
    if graph.numE == 0:
        for v in vertices:
            all_path.append([v])
        return all_path

    # Base level subproblems
    size_one_prob = []
    for v in vertices:
        sub = object.Subproblem(v, v, set([v]), [[v]], v.value)
        size_one_prob.append(sub)

    # Prune: find the sources of this graph
    sources = []
    for v in vertices:
        if not v.neighbors:
            sources.append(v)
    if not sources:
        sources = vertices
    # Perform TSP on each source
    results = [] # best subproblem for each starting vertex
    for v in sources:
        prevProblems = size_one_prob
        for s in range(2, len(vertices) + 1):
            print(v.index, s)
            # Create all subproblems with size s
            problems = []
            for prev in prevProblems:
                if v in prev.visited: # pick subproblems that start with v
                    for v_j in list(set(vertices) - prev.visited):
                        visited = prev.visited.copy()
                        sub = object.Subproblem(v, v_j, visited, copy.deepcopy(prev.path), prev.score)
                        visited.add(v_j)
                        sub.update_path_score(v_j)
                        problems.append(sub)
            prevProblems = problems
        maxV = max([p.score for p in problems])
        best_sub = [p for p in problems if p.score == maxV][0]
        results.append(best_sub)

    maxV = max([p.score for p in results])
    best = [p for p in results if p.score == maxV][0]
    return best.path

def print_graph(g):
    graph = dict()
    for v in g.vertices:
        graph[str(v.index)] = v.neighbors
    print graph

def print_path(path):
    paths = []
    for p in path:
        temp = [x.index for x in p]
        paths.append(temp)
    print paths
    return paths

# Test
if __name__ == '__main__':
    import time
    start_time = time.time()

    g = object.Graph("../final_inputs/53.in")
    path = horse(g)
    print_path(path)

    print("--- %s seconds ---" % (time.time() - start_time))
