import dag

def find_sources_and_singles(graph):
    sources = [_.index for _ in graph.vertices][:] # Index
    singles = [] # Index
    for v in graph.vertices:
        for vv in v.neighbors:
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

    # If no source, it's a huge cycle
    if not sources:
        n = 10 # Number of times you want to run DFS
        maxValue, maxPath = 0, None
        for i in range(n):
            pass

    # Run DFS on each source
    for source in sources:
        pass
        # total_path += dfs_path(graph, source)

    return total_path


