import object
import copy

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
	return dist, path

def find_fully_connected(graph):
	"""find if there is a path that connect every vertex"""
	vertices = graph.vertices
	for i in range(0, len(vertices)):
		print i
		dist, path = modified_bfs(g, i)
		if max(dist) == len(vertices) - 1:
			for ind in range(0, len(dist)):
				if dist[ind] == len(vertices) - 1:
					result = copy.deepcopy(path[ind])
					result.append(ind)
					return result
	return None

def find_longest_path(graph, s, t):
	"""take in a graph and the index of the starting vertex and the index of the ending vertex; 
		return longest distance and path from s to t"""
	dist_list, path_list = modified_bfs(graph, s)
	return dist_list[t], path_list[t]

def compute_score(graph, lists_of_pathes):
	"""take in a graph and a list of pathes and compute the score
	under the assuption that the proposed soln is valid"""
	vertices = graph.vertices
	score = 0
	for lst in lists_of_pathes:
		base = 0
		for v in lst:
			base += vertices[v].value
		score += base * len(lst)
	return score

def approximation_longest_path(graph):
	pass

def delete_given_path(graph, path):
	g = copy.deepcopy(graph)
	vertices = g.vertices
	for v in vertices:
		pass

# find all fully connected
if __name__ == '__main__':
    import time
    result = open('fully_connected.txt', "w")
    hard = [4, 6, 10, 16, 17, 20, 22, 34, 35, 51, 53, 56, 57, 58, 59, 81, 89, \
    109, 111, 114, 115, 116, 117, 124, 125, 140, 141, 147, 154, 160, 162, 163, 172, 173, 174, 180, 184, \
    233, 235, 236, 237, 241, 242, 243, 245, 246, 250, 252, 254, 260, 277, 281, 285, 292, 293, 295, 296, \
    302, 313, 314, 315, 317, 318, 320, 325, 349, \
    358, 359, 360, 361, 363, 365, 373, 374, 376, 377, 382, 383, 384, 391, 393, \
    400, 401, 405, 410, 411, 424, 425, 440, 441, 445, 446, 447, \
    454, 455, 457, 459, 466, 470, 476, 481, 482, 490, 491, 494, 495, \
    503, 504, 512, 513, 514, 532, 533, 549, 559, 566, 567, 572, 577, 579, 586, 592, 594]

    moderate = [19, 72, 145, 149, 155, 156, 164, 187, 188, 189, 215, \
    316, 340, 341, 342, 364, 422, 436, 483, 507, 517, 560]

    easy = [62, 119]

    for i in range(1, 601):
    	if i in hard or i in easy or i in moderate:
    		continue
        try:
            g = object.Graph("../final_inputs/"+str(i)+".in")
            print str(i)+".in"
            if len(g.vertices) <= 300:
	            start_time = time.time()
	            path = find_fully_connected(g)
	            print path
	            if path:
		            result.write(str(i) + ". " + str(path))
		            result.write("\n")
	            print("--- %s seconds ---" % (time.time() - start_time))
        except (IOError):
            pass
        except (IndexError):
            pass