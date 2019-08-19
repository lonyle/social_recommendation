# all users have the same recommendation prob.
# tried to do parallel sampling, but the memory is not enough

import numpy as np 
from scipy.special import comb
import sampling
import json
import osn
import matplotlib.pyplot as plt
from multiprocessing import Pool, Manager, Process

sampling_result_filename = 'data/output_sampling.json'
#graph = osn.OnlineSocialNetwork('/home/liye/Data/yelp-round11/user.json')
osn_filename = '/home/liye/Data/yelp-round11/user.json'

def get_random_RRset_size(graph_dict):
	print ('Number of users:', len(graph_dict))
	nodes = graph_dict.keys()
	v = np.random.choice( list(nodes) )
	shuffle_node_vec = list(nodes)
	np.random.shuffle(shuffle_node_vec)
	RRset = set([v])
	print ('Number of neighbors of v:', len(graph_dict[v]))
	if len(graph_dict[v]) == 0: # shortcut
		return [1] * len(nodes)

	size_vec = []
	## initialize awaiting_flag: awaiting to be added to the cluster
	awaiting_flag = dict()
	for node in nodes:
		awaiting_flag[node] = False
	####
	count = 0
	for node in shuffle_node_vec:
		# count += 1
		# if count % 10000 == 0:
		# 	print (count)
		if node == v:
			continue
		awaiting_flag[node] = True
		neighbors = graph_dict[node]

		current_nodes = []
		# check whether a node is in RRset
		for neighbor in neighbors:
			if neighbor in RRset: # new node will be added
				#RRset.add(node)
				current_nodes = [node]
				break
		
		# diffusion to other nodes
		while len(current_nodes) > 0:
			# the new nodes are added in the RRset, so these nodes will not be in the awaiting set
			for node_ in current_nodes:
				RRset.add(node_)
				awaiting_flag[node_] = False

			new_nodes = []
			for node_ in current_nodes:
				neighbors_ = graph_dict[node_]
				for neighbor_ in neighbors_:
					if neighbor_ in awaiting_flag: # check the existence of key
						if awaiting_flag[neighbor_] == True:
							new_nodes.append(neighbor_)
			current_nodes = new_nodes[:]
			
		size_vec.append(len(RRset))
	return size_vec

def store_sampling_results(graph_dict, N_sample = 1000):		
	pool = Pool(8)
	future_results = [pool.apply_async(get_random_RRset_size, (graph_dict,) ) for _ in range(N_sample)]
	pool.close()
	pool.join()
	
	size_mat = [f.get() for f in future_results]

	# size_mat = []
	# for n in range(N_sample):
	# 	print ('sample', n)
	# 	size_vec = get_random_RRset_size() # store the results
	# 	print ('size of the largest RRset', size_vec[-1])
	# 	# plt.plot(np.arange(len(size_vec)), size_vec)
	# 	# plt.show()

	# 	size_mat.append(size_vec)

	print ('dumping to file...')
	with open(sampling_result_filename, 'w') as output_file:
		json.dump(size_mat, output_file)
	print ('dumped.')
	return size_mat

def get_S(graph, initial_prob): # probability for an node to adopt given r nodes are occupied
	prob_vec = sampling.get_prob_table(initial_prob, graph.N_node)
	
	size_mat = json.load(open(sampling_result_filename))
	S_mat = []
	for size_vec in size_mat:
		S_vec = []
		for size in size_vec:
			S = prob_vec[size]
			S_vec.append(S)
		S_mat.append(S_vec)
	S_matrix = np.matrix(S_mat)
	S_average = S_matrix.mean(0).ravel()
	return S_average

def expected_size(graph, initial_prob, percolation_prob): # phi is the percolation probability
	S = get_S(graph, initial_prob)
	phi = percolation_prob
	sum_ = 0
	N = graph.N_node
	for r in range(N):
		sum_ += S[r] * comb(N, r, exact=True) * phi**r * (1-phi)**(N-r)
	return sum_

if __name__ == '__main__':
	with Manager() as manager:
		graph_dict = manager.dict()
		f = open(osn_filename)
		line = f.readline()
		while line:
			data = json.loads(line)
			user_id = data['user_id']
			friends = data['friends']
			graph_dict[user_id] = friends
			line = f.readline()
		f.close()

	
		store_sampling_results(graph_dict)

	initial_prob =  0.5
	percolation_prob = 0.5
	#expected_size(graph, initial_prob, percolation_prob)

