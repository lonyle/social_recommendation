def get_edges(filename = 'optimization/facebook_combined.txt'):
	''' get the edges (dictionary of lists) for facebook network
	'''
	print ('loading the facebook edges...')
	edges = dict()
	with open(filename) as f:
		for line in f:
			out_node, in_node = line.strip().split(' ')
			if out_node not in edges:
				edges[out_node] = []
			edges[out_node].append(in_node)

			# undirected edges
			if in_node not in edges:
				edges[in_node] = []
			edges[in_node].append(out_node)

	return edges
