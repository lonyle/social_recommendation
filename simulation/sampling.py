# sampling and estimation in the basic way: generating RRset
# In a sample, we need to record the nodes that is the reverse reachable set (in the same cluster for undirected graph)

import numpy as np
import setting
import estimation

import sys
sys.path.insert(0, 'preprocess')
import osn

def get_RRset(graph, act_nodes, v): #undirected graph
	current_nodes = [v]
	RRset = set()
	while len(current_nodes) > 0:
		new_nodes = []
		for node in current_nodes:
			neighbors = graph.edges[node]
			for neighbor in neighbors:
				if (neighbor in act_nodes) and (neighbor not in RRset) and (neighbor != v):
					new_nodes.append(neighbor)
					RRset.add(neighbor)
		current_nodes = new_nodes[:]

	return RRset

def get_random_RRset(graph, occupation_prob_type, type_node_v):
	while True: # generate a node with required type
		v = np.random.choice(list(graph.nodes))
		degree = len(graph.edges[v])
		if type_node_v == setting.type_of_node(degree):
			break
	
	act_nodes = set()
	for node in graph.nodes:
		degree = len(graph.edges[node])
		Type = setting.type_of_node(degree)
		if np.random.random() < occupation_prob_type[Type]:
			act_nodes.add(node)
	print ('number of act_nodes:', len(act_nodes) )
	RRset = get_RRset(graph, act_nodes, v)
	return RRset

# for comparison with the result obtained by sampling_sequence.py
def get_est_informed_prob(graph, initial_prob, occupation_prob_type, type_node_v, N_samples=100):
	# the estimated fraction of users who make recommendations
	prob_vec = estimation.get_prob_table(initial_prob, graph.N_node)
	sum_prob = 0.0
	for n in range(N_samples):
		RRset = get_random_RRset(graph, occupation_prob_type, type_node_v)
		size_RRset = len(RRset)
		FriRec_prob = prob_vec[size_RRset]
		
		sum_prob += FriRec_prob
		
		est = sum_prob / (n+1)
		print ('N_sample:', n+1, 'Type:', type_node_v, 'size_RRset:', size_RRset)
		print ('# estimated FriRec_prob:', est)
	return est


if __name__ == '__main__':
	graph = osn.OnlineSocialNetwork('yelp')
	initial_prob = 0.001
	occupation_prob_type = {'small': 0.05, 'medium': 0.15, 'large': 0.1}
	get_est_informed_prob(graph, initial_prob, occupation_prob_type, 'medium')

	# medium: 0.0004842586257624044 (500)
	# medium: 0.00042778954009355563 (500)
	# medium: 0.00022749070417168183 (500)
	# large: 0.0033110632966083394 (500)
	# large: 0.0027964006863371495 (2000)