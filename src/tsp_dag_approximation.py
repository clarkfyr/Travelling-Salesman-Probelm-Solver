import object
import dag
import tsp
import longest_path as lp


def separate_sccs(dag):
    """
    Use to separate a graph's SCCs into subsets
    :param dag: graph based on DAG
    :return: a list of SCC groups
    """

    scc_lst = []
    sccs = [s.index for s in dag.sccs]
    # Find independent SCC and find its path
    for scc in dag.sccs:
        if (not scc.in_vertices) and (not scc.out_vertices):
            scc_lst.append([scc.index])
            sccs.remove(scc.index)

    # Group connected scc
    while sccs:
        s_j = sccs[0] # scc index
        temp = [s_j]
        if dag.sccs[s_j].in_vertices:
            for i in dag.sccs[s_j].in_vertices:
                in_s = dag.locate_scc(i)
                temp.append(in_s)
                sccs.remove(in_s)
        if dag.sccs[s_j].out_vertices:
            for j in dag.sccs[s_j].out_vertices:
                out_s = dag.locate_scc(j)
                temp.append(out_s)
                sccs.remove(out_s)
        scc_lst.append(temp)

    return scc_lst


def tsp_dag(scc_lst):
    """
    Use longest path on SCC groups that have more than 1 SCC
    Use TSP on disconnected SCC groups that have only 1 SCC
    :param scc_list: a list of SCC groups
    :return: a list of paths
    """

    total_path = []
    for group in scc_lst:
        if len(group) == 1: # Disconnected SCC
            g = object.Graph()
            g.add_vertices(group[0].vertices)
            total_path += tsp.tsp(g)
        else: # Connected SCC
            pass


    return total_path

if __name__ == "__main__":
    dag = dag.DAG("../inputs/greedy_approximation/145.in")
    a = separate_sccs(dag)

