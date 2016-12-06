"""
Longest Path Approximation
"""
import data_structure as ds
import copy
import utility
import time
import dag


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


def highest_single_path(graph):
	"""greedily find the single path with highest score in a graph"""
	highest_score_path = []
	highest_score = 0
	for v in graph.vertices:
		if v.value != 0:
			paths = modified_bfs(graph, v.index)[1]
			for p in paths:
				score = utility.compute_score(graph, p)
				if score > highest_score:
					highest_score_path = [p]
					highest_score = score
				elif score == highest_score:
					highest_score_path.append(p)
	return highest_score, highest_score_path


def greedy_highest_path_approximation(graph):
	"""use greedy algs to find an approximating path"""
	def helper(prev_graph, prev_path):
		curr_graph = ds.delete_given_path(prev_graph, prev_path)
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
		s = utility.compute_score_full_assignment(graph, out)
		if s >= score:
			score = s
			final = out
	return score, final


def get_longest_path_in_scc(graph, s, t):
	"""find longest path from s to t and all other paths in scc"""
	if graph.which_scc(s) != graph.which_scc(t):
		return None
	scc_index = graph.which_scc(s)

	# Delete the through path from s to t
	through_path = modified_bfs_in_scc(graph, s)[1][t]
	graph.delete_path(through_path)
	final_out = [through_path]
	# final_out = []
	run = sum([vertex.value for vertex in graph.sccs[scc_index].vertices]) > 0

	flatten = lambda l: [item for sublist in l for item in sublist]

	while run:
		length = 0
		path = None
		for v in graph.sccs[scc_index].vertices:
			curr_paths = modified_bfs_in_scc(graph, v.index)[1]

			for curr_path in curr_paths:
				if (curr_path == [v.index] and v.index in flatten(final_out)):
					curr_path = []
				if (curr_path and len(curr_path) > length):
					length = len(curr_path)
					path = curr_path

		if (path and len(path) > 0):
			final_out.append(path)
			graph.delete_path(path)
			run = sum([vertex.value for vertex in graph.sccs[scc_index].vertices]) > 0
		else:
			run = False
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
			if v not in prob[1] and graph.which_scc(s) == graph.which_scc(v):
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
			path = modified_bfs_in_scc(dag, scc, i)[1][j]
			if not maxPath or len(maxPath) < len(path):
				maxPath = path
				start = i
				end = j
	return start, end, maxPath


# Test
def run():
	result = open('highest_single_path_approximation.txt', "w")

	for i in range(1, 601):
		try:
			g = ds.Graph("../inputs/unsolved/"+str(i)+".in")
			print str(i)+".in"
			if len(g.vertices) <= 50:
				start_time = time.time()
				path = greedy_highest_path_approximation(g)
				print path
				if path:
					result.write(str(i) + ". " + str(path[1]) + " score: " + str(path[0]))
					result.write("\n")
				print("--- %s seconds ---" % (time.time() - start_time))
		except (IOError, IndexError):
			pass

g = dag.DAG("../inputs/unsolved/332.in")
ps = get_longest_path_in_scc(g,20,43)
