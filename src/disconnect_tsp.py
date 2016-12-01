import object
import dag
import tsp
import longest_path as lp


def disconnect_tsp(dag):
    """
    Deal with situation where there are independent SCCs
    :param scc_list: a list of SCCs
    :return: [tuple <list, list>] (partial result path, unsolved SCCs)
    """
    # Find independent SCC and find its path
    total_path = []
    for scc in dag.sccs:
        if not scc.in_vertices and not scc.out_vertices:
            path = tsp.tsp(scc)
            total_path += path
            dag.sccs.remove(scc)

    total_path += lp.greedy_highest_path_approximation(dag)

    return total_path


