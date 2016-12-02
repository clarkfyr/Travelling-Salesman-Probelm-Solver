import object
import dag
import tsp
import longest_path as lp

def find_end(dag, scc1, scc2):
    if scc2 is None:
        return [_.index for _ in scc1.vertices]
    for v in scc1.out_vertices:
        if dag._locate_scc(v) == scc2.index:
            return v

def tsp_dag(dag):
    """
    Use longest path on SCC groups that have more than 1 SCC
    Use TSP on disconnected SCC groups that have only 1 SCC
    :param scc_list: a list of SCC groups
    :return: a list of paths
    """
    scc_list = dag.solve()
    total_path = []
    for group in scc_list:
        if len(group) == 1: # Disconnected SCC
            g = object.Graph()
            g.add_vertices(group[0].vertices)
            total_path += tsp.tsp(g)
        else: # Connected SCC
            # First SCC
            super_path = []
            i = 0
            scc = group[i]
            next_scc = group[i + 1]
            starts = scc.vertices
            ends = find_end(dag, scc, next_scc)
            while i < len(group):
                s, e, path = lp.find_longest_among_longest(dag, scc, starts, ends)
                super_path += path
                if i == len(group) - 1: # The end
                    break
                i += 1
                scc = group[i]
                if (i + 1) == len(group):
                    next_scc = None
                else:
                    next_scc = group[i + 1]
                starts = [_ for _ in dag.vertices[e].neighbors if dag._locate_scc(_) == next_scc]
                ends = find_end(dag, scc, next_scc)

    return total_path

if __name__ == "__main__":
    dag = dag.DAG("../inputs/greedy_approximation/145.in")

