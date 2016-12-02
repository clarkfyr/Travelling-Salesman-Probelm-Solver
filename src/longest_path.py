import object
import copy
import dag
import pdb

def modified_bfs(graph, s):
	"""take in a graph and the index of the starting vertex;
		return a list of longest distance to every vertex and path"""
	vertices = graph.vertices
	dist = []
	path = []
	queue = []
	for i in range(0, len(vertices)):
		dist.append(-1)
		path.append([])
	queue.append([s, path[s]])
	while len(queue) != 0:
		prob = queue.pop(0)
		if len(prob[1]) >= dist[prob[0]] and len(prob[1]) < len(vertices):
			path[prob[0]] = prob[1]
			dist[prob[0]] = len(prob[1])
		for v in vertices[prob[0]].neighbors:
			if v not in prob[1]:
				new_path = copy.deepcopy(prob[1])
				new_path.append(prob[0])
				new_prob = [v, new_path]
				queue.append(new_prob)
	for i in range(0, len(vertices)):
		if vertices[i].value != 0:
			path[i].append(i)
	return dist, path

def find_fully_connected(graph):
	"""find if there is a path that connect every vertex"""
	vertices = graph.vertices
	for i in range(0, len(vertices)):
		dist, path = modified_bfs(g, i)
		if max(dist) == len(vertices) - 1:
			for ind in range(0, len(dist)):
				if dist[ind] == len(vertices) - 1:
					result = copy.deepcopy(path[ind])
					return result
	return None

def find_longest_path(graph, s, t):
	"""take in a graph and the index of the starting vertex and the index of the ending vertex;
		return longest distance and path from s to t"""
	dist_list, path_list = modified_bfs(graph, s)
	return dist_list[t], path_list[t]

def compute_score(graph, list_of_path):
	"""take in a graph and a pathes and compute the score
	under the assuption that the proposed soln is valid"""
	vertices = graph.vertices
	score = 0
	base = 0
	for v in list_of_path:
		base += vertices[v].value
	score += base * len(list_of_path)
	return score

def compute_score_full_assignment(graph, paths):
	"""take in a graph and a full assignment lists of pathes and compute the total score of the given soln"""
	total = 0
	for path in paths:
		total += compute_score(graph, path)
	return total

def highest_single_path(graph):
	"""greedily find the single path with highest score in a graph"""
	highest_score_path = []
	highest_score = 0
	for v in graph.vertices:
		if v.value != 0:
			paths = modified_bfs(graph, v.index)[1]
			for p in paths:
				score = compute_score(graph, p)
				if score > highest_score:
					highest_score_path = [p]
					highest_score = score
				elif score == highest_score:
					highest_score_path.append(p)
	return highest_score, highest_score_path

def greedy_highest_path_approximation(graph):
	"""use greedy algs to find an approximating path"""
	def helper(prev_graph, prev_path):
		curr_graph = object.delete_given_path(prev_graph, prev_path)
		return_path = []
		single_path = highest_single_path(curr_graph)[1]
		if not single_path:
			return [[]]
		for curr_path in single_path:
			paths = helper(curr_graph, curr_path)
			for path in paths:
				path.append(curr_path)
				return_path.append(path)
		return return_path
	first_path = highest_single_path(graph)[1]
	final_out = []
	for first in first_path:
		Fpaths = helper(graph, first)
		for Fpath in Fpaths:
			Fpath.append(first)
			final_out.append(Fpath)
	score = 0
	final = None
	for out in final_out:
		s = compute_score_full_assignment(graph, out)
		if s >= score:
			score = s
			final = out
	return score, final

def get_longest_path_in_scc(graph, s, t):
	"""find longest path from s to t and all other paths in scc"""
	if graph.locate_scc(s) != graph.locate_scc(t):
		return None
	original_path = modified_bfs_in_scc(graph, s)[1][t]
	new_graph = object.delete_given_path(graph, original_path)
	scc_index = graph.locate_scc(s)
	final_out = [original_path]
	while not end_iter:
		length = -1
		path = None
		for v in new_graph.sccs[scc_index].vertices:
			curr_paths = modified_bfs_in_scc(new_graph, v.index)[1]
			for curr_path in curr_paths:
				if len(curr_path) >= length + 1:
					length = len(curr_path) - 1
					path = curr_path
		final_out.append(path)
		new_graph = object.delete_given_path(new_graph, path)
		for v in new_graph.sccs[scc_index].vertices:
			end_iter = True
			if v.value != 0:
				end_iter = False
	return final_out

def modified_bfs_in_scc(graph, s):
	"""find longest path from s inside scc for given scc index"""
	vertices = graph.vertices
	dist = []
	path = []
	queue = []
	for i in range(0, len(vertices)):
		dist.append(-1)
		path.append([])
	queue.append([s, path[s]])
	while len(queue) != 0:
		prob = queue.pop(0)
		if len(prob[1]) >= dist[prob[0]] and len(prob[1]) < len(vertices):
			path[prob[0]] = prob[1]
			dist[prob[0]] = len(prob[1])
		for v in vertices[prob[0]].neighbors:
			if v not in prob[1] and graph.locate_scc(s) == graph.locate_scc(v):
				new_path = copy.deepcopy(prob[1])
				new_path.append(prob[0])
				new_prob = [v, new_path]
				queue.append(new_prob)
	for i in range(0, len(vertices)):
		if dist[i] != -1:
			path[i].append(i)
	return dist, path


def find_longest_among_longest(dag, scc, starts, ends):
	"""

	:param starts: starting vertex indices
	:param ends: ending vertex indices
	:return:
	"""
	maxPath = []
	start, end = None, None
	for i in starts:
		for j in ends:
			path = lp.modified_bfs_in_scc(dag, scc, i)[1][j]
			if not maxPath or len(maxPath) < len(path):
				maxPath = path
				start = i
				end = j
	return start, end, maxPath
	
# if __name__ == '__main__':
#     import time
#     result = open('highest_single_path_approximation.txt', "w")

#     for i in range(1, 601):
#     	# if i in hard or i in easy or i in moderate:
#     	# 	continue
#         try:
#             g = object.Graph("../inputs/unsolved/"+str(i)+".in")
#             print str(i)+".in"
#             if len(g.vertices) <= 50:
# 	            start_time = time.time()
# 	            path = greedy_highest_path_approximation(g)
# 	            print path
# 	            if path:
# 		            result.write(str(i) + ". " + str(path[1]) + " score: " + str(path[0]))
# 		            result.write("\n")
# 	            print("--- %s seconds ---" % (time.time() - start_time))
#         except (IOError):
#             pass
#         except (IndexError):
#             pass
