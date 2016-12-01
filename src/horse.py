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

    # Prune: find the sources of this graph
    sources = []
    for v in vertices:
        is_source = True
        for u in vertices:
            if v.index in u.neighbors:
                is_source = False
        if is_source:
            sources.append(v)
    if not sources:
        sources = vertices

    # Perform TSP on each source
    results = [] # best subproblem for each starting vertex
    for v in sources:
        prevProblems = [object.Subproblem(v, v, set([v]), [[v]], v.value)]

        for s in range(2, len(vertices) + 1):
            print v.index, s
            # Create all subproblems with size s
            problems = []
            for prev in prevProblems:

                # Prune: Only look at prev.children
                end_points = []
                for a in prev.end.neighbors: # Add all child that's unvisited
                    if vertices[a] not in prev.visited:
                        end_points.append(vertices[a])
                if not end_points: # Prev has no child in unvisited
                    for b in sources:
                        if b not in prev.visited:
                            end_points.append(b)
                if not end_points: # No sources in unvisited
                    end_points = list(set(vertices) - prev.visited)

                # Try all end points
                for v_j in end_points:
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
    print best.score
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
    hard = [56, 57, 163, 254, 325, 364, 405, 441, 445, 454, 504, 507, 517]
    # easy = [19, 145, 155, 156, 164, 187, 188, 364, 422, 436, 507]
    easy = [62, 119]
    result = open('result.txt', "w")
    for i in easy:
        if i in hard:
            continue

        try:
            g = object.Graph("../final_inputs/"+str(i)+".in")
            print "../final_inputs/"+str(i)+".in"

            # if len(g.vertices) <= 20:
            start_time = time.time()
            path = horse(g)
            p = print_path(path)
            result.write(str(i) + ". " + str(p))
            result.write("\n")

            print("--- %s seconds ---" % (time.time() - start_time))
        except (IOError):
            print(str(i) + " solved")
        except (IndexError):
            print(str(i) + " error")
